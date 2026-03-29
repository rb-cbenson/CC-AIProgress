#!/usr/bin/env python3
"""Add user-found tools + discovery sources."""
import json, sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

tools = json.load(open('data/tools.json', 'r', encoding='utf-8'))
existing = {t['id'] for t in tools}
sources = json.load(open('data/news-sources.json', 'r', encoding='utf-8'))
source_ids = {s['id'] for s in sources}

new_tools = [
    {
        "id": "lindy-ai", "name": "Lindy.ai", "category": "ai-agents",
        "developer": "Lindy", "url": "https://www.lindy.ai/",
        "description": "No-code AI agent builder. Create agents for email triage, meeting scheduling, customer support, sales outreach. Connects to 3,000+ apps.",
        "pricingCAD": {"freeTier": True, "freeTierDetails": "Free tier with limited agent runs",
            "freeTierLimits": {"notes": "Free tier available with limits"}, "paidPlans": [{"name": "Pro", "priceCAD": 70, "period": "month", "details": "Unlimited agents and runs"}]},
        "capabilities": ["automation", "text-generation", "api-call"], "integrations": ["zapier", "n8n"],
        "accessMethod": "web", "platformSupport": ["web"],
        "ranking": {"overall": 65, "inCategory": 5, "trend": "rising"},
        "pros": ["No-code agent builder", "3000+ app integrations", "Pre-built templates"],
        "cons": ["Pro plan expensive", "Web-only"],
        "trustScore": 68, "firstTracked": "2026-03-28", "lastVerified": "2026-03-28"
    },
    {
        "id": "play-ht", "name": "Play.ht", "category": "speech-voice",
        "developer": "PlayHT", "url": "https://play.ht/",
        "description": "AI voice generator and text-to-speech. Ultra-realistic voices, voice cloning, API access. Podcasts, audiobooks, content creation.",
        "pricingCAD": {"freeTier": True, "freeTierDetails": "Free tier with limited characters/month",
            "freeTierLimits": {"notes": "Limited characters per month"}, "paidPlans": [{"name": "Creator", "priceCAD": 43, "period": "month", "details": "Unlimited words, commercial license"}]},
        "capabilities": ["speech-synthesis", "audio-generation", "api-call"], "integrations": [],
        "accessMethod": "web+api", "platformSupport": ["web", "api"],
        "ranking": {"overall": 60, "inCategory": 3, "trend": "stable"},
        "pros": ["Ultra-realistic voices", "Voice cloning", "API access"],
        "cons": ["Free tier limited", "Competes with ElevenLabs"],
        "trustScore": 70, "firstTracked": "2026-03-28", "lastVerified": "2026-03-28"
    },
    {
        "id": "copy-ai", "name": "Copy.ai", "category": "productivity",
        "developer": "Copy.ai", "url": "https://www.copy.ai/",
        "description": "AI copywriting and content platform. Marketing copy, blog posts, social media, emails. GTM AI workflows for sales teams.",
        "pricingCAD": {"freeTier": True, "freeTierDetails": "2,000 words/month free",
            "freeTierLimits": {"notes": "2,000 words/month renewable"}, "paidPlans": [{"name": "Starter", "priceCAD": 50, "period": "month", "details": "Unlimited words"}]},
        "capabilities": ["text-generation", "text-editing", "summarization"], "integrations": ["zapier"],
        "accessMethod": "web", "platformSupport": ["web"],
        "ranking": {"overall": 62, "inCategory": 8, "trend": "stable"},
        "pros": ["Purpose-built for marketing copy", "2000 free words/month renewable", "GTM templates"],
        "cons": ["Not general-purpose AI", "Web-only", "Expensive for unlimited"],
        "trustScore": 72, "firstTracked": "2026-03-28", "lastVerified": "2026-03-28"
    },
    {
        "id": "intercom-fin", "name": "Intercom Fin", "category": "ai-agents",
        "developer": "Intercom", "url": "https://www.intercom.com/",
        "description": "AI customer support agent. Resolves tickets autonomously using your knowledge base. Hands off to humans when needed.",
        "pricingCAD": {"freeTier": True, "freeTierDetails": "14-day free trial",
            "freeTierLimits": {"notes": "14-day trial only. No ongoing free tier."},
            "paidPlans": [{"name": "Essential", "priceCAD": 42, "period": "month", "details": "Per seat + $0.99/resolution"}]},
        "capabilities": ["text-generation", "text-analysis", "automation", "api-call"], "integrations": ["zapier", "n8n"],
        "accessMethod": "web+api", "platformSupport": ["web", "api"],
        "ranking": {"overall": 55, "inCategory": 4, "trend": "rising"},
        "pros": ["Autonomous ticket resolution", "Uses your knowledge base", "Enterprise-grade"],
        "cons": ["Expensive per-seat + per-resolution", "Trial only, no free tier", "Support niche"],
        "trustScore": 80, "firstTracked": "2026-03-28", "lastVerified": "2026-03-28"
    }
]

