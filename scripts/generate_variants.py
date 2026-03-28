#!/usr/bin/env python3
"""Generate workflow pipeline variants using Groq."""
import json, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from pathlib import Path
from env_loader import load_env
load_env(Path(__file__).parent.parent / '.env')

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from groq import Groq

tools = json.load(open('data/tools.json', 'r', encoding='utf-8'))
credit_tracker = json.load(open('data/credit-tracker.json', 'r', encoding='utf-8'))

safe_tools = sorted(set(credit_tracker['safeToTestNow'] + credit_tracker['unlimitedFreeTools']))

tool_summary = []
for t in tools:
    caps = ', '.join(t.get('capabilities', [])[:3])
    free = 'FREE' if t.get('pricingCAD', {}).get('freeTier') else 'PAID'
    access = t.get('accessMethod', '?')
    tool_summary.append(f"{t['id']}: {t['name']} [{caps}] ({free}, {access})")

tool_text = '\n'.join(tool_summary[:80])

prompt = (
    "Generate alternative pipeline variants for 8 AI workflow types. "
    "For each type, create exactly 3 variants:\n"
    "1. FREE-BEST: Best quality using only free/renewable-credit tools\n"
    "2. FREE-LOCAL: Fully local/offline using open-source tools only\n"
    "3. PAID-PREMIUM: Best possible quality regardless of cost\n\n"
    f"Available tools:\n{tool_text}\n\n"
    f"Tools safe to test: {', '.join(safe_tools[:40])}\n\n"
    "Workflow types:\n"
    "1. short-video: Short-form video production (TikTok/Reels)\n"
    "2. coding: AI-assisted coding (multi-model)\n"
    "3. research: Research & knowledge synthesis\n"
    "4. robotics-sim: Robotics sim-to-real\n"
    "5. pcb-design: PCB design & manufacturing\n"
    "6. music: Music production\n"
    "7. prototype: Product prototype (idea to physical object)\n"
    "8. content: Content creation (blog/social)\n\n"
    "Return ONLY valid JSON array. Each item:\n"
    '[\n'
    '  {\n'
    '    "workflowType": "short-video",\n'
    '    "variants": [\n'
    '      {\n'
    '        "variantId": "short-video-free-best",\n'
    '        "name": "Free Best Quality",\n'
    '        "tier": "free-best",\n'
    '        "steps": [\n'
    '          {"order": 1, "toolId": "groq", "action": "Generate script", "free": true}\n'
    '        ],\n'
    '        "estimatedCost": "$0",\n'
    '        "pros": ["All free"],\n'
    '        "cons": ["Lower quality than paid"],\n'
    '        "testable": true\n'
    '      }\n'
    '    ]\n'
    '  }\n'
    ']\n\n'
    "IMPORTANT: Use actual tool IDs from the list above. "
    "Each variant should have 3-6 steps. "
    "FREE-LOCAL variants must use only tools that run locally (ollama, stable-diffusion, blender, kicad, etc). "
    "PAID-PREMIUM should use the highest quality tools regardless of cost."
)

client = Groq(api_key=os.environ['GROQ_API_KEY'])
response = client.chat.completions.create(
    model='llama-3.3-70b-versatile',
    messages=[{'role': 'user', 'content': prompt}],
    max_tokens=8000,
    temperature=0.3
)

result = response.choices[0].message.content.strip()

# Extract JSON from response
if '```' in result:
    parts = result.split('```')
    for p in parts:
        p = p.strip()
        if p.startswith('json'):
            p = p[4:].strip()
        if p.startswith('['):
            result = p
            break

try:
    variants = json.loads(result)
    print(f"Generated {len(variants)} workflow types with variants")
    for v in variants:
        vcount = len(v.get('variants', []))
        print(f"  {v['workflowType']}: {vcount} variants")

    with open('data/workflow-variants.json', 'w', encoding='utf-8') as f:
        json.dump(variants, f, indent=2, ensure_ascii=False)
    print(f"\nSaved to data/workflow-variants.json")
except json.JSONDecodeError as e:
    print(f"JSON parse error: {e}")
    print(f"Raw (first 500): {result[:500]}")
    with open('data/workflow-variants-raw.txt', 'w', encoding='utf-8') as f:
        f.write(result)
    print("Raw output saved to data/workflow-variants-raw.txt")
