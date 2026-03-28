#!/usr/bin/env python3
"""
CC-AIProgress Research Sweep — End-to-end automated research

Runs search.py to gather web results, then sends them to an AI for
analysis and briefing generation. No Claude session needed.

Pipeline: search.py (free) → AI analysis (Groq/Mistral/OpenRouter free) → briefings.json

Usage:
    python scripts/research-sweep.py                    # Full sweep
    python scripts/research-sweep.py --search-only      # Just run searches, skip AI
    python scripts/research-sweep.py --analyze-only     # Just analyze existing cache
    python scripts/research-sweep.py --provider groq    # Force specific AI provider
    python scripts/research-sweep.py --dry-run          # Show what would happen

Env vars needed:
    TAVILY_API_KEY (or falls back to DDG/RSS)
    GROQ_API_KEY (or MISTRAL_API_KEY, or OPENROUTER_API_KEY)
"""

import json, sys, os, subprocess
from datetime import datetime
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE = Path(__file__).resolve().parent.parent

# Load API keys from .env
sys.path.insert(0, str(BASE / "scripts"))
from env_loader import load_env
load_env()
DATA = BASE / "data"
CACHE_PATH = DATA / "search-cache.json"

DRY_RUN = "--dry-run" in sys.argv
SEARCH_ONLY = "--search-only" in sys.argv
ANALYZE_ONLY = "--analyze-only" in sys.argv

# ============================================================
# AI PROVIDERS — each takes a prompt, returns text
# ============================================================

def call_groq(prompt):
    api_key = os.environ.get("GROQ_API_KEY", "")
    if not api_key:
        return None, "No GROQ_API_KEY"
    try:
        from groq import Groq
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=4000,
            temperature=0.3
        )
        return response.choices[0].message.content, None
    except Exception as e:
        return None, f"Groq error: {str(e)[:200]}"

def call_mistral(prompt):
    api_key = os.environ.get("MISTRAL_API_KEY", "")
    if not api_key:
        return None, "No MISTRAL_API_KEY"
    try:
        from openai import OpenAI
        client = OpenAI(base_url="https://api.mistral.ai/v1", api_key=api_key)
        response = client.chat.completions.create(
            model="mistral-small-latest",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=4000,
            temperature=0.3
        )
        return response.choices[0].message.content, None
    except Exception as e:
        return None, f"Mistral error: {str(e)[:200]}"

def call_openrouter(prompt):
    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    if not api_key:
        return None, "No OPENROUTER_API_KEY"
    try:
        from openai import OpenAI
        client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)
        response = client.chat.completions.create(
            model="nvidia/nemotron-3-super-120b-a12b:free",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=4000,
            temperature=0.3
        )
        return response.choices[0].message.content, None
    except Exception as e:
        return None, f"OpenRouter error: {str(e)[:200]}"

AI_PROVIDERS = [
    ("groq", call_groq),
    ("mistral", call_mistral),
    ("openrouter", call_openrouter),
]

def call_ai(prompt, force_provider=None):
    """Call an AI with automatic fallback."""
    if force_provider:
        for name, fn in AI_PROVIDERS:
            if name == force_provider:
                result, error = fn(prompt)
                if result:
                    return result, name, None
                return None, name, error
        return None, force_provider, f"Unknown provider: {force_provider}"

    for name, fn in AI_PROVIDERS:
        result, error = fn(prompt)
        if result:
            return result, name, None
        print(f"  [{name}] failed: {error} — trying next...")

    return None, "none", "All AI providers failed"


# ============================================================
# STEP 1: RUN SEARCH
# ============================================================

def run_search():
    """Run search.py and return cached results."""
    print("Step 1: Running search queries...")
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    result = subprocess.run(
        [sys.executable, str(BASE / "scripts" / "search.py")],
        capture_output=True, encoding="utf-8", errors="replace",
        timeout=120, cwd=str(BASE), env=env
    )
    print(result.stdout)
    if result.stderr:
        print(result.stderr)

    if CACHE_PATH.exists():
        return json.load(open(CACHE_PATH, "r", encoding="utf-8"))
    return None


