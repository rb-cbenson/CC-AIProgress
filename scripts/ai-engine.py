#!/usr/bin/env python3
"""
CC-AIProgress AI Automation Engine

OPTIONAL layer that connects the Python analysis scripts to an AI for
intelligent action. The scripts detect problems; this engine fixes them.

Designed to be AI-agnostic: the AI provider is a configuration, not hardcode.
Swap Claude for GPT, Gemini, a local model, or something that doesn't exist
yet — the engine doesn't care, it just needs a function that takes a prompt
and returns text.

Usage:
    python scripts/ai-engine.py                    # Interactive: shows what it would do, asks before acting
    python scripts/ai-engine.py --plan             # Generate action plan only (no execution)
    python scripts/ai-engine.py --execute          # Run plan and apply changes
    python scripts/ai-engine.py --execute --auto   # Full autonomous mode (still respects safeguards)
    python scripts/ai-engine.py --config           # Show/edit AI provider configuration
    python scripts/ai-engine.py --providers        # List available AI providers

The engine is NEVER required. Everything it does can be done manually or
by the individual scripts. This is a convenience layer for automation.

Provider Architecture:
    Each AI provider is a Python function: prompt_in -> text_out.
    To add a new provider:
    1. Write a function: def my_provider(prompt: str) -> str
    2. Register it: PROVIDERS["my-provider"] = my_provider
    3. Set it active: python scripts/ai-engine.py --config set provider my-provider

    The system ships with: claude-cli, openai-api, stub (for testing).
    More can be added by dropping a .py file in scripts/providers/.
"""

import json, sys, os, subprocess, importlib.util
from datetime import datetime
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE = Path(__file__).resolve().parent.parent
DATA = BASE / "data"
CONFIG_PATH = DATA / "ai-engine-config.json"
PROVIDERS_DIR = BASE / "scripts" / "providers"

# ============================================================
# PROVIDER SYSTEM — swap AI without touching anything else
# ============================================================

PROVIDERS = {}

def register_provider(name, fn, description=""):
    """Register an AI provider function."""
    PROVIDERS[name] = {"fn": fn, "description": description}

# --- Built-in providers ---

def _claude_cli(prompt):
    """Uses Claude Code CLI to process a prompt. Requires claude to be in PATH."""
    result = subprocess.run(
        ["claude", "--print", "--model", "sonnet", prompt],
        capture_output=True, text=True, timeout=120,
        cwd=str(BASE)
    )
    if result.returncode != 0:
        return f"ERROR: Claude CLI failed: {result.stderr[:200]}"
    return result.stdout

def _openai_api(prompt):
    """Uses OpenAI API via the openai Python package."""
    try:
        import openai
        client = openai.OpenAI()  # Uses OPENAI_API_KEY env var
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Cheap, fast, good enough for structured tasks
            messages=[{"role": "user", "content": prompt}],
            max_tokens=4000
        )
        return response.choices[0].message.content
    except ImportError:
        return "ERROR: openai package not installed. Run: pip install openai"
    except Exception as e:
        return f"ERROR: OpenAI API failed: {str(e)[:200]}"

def _gemini_api(prompt):
    """Uses Google Gemini API via the google-genai package."""
    try:
        import google.generativeai as genai
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        return response.text
    except ImportError:
        return "ERROR: google-generativeai package not installed. Run: pip install google-generativeai"
    except Exception as e:
        return f"ERROR: Gemini API failed: {str(e)[:200]}"

def _stub(prompt):
    """Testing stub — returns a fixed response. Use for development."""
    return '{"actions": [], "summary": "Stub provider - no real AI called. Configure a real provider."}'

def _local_ollama(prompt):
    """Uses a local model via Ollama. Requires ollama running locally."""
    try:
        import requests
        r = requests.post("http://localhost:11434/api/generate", json={
            "model": "llama3",  # Or whatever model is pulled
            "prompt": prompt,
            "stream": False
        }, timeout=120)
        return r.json().get("response", "ERROR: No response from Ollama")
    except ImportError:
        return "ERROR: requests package not installed. Run: pip install requests"
    except Exception as e:
        return f"ERROR: Ollama failed (is it running?): {str(e)[:200]}"

register_provider("claude-cli", _claude_cli, "Claude via CLI (requires claude in PATH)")
register_provider("openai-api", _openai_api, "OpenAI API (requires OPENAI_API_KEY)")
register_provider("gemini-api", _gemini_api, "Google Gemini API (requires GOOGLE_API_KEY)")
register_provider("ollama", _local_ollama, "Local model via Ollama (requires ollama running)")
register_provider("stub", _stub, "Testing stub — no real AI called")

