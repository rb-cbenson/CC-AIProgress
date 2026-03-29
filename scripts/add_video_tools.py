#!/usr/bin/env python3
"""Add missing video generation tools found via Reddit gap."""
import json, sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

tools = json.load(open('data/tools.json', 'r', encoding='utf-8'))
existing = {t['id'] for t in tools}
sources = json.load(open('data/news-sources.json', 'r', encoding='utf-8'))

new_tools = [
    {
        "id": "hunyuan-video", "name": "Hunyuan Video", "category": "video-generation",
        "developer": "Tencent", "url": "https://www.hunyuanvideox.com/",
        "description": "Largest open-source video model (13B params). v1.5 runs on a single RTX 4090. Free online studio. API via fal.ai. High fidelity, no audio generation.",
        "pricingCAD": {"freeTier": True, "freeTierDetails": "Open-source, free online studio, API ~$0.075/sec via fal.ai",
            "freeTierLimits": {"requestsPerDay": "unlimited (self-hosted)", "notes": "Open-source. Self-host free. Cloud API is pay-per-second."}, "paidPlans": []},
        "capabilities": ["video-generation"], "integrations": [],
        "accessMethod": "web+api", "platformSupport": ["web", "api", "linux", "windows"],
        "ranking": {"overall": 55, "inCategory": 5, "trend": "rising"},
        "pros": ["Open-source, self-hostable", "Runs on consumer GPU (RTX 4090)", "Free online studio"],
        "cons": ["No audio generation", "Hardware-intensive for local use", "Chinese company — data policy concerns"],
        "trustScore": 68, "firstTracked": "2026-03-28", "lastVerified": "2026-03-28"
    },
    {
        "id": "ltx-video", "name": "LTX Studio / LTX-2", "category": "video-generation",
        "developer": "Lightricks", "url": "https://ltx.studio/",
        "description": "Open-source video model with native 4K + synchronized audio generation. Licensed training data (Getty/Shutterstock) = clean IP chain. Runs on 16GB consumer GPUs.",
        "pricingCAD": {"freeTier": True, "freeTierDetails": "800 one-time credits on LTX Studio. Model free for companies under $10M ARR.",
            "freeTierLimits": {"requestsPerDay": "credit-based", "notes": "800 one-time credits. Does not renew on free plan."},
            "paidPlans": [{"name": "Lite", "priceCAD": 22, "period": "month", "details": "8K credits"},
                {"name": "Standard", "priceCAD": 50, "period": "month", "details": "28K credits, Veo 2/Kling access"}]},
        "capabilities": ["video-generation", "audio-generation"], "integrations": [],
        "accessMethod": "web+api", "platformSupport": ["web", "api", "linux", "windows"],
        "ranking": {"overall": 52, "inCategory": 4, "trend": "rising"},
        "pros": ["Native 4K + audio generation", "Clean IP (licensed training data)", "Open-source model"],
        "cons": ["800 free credits don't renew", "Full studio features need paid plan"],
        "trustScore": 74, "firstTracked": "2026-03-28", "lastVerified": "2026-03-28"
    },
    {
        "id": "vadoo", "name": "Vadoo AI", "category": "video-generation",
        "developer": "Vadoo", "url": "https://www.vadoo.tv/",
        "description": "All-in-one short-form content factory: AI scriptwriting, text-to-video, captions, voiceovers, B-roll, SEO tools, auto-posting to TikTok/Reels/Shorts.",
        "pricingCAD": {"freeTier": True, "freeTierDetails": "20 videos/month, 200MB storage, max 1m30s per video",
            "freeTierLimits": {"requestsPerMonth": 20, "notes": "20 videos/month renewable. 200MB storage. 1m30s max per video."},
            "paidPlans": [{"name": "Starter", "priceCAD": 17, "period": "month", "details": "750 credits"}]},
        "capabilities": ["video-generation", "text-generation", "speech-synthesis"], "integrations": [],
        "accessMethod": "web", "platformSupport": ["web"],
        "ranking": {"overall": 70, "inCategory": 8, "trend": "rising"},
        "pros": ["20 free videos/month (renewable)", "Auto-posting to social platforms", "All-in-one: script + video + captions + voiceover"],
        "cons": ["Lower quality than Kling/Veo for cinematic content", "Web-only, no API"],
        "trustScore": 62, "firstTracked": "2026-03-28", "lastVerified": "2026-03-28"
    },
    {
        "id": "higgsfield", "name": "Higgsfield AI", "category": "video-generation",
        "developer": "Higgsfield", "url": "https://higgsfield.ai/",
        "description": "Multi-model video aggregator — 15+ models (Veo, Kling, Seedance) under one subscription with 70+ cinematic camera presets.",
        "pricingCAD": {"freeTier": True, "freeTierDetails": "Limited free plan",
            "freeTierLimits": {"requestsPerDay": "limited", "notes": "Limited free tier. Details unclear."},
            "paidPlans": [{"name": "Basic", "priceCAD": 13, "period": "month", "details": "150 credits, ~25 videos"}]},
        "capabilities": ["video-generation"], "integrations": ["kling", "veo"],
        "accessMethod": "web", "platformSupport": ["web"],
        "ranking": {"overall": 68, "inCategory": 7, "trend": "rising"},
        "pros": ["One subscription for 15+ models", "70+ camera presets", "Compare models side-by-side"],
        "cons": ["Free tier very limited", "Lower tiers restrict model access"],
        "trustScore": 60, "firstTracked": "2026-03-28", "lastVerified": "2026-03-28"
    },
    {
        "id": "seedance", "name": "Seedance", "category": "video-generation",
        "developer": "ByteDance", "url": "https://seed.bytedance.com/en/seedance",
        "description": "ByteDance's video AI. 2K resolution, 24fps, up to 15 seconds. Integrating into CapCut (rolling out, not US yet). Consumer access via Dreamina.",
        "pricingCAD": {"freeTier": True, "freeTierDetails": "~225 daily free tokens via Dreamina (~1-2 videos/day, watermarked)",
            "freeTierLimits": {"requestsPerDay": "1-2 videos", "notes": "225 daily tokens via Dreamina. Watermarked. Renews daily."},
            "paidPlans": [{"name": "Dreamina Paid", "priceCAD": 14, "period": "month", "details": "More tokens, no watermark"}]},
        "capabilities": ["video-generation"], "integrations": [],
        "accessMethod": "web+api", "platformSupport": ["web", "api"],
        "ranking": {"overall": 45, "inCategory": 3, "trend": "rising"},
        "pros": ["ByteDance scale and investment", "CapCut integration coming", "2K resolution, daily free credits"],
        "cons": ["Not available in US yet (CapCut integration)", "ByteDance data concerns", "Watermarked on free tier"],
        "trustScore": 65, "firstTracked": "2026-03-28", "lastVerified": "2026-03-28"
    },
    {
        "id": "pollo-ai", "name": "Pollo AI", "category": "video-generation",
        "developer": "Pollo", "url": "https://pollo.ai/",
        "description": "Multi-model video aggregator (Pollo 2.5, Kling, Veo, Seedance). Draft-then-finalize workflow for cost optimization.",
        "pricingCAD": {"freeTier": True, "freeTierDetails": "10 credits, 1 video, 10 images. No quality throttling on free tier.",
            "freeTierLimits": {"requestsPerMonth": 1, "notes": "10 credits = 1 video. Same quality as paid. Does not auto-renew."},
            "paidPlans": [{"name": "Lite", "priceCAD": 22, "period": "month", "details": "300 credits, 30 videos"}]},
        "capabilities": ["video-generation", "image-generation"], "integrations": ["kling", "veo", "seedance"],
        "accessMethod": "web", "platformSupport": ["web"],
        "ranking": {"overall": 72, "inCategory": 9, "trend": "stable"},
        "pros": ["Multiple models in one place", "Draft-then-finalize saves costs", "No quality throttling on free"],
        "cons": ["10 free credits likely one-time", "Web-only"],
        "trustScore": 58, "firstTracked": "2026-03-28", "lastVerified": "2026-03-28"
    },
    {
        "id": "a2e", "name": "A2E", "category": "video-generation",
        "developer": "A2E", "url": "https://a2e.ai/",
        "description": "Avatar and face pipeline — AI avatars, face swap, head swap, voice cloning (50+ languages), lip sync, talking photos.",
        "pricingCAD": {"freeTier": True, "freeTierDetails": "~30 daily credits (watermarked 720p, lower priority). 100 bonus credits for new users.",
            "freeTierLimits": {"requestsPerDay": 30, "notes": "30 daily credits renewable. Watermarked 720p. 100 bonus credits on signup."},
            "paidPlans": [{"name": "Pro", "priceCAD": 14, "period": "month", "details": "60 credits/day, 4K, no watermark, API"}]},
        "capabilities": ["video-generation", "speech-synthesis", "image-editing"], "integrations": [],
        "accessMethod": "web+api", "platformSupport": ["web", "api"],
        "ranking": {"overall": 75, "inCategory": 10, "trend": "stable"},
        "pros": ["Daily renewable credits", "50+ language voice cloning", "Face swap and lip sync"],
        "cons": ["Positions as 'uncensored' — trust/safety concerns", "Avatar niche, not cinematic video"],
        "trustScore": 52, "firstTracked": "2026-03-28", "lastVerified": "2026-03-28"
    },
    {
        "id": "hailuo", "name": "Hailuo AI", "category": "video-generation",
        "developer": "MiniMax", "url": "https://hailuoai.video/",
        "description": "Budget champion for AI video. MiniMax's consumer brand. Hailuo 2.3 set new cost-effectiveness record. 6-second 1080p clips with free tier.",
        "pricingCAD": {"freeTier": True, "freeTierDetails": "Free tier: 6-second 1080p watermarked videos, ~20-30 short clips, daily free credits during launch.",
            "freeTierLimits": {"requestsPerDay": "20-30 clips", "notes": "Daily free credits. Watermarked. 6-second 1080p."},
            "paidPlans": [{"name": "Standard", "priceCAD": 14, "period": "month", "details": "1000 credits, ~40 videos, no watermark"}]},
        "capabilities": ["video-generation"], "integrations": ["minimax-video"],
        "accessMethod": "web", "platformSupport": ["web"],
        "ranking": {"overall": 58, "inCategory": 6, "trend": "rising"},
        "pros": ["Best price/quality ratio in budget segment", "$0.25/clip on paid plan", "Daily renewable free credits"],
        "cons": ["6-second max on free tier", "MiniMax — smaller company", "Web-only"],
        "trustScore": 64, "firstTracked": "2026-03-28", "lastVerified": "2026-03-28"
    }
]