def load_cache():
    """Load existing search cache."""
    if CACHE_PATH.exists():
        cache = json.load(open(CACHE_PATH, "r", encoding="utf-8"))
        age_hours = 0
        try:
            gen = datetime.fromisoformat(cache["generated"])
            age_hours = (datetime.now() - gen).total_seconds() / 3600
        except:
            pass
        print(f"  Cache loaded: {cache.get('total_results', 0)} results, {age_hours:.1f} hours old")
        if age_hours > 24:
            print(f"  WARNING: Cache is {age_hours:.0f} hours old. Consider running with fresh search.")
        return cache
    return None


# ============================================================
# STEP 2: BUILD AI PROMPT
# ============================================================

def build_analysis_prompt(search_results, last_briefing_date):
    """Build the prompt for AI analysis of search results."""

    # Compile search results into a compact format
    findings = []
    for q in search_results.get("queries", []):
        query = q["query"]
        for r in q.get("results", []):
            findings.append(f"[{query}] {r['title']} — {r['snippet'][:200]}")

    findings_text = "\n".join(findings[:80])  # Cap to stay within context

    return f"""You are an AI research analyst for an AI tool tracking system. Analyze these search results and produce a structured intelligence briefing.

The last briefing was on {last_briefing_date}. Only include developments AFTER that date.

## Search Results
{findings_text}

## Output Instructions
Return ONLY valid JSON matching this exact schema:
{{
  "id": "briefing-{datetime.now().strftime('%Y-%m-%d')}",
  "date": "{datetime.now().strftime('%Y-%m-%d')}",
  "type": "daily",
  "title": "Descriptive title — lead with the biggest finding",
  "summary": "2-3 sentence executive summary. Be specific.",
  "sections": [
    {{
      "heading": "Section title",
      "content": "3-5 sentences of analysis. What happened, why it matters, what to do about it.",
      "impact": "high|medium|low",
      "affectedTools": [],
      "affectedProjects": [],
      "actionItems": ["Specific next steps"]
    }}
  ],
  "toolUpdates": [
    {{
      "toolId": "tool-id-kebab-case",
      "change": "What changed",
      "verified": true
    }}
  ],
  "newDiscoveries": [
    {{
      "name": "Tool name",
      "url": "URL",
      "category": "category-id",
      "why": "Why it matters"
    }}
  ],
  "generatedBy": "research-sweep-automated"
}}

Rules:
- Only include genuinely significant developments, not noise
- Use kebab-case tool IDs (e.g., "chatgpt", "claude", "runway")
- If nothing significant happened, return type "daily" with empty sections
- Maximum 5 sections, ordered by impact
- Every claim must come from the search results — never fabricate
- Be concise — this is a briefing, not an essay"""


# ============================================================
# STEP 3: PARSE AND SAVE BRIEFING
# ============================================================

def parse_briefing(ai_response):
    """Extract JSON briefing from AI response."""
    text = ai_response.strip()

    # Handle markdown-wrapped JSON
    if "```" in text:
        parts = text.split("```")
        for part in parts:
            part = part.strip()
            if part.startswith("json"):
                part = part[4:].strip()
            if part.startswith("{"):
                try:
                    return json.loads(part), None
                except:
                    continue

    # Try direct parse
    try:
        return json.loads(text), None
    except json.JSONDecodeError as e:
        # Try to find JSON object in the text
        start = text.find("{")
        end = text.rfind("}") + 1
        if start >= 0 and end > start:
            try:
                return json.loads(text[start:end]), None
            except:
                pass
        return None, f"Could not parse JSON: {str(e)[:100]}"