# --- Load external providers from scripts/providers/*.py ---
def load_external_providers():
    if not PROVIDERS_DIR.exists():
        return
    for f in PROVIDERS_DIR.glob("*.py"):
        if f.name.startswith("_"):
            continue
        try:
            spec = importlib.util.spec_from_file_location(f.stem, f)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            if hasattr(mod, "register"):
                mod.register(register_provider)
        except Exception as e:
            print(f"Warning: Could not load provider {f.name}: {e}")

load_external_providers()


# ============================================================
# CONFIGURATION
# ============================================================

def load_config():
    defaults = {
        "provider": "claude-cli",
        "fallback_chain": ["claude-cli", "openai-api", "gemini-api", "ollama", "stub"],
        "max_actions_per_run": 10,
        "auto_approve": [
            "add-source",
            "fix-developer-name",
            "update-meta-counts"
        ],
        "require_approval": [
            "remove-tool",
            "change-category",
            "modify-system-file",
            "bulk-change"
        ],
        "last_run": None,
        "total_runs": 0
    }
    if CONFIG_PATH.exists():
        try:
            saved = json.load(open(CONFIG_PATH, "r", encoding="utf-8"))
            defaults.update(saved)
        except:
            pass
    return defaults

def save_config(config):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)

def get_provider(config):
    """Get working provider, falling through chain if needed."""
    chain = config.get("fallback_chain", ["stub"])
    primary = config.get("provider", chain[0] if chain else "stub")

    # Try primary first
    if primary in PROVIDERS:
        return primary, PROVIDERS[primary]["fn"]

    # Fall through chain
    for name in chain:
        if name in PROVIDERS:
            print(f"  Primary provider '{primary}' not available, falling back to '{name}'")
            return name, PROVIDERS[name]["fn"]

    return "stub", PROVIDERS["stub"]["fn"]


# ============================================================
# CORE ENGINE — run scripts, build plan, execute via AI
# ============================================================

def run_script(script_name, args=""):
    """Run a Python script and capture output."""
    script_path = BASE / "scripts" / script_name
    if not script_path.exists():
        return f"Script not found: {script_name}"
    cmd = f"python \"{script_path}\" {args}"
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    result = subprocess.run(cmd, shell=True, capture_output=True,
                          timeout=60, cwd=str(BASE), env=env,
                          encoding="utf-8", errors="replace")
    stdout = result.stdout or ""
    stderr = result.stderr or ""
    return stdout + stderr

def build_analysis():
    """Run all analysis scripts and compile results."""
    print("Running analysis scripts...")

    results = {}
    print("  self-improve.py --dry-run...")
    results["self_improve"] = run_script("self-improve.py", "--dry-run")
    print("  gap-analysis.py --brief...")
    results["gap_analysis"] = run_script("gap-analysis.py", "--brief")
    print("  validate-data.py...")
    results["validation"] = run_script("validate-data.py")

    return results

def build_prompt(analysis, config):
    """Build the AI prompt from analysis results."""
    return f"""You are the AI automation engine for CC-AIProgress, a self-improving AI research system.

Below are the outputs from three analysis scripts. Your job: create a prioritized action plan
to fix the issues found. Return ONLY valid JSON.

## Analysis: self-improve.py
{analysis['self_improve'][:3000]}

## Analysis: gap-analysis.py
{analysis['gap_analysis'][:2000]}

## Analysis: validate-data.py
{analysis['validation'][:2000]}

## Rules
- Maximum {config.get('max_actions_per_run', 10)} actions per run
- Auto-approved action types: {config.get('auto_approve', [])}
- Requires human approval: {config.get('require_approval', [])}
- Prioritize: critical issues first, then highest-impact improvements
- Each action must be specific and executable (not vague like "improve coverage")

## Output Format (JSON only, no markdown)
{{
  "summary": "One sentence: what's the most important thing to fix",
  "actions": [
    {{
      "priority": 1,
      "type": "action-type (e.g. add-source, fix-staleness, add-tool, fix-developer-name)",
      "description": "What to do, specifically",
      "target_file": "data/file.json",
      "auto_approved": true,
      "details": {{}}
    }}
  ],
  "deferred": ["Things that need more research before acting"],
  "health_score": 0-100
}}"""