added = 0
for nt in new_tools:
    if nt["id"] not in existing:
        tools.append(nt)
        added += 1
        print(f"  Added: {nt['id']} ({nt['name']}) - {nt['developer']}")

# Add Arena.ai as a source, not a tool
sources.append({
    "id": "arena-ai-video",
    "name": "Arena.ai Video Leaderboard",
    "type": "benchmark",
    "url": "https://arena.ai/",
    "frequency": "Continuously updated",
    "description": "Crowdsourced blind-comparison ELO leaderboard for AI video models. 5M+ monthly users. Current T2V leader changes frequently. Essential for ranking video tools.",
    "free": True,
    "tags": ["benchmark", "leaderboard", "video-generation", "crowdsourced"]
})
print(f"  Added arena-ai-video to news-sources.json")

with open('data/tools.json', 'w', encoding='utf-8') as f:
    json.dump(tools, f, indent=2, ensure_ascii=False)
with open('data/news-sources.json', 'w', encoding='utf-8') as f:
    json.dump(sources, f, indent=2, ensure_ascii=False)

meta = json.load(open('data/meta.json', 'r', encoding='utf-8'))
meta['totalTools'] = len(tools)
with open('data/meta.json', 'w', encoding='utf-8') as f:
    json.dump(meta, f, indent=2, ensure_ascii=False)

print(f"\nAdded {added} video tools. Total: {len(tools)} tools, {len(sources)} sources.")