def save_briefing(briefing):
    """Append briefing to briefings.json."""
    briefings_path = DATA / "briefings.json"
    briefings = []
    if briefings_path.exists():
        try:
            briefings = json.load(open(briefings_path, "r", encoding="utf-8"))
        except:
            pass

    # Check for duplicate date
    existing_dates = {b.get("date") for b in briefings}
    if briefing.get("date") in existing_dates:
        briefing["id"] = briefing.get("id", "") + "-v2"
        print(f"  Note: briefing for this date already exists, saving as {briefing['id']}")

    briefings.append(briefing)

    with open(briefings_path, "w", encoding="utf-8") as f:
        json.dump(briefings, f, indent=2, ensure_ascii=False)

    return len(briefings)


def update_meta():
    """Update meta.json lastUpdated."""
    meta_path = DATA / "meta.json"
    if meta_path.exists():
        meta = json.load(open(meta_path, "r", encoding="utf-8"))
        meta["lastUpdated"] = datetime.now().strftime("%Y-%m-%d")
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2, ensure_ascii=False)


# ============================================================
# MAIN
# ============================================================

def main():
    force_provider = None
    if "--provider" in sys.argv:
        idx = sys.argv.index("--provider")
        if idx + 1 < len(sys.argv):
            force_provider = sys.argv[idx + 1]

    print("=" * 60)
    print("CC-AIProgress Automated Research Sweep")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    if DRY_RUN:
        print("MODE: DRY RUN — no files will be modified")
    print("=" * 60)

    # Step 1: Search
    if ANALYZE_ONLY:
        cache = load_cache()
    else:
        if DRY_RUN:
            print("\nStep 1: Would run 12 search queries via search.py")
            cache = load_cache()
        else:
            cache = run_search()

    if not cache:
        print("ERROR: No search results available. Run without --analyze-only.")
        return 1

    if SEARCH_ONLY:
        print("\nSearch complete. Use --analyze-only to generate briefing from cache.")
        return 0

    # Get last briefing date
    briefings_path = DATA / "briefings.json"
    last_date = "2026-03-01"
    if briefings_path.exists():
        try:
            briefings = json.load(open(briefings_path, "r", encoding="utf-8"))
            dates = [b.get("date", "") for b in briefings]
            if dates:
                last_date = max(dates)
        except:
            pass
    print(f"\nLast briefing: {last_date}")

    # Step 2: AI Analysis
    print(f"\nStep 2: AI analysis...")
    prompt = build_analysis_prompt(cache, last_date)
    print(f"  Prompt: {len(prompt)} chars, {len(cache.get('queries', []))} queries, {cache.get('total_results', 0)} results")

    if DRY_RUN:
        print(f"  Would send to: {force_provider or 'groq → mistral → openrouter'}")
        print(f"\n  Prompt preview:\n{prompt[:500]}...")
        return 0

    response, provider, error = call_ai(prompt, force_provider)
    if not response:
        print(f"  ERROR: {error}")
        print("  All AI providers failed. Search results are cached — retry later or analyze manually.")
        return 1

    print(f"  Provider: {provider}")

    # Step 3: Parse and save
    print(f"\nStep 3: Parsing briefing...")
    briefing, parse_error = parse_briefing(response)
    if not briefing:
        print(f"  ERROR: {parse_error}")
        print(f"  Raw response saved to data/research-sweep-raw.json")
        with open(DATA / "research-sweep-raw.json", "w", encoding="utf-8") as f:
            json.dump({"response": response, "provider": provider, "timestamp": datetime.now().isoformat()}, f, indent=2)
        return 1

    # Add metadata
    briefing["generatedBy"] = f"research-sweep-{provider}"
    briefing["searchProvider"] = cache.get("providers_used", ["unknown"])[0]

    print(f"  Title: {briefing.get('title', 'No title')}")
    print(f"  Sections: {len(briefing.get('sections', []))}")
    print(f"  Tool updates: {len(briefing.get('toolUpdates', []))}")
    print(f"  New discoveries: {len(briefing.get('newDiscoveries', []))}")

    # Save
    total = save_briefing(briefing)
    update_meta()
    print(f"\nBriefing saved. Total briefings: {total}")
    print(f"View in dashboard: Command Center tab")

    return 0


if __name__ == "__main__":
    code = main()
    sys.exit(code)