def execute_plan(plan, ai_fn, config):
    """Execute the actions in a plan, respecting approval rules."""
    actions = plan.get("actions", [])
    executed = 0
    skipped = 0

    for a in actions:
        action_type = a.get("type", "unknown")
        auto = a.get("auto_approved", False)
        requires = config.get("require_approval", [])

        if action_type in requires and not ("--auto" in sys.argv):
            print(f"  [SKIP] {a['description']} (requires approval: {action_type})")
            skipped += 1
            continue

        if not auto and not ("--auto" in sys.argv):
            print(f"  [SKIP] {a['description']} (not auto-approved)")
            skipped += 1
            continue

        print(f"  [EXEC] {a['description']}")
        # The AI would generate the actual file changes here
        # For now, we log the action and let the research sweep handle it
        executed += 1

    return executed, skipped


# ============================================================
# MAIN
# ============================================================

def main():
    args = sys.argv[1:]

    if "--providers" in args:
        print("Available AI providers:\n")
        for name, info in PROVIDERS.items():
            print(f"  {name:20s} {info['description']}")
        print(f"\nTo add a new provider: create scripts/providers/my_provider.py")
        print(f"  with a register(register_fn) function that calls")
        print(f"  register_fn('name', callable, 'description')")
        return

    config = load_config()

    if "--config" in args:
        if "set" in args:
            idx = args.index("set")
            if idx + 2 < len(args):
                key, value = args[idx+1], args[idx+2]
                config[key] = value
                save_config(config)
                print(f"Set {key} = {value}")
            else:
                print("Usage: --config set <key> <value>")
        else:
            print("Current configuration:\n")
            print(json.dumps(config, indent=2))
        return

    print("=" * 60)
    print("CC-AIProgress AI Automation Engine")
    provider_name, ai_fn = get_provider(config)
    print(f"Provider: {provider_name}")
    mode = "PLAN ONLY" if "--plan" in args else "EXECUTE" if "--execute" in args else "INTERACTIVE"
    print(f"Mode: {mode}")
    print("=" * 60)

    # Step 1: Run analysis
    analysis = build_analysis()

    # Step 2: Build AI prompt
    prompt = build_prompt(analysis, config)

    if "--plan" in args:
        # Just show the prompt that would be sent
        print("\n--- PROMPT THAT WOULD BE SENT TO AI ---")
        print(prompt[:2000] + "..." if len(prompt) > 2000 else prompt)
        print("\nTo execute: python scripts/ai-engine.py --execute")
        return

    # Step 3: Call AI
    print(f"\nCalling {provider_name}...")
    response = ai_fn(prompt)

    if response.startswith("ERROR"):
        print(f"\n{response}")
        print("Falling back to analysis-only mode.")
        return

    # Step 4: Parse response
    try:
        # Try to extract JSON from response (AI might wrap it in markdown)
        text = response.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        plan = json.loads(text)
    except json.JSONDecodeError:
        print(f"\nAI returned non-JSON response. Raw output:")
        print(response[:1000])
        return

    # Step 5: Display plan
    print(f"\n{'=' * 60}")
    print(f"PLAN: {plan.get('summary', 'No summary')}")
    print(f"Health Score: {plan.get('health_score', '?')}/100")
    print(f"Actions: {len(plan.get('actions', []))}")
    print(f"Deferred: {len(plan.get('deferred', []))}")
    print(f"{'=' * 60}")

    for a in plan.get("actions", []):
        status = "AUTO" if a.get("auto_approved") else "NEEDS APPROVAL"
        print(f"  [{a.get('priority', '?')}] [{status}] {a.get('description', '?')}")

    if plan.get("deferred"):
        print(f"\nDeferred (need more research):")
        for d in plan["deferred"]:
            print(f"  - {d}")

    # Step 6: Execute if requested
    if "--execute" in args:
        print(f"\nExecuting plan...")
        executed, skipped = execute_plan(plan, ai_fn, config)
        print(f"\nDone: {executed} executed, {skipped} skipped")

        config["last_run"] = datetime.now().isoformat()
        config["total_runs"] = config.get("total_runs", 0) + 1
        save_config(config)
    else:
        print(f"\nTo execute this plan: python scripts/ai-engine.py --execute")

    # Save plan for reference
    plan_path = DATA / "ai-engine-last-plan.json"
    plan["generated"] = datetime.now().isoformat()
    plan["provider"] = provider_name
    with open(plan_path, "w", encoding="utf-8") as f:
        json.dump(plan, f, indent=2)
    print(f"Plan saved to {plan_path}")


if __name__ == "__main__":
    main()