new_sources = [
    {"id": "theresanaiforthat", "name": "There Is An AI For That (TAAFT)", "type": "directory",
     "url": "https://theresanaiforthat.com/", "frequency": "Daily updates",
     "description": "The #1 AI tool discovery site. Task-based search across thousands of tools.",
     "free": True, "tags": ["directory", "discovery", "comprehensive"]},
    {"id": "topai-tools", "name": "TopAI.tools", "type": "directory",
     "url": "https://topai.tools/", "frequency": "Daily updates",
     "description": "22,290+ AI tools across 120+ categories. Largest curated directory. Top 100 ranking and free tool filtering.",
     "free": True, "tags": ["directory", "discovery", "largest", "rankings"]},
    {"id": "futurepedia", "name": "Futurepedia", "type": "directory",
     "url": "https://www.futurepedia.io/", "frequency": "Regular updates",
     "description": "~5,700 tools in 50+ categories. Community engagement, guides, tutorials.",
     "free": True, "tags": ["directory", "discovery", "guides"]},
    {"id": "futuretools", "name": "FutureTools (Matt Wolfe)", "type": "directory",
     "url": "https://futuretools.io/", "frequency": "Regular updates",
     "description": "4,000+ tools in 29 categories. Curated by Matt Wolfe (230K+ YouTube).",
     "free": True, "tags": ["directory", "discovery", "curated"]},
    {"id": "product-hunt-ai", "name": "Product Hunt AI Category", "type": "directory",
     "url": "https://www.producthunt.com/topics/artificial-intelligence", "frequency": "Daily launches",
     "description": "Daily new AI product launches with community voting. Catches tools at launch.",
     "free": True, "tags": ["directory", "launches", "early-signal"]},
    {"id": "r-locallama", "name": "r/LocalLLaMA", "type": "reddit",
     "url": "https://www.reddit.com/r/LocalLLaMA/", "frequency": "Hourly",
     "description": "Builder community for local AI. Monthly threads on what people use. High signal.",
     "free": True, "tags": ["reddit", "community", "local-ai"]},
    {"id": "r-aivideo", "name": "r/aivideo", "type": "reddit",
     "url": "https://www.reddit.com/r/aivideo/", "frequency": "Daily",
     "description": "AI video generation community. Tool comparisons, workflow sharing.",
     "free": True, "tags": ["reddit", "community", "video-generation"]},
    {"id": "r-aiagents", "name": "r/AI_Agents", "type": "reddit",
     "url": "https://www.reddit.com/r/AI_Agents/", "frequency": "Daily",
     "description": "AI agent community. Autonomous agents, tool use, multi-step workflows.",
     "free": True, "tags": ["reddit", "community", "ai-agents"]}
]

added_tools = 0
for nt in new_tools:
    if nt["id"] not in existing:
        tools.append(nt)
        added_tools += 1
        print(f"  Tool: {nt['id']}")

added_sources = 0
for ns in new_sources:
    if ns["id"] not in source_ids:
        sources.append(ns)
        added_sources += 1
        print(f"  Source: {ns['id']}")

with open('data/tools.json', 'w', encoding='utf-8') as f:
    json.dump(tools, f, indent=2, ensure_ascii=False)
with open('data/news-sources.json', 'w', encoding='utf-8') as f:
    json.dump(sources, f, indent=2, ensure_ascii=False)

meta = json.load(open('data/meta.json', 'r', encoding='utf-8'))
meta['totalTools'] = len(tools)
with open('data/meta.json', 'w', encoding='utf-8') as f:
    json.dump(meta, f, indent=2, ensure_ascii=False)

print(f"\n+{added_tools} tools, +{added_sources} sources. Total: {len(tools)} tools, {len(sources)} sources.")
