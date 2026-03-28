#!/usr/bin/env python3
"""One-time: add missing tools discovered through orchestrator testing."""
import json, sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

tools = json.load(open('data/tools.json', 'r', encoding='utf-8'))
existing = {t['id'] for t in tools}

new_tools = [
    {
        "id": "kicad",
        "name": "KiCad",
        "category": "3d-cad",
        "developer": "KiCad Community",
        "url": "https://www.kicad.org/",
        "description": "Open-source electronics design suite: schematic capture, PCB layout, 3D viewer, Gerber export. Industry standard for open-source PCB design.",
        "pricingCAD": {"freeTier": True, "freeTierDetails": "Fully free and open source", "freeTierLimits": {"requestsPerDay": "unlimited", "notes": "Desktop app, no limits"}, "paidPlans": []},
        "capabilities": ["circuit-design", "pcb-layout", "3d-modeling", "simulation"],
        "integrations": ["jlcpcb-api", "freecad", "blender"],
        "accessMethod": "desktop-app",
        "platformSupport": ["windows", "mac", "linux"],
        "ranking": {"overall": 50, "inCategory": 3, "trend": "rising"},
        "pros": ["Fully free and open source", "Professional-grade PCB design", "JLCPCB integration"],
        "cons": ["Steeper learning curve than commercial tools", "No cloud collaboration"],
        "trustScore": 82,
        "firstTracked": "2026-03-28",
        "lastVerified": "2026-03-28"
    },
    {
        "id": "opencv",
        "name": "OpenCV",
        "category": "robotics-ai",
        "developer": "OpenCV Community",
        "url": "https://opencv.org/",
        "description": "Open-source computer vision library. Image processing, object detection, face recognition, optical flow. Foundation of most CV pipelines in robotics.",
        "pricingCAD": {"freeTier": True, "freeTierDetails": "Fully free and open source (Apache 2.0)", "freeTierLimits": {"requestsPerDay": "unlimited"}, "paidPlans": []},
        "capabilities": ["image-analysis", "sensor-processing", "code-execution"],
        "integrations": ["realsense", "luxonis-oak", "ros2-nav2", "jetson-orin"],
        "accessMethod": "cli",
        "platformSupport": ["windows", "mac", "linux"],
        "ranking": {"overall": 30, "inCategory": 2, "trend": "stable"},
        "pros": ["Industry standard for computer vision", "Runs on everything including embedded", "Massive documentation"],
        "cons": ["Traditional CV — not AI-native", "Python bindings can be slow"],
        "trustScore": 90,
        "firstTracked": "2026-03-28",
        "lastVerified": "2026-03-28"
    },
    {
        "id": "groq",
        "name": "Groq",
        "category": "text-chat",
        "developer": "Groq Inc.",
        "url": "https://groq.com/",
        "description": "Ultra-fast LLM inference on custom LPU hardware. Runs Llama, Mixtral at 10-100x speed of GPU inference. Free tier: 30 req/min, 14,400 req/day.",
        "pricingCAD": {"freeTier": True, "freeTierDetails": "30 req/min, 14,400 req/day free", "freeTierLimits": {"requestsPerDay": 14400, "requestsPerMinute": 30, "tokensPerMinute": 100000, "models": ["llama-3.3-70b-versatile", "mixtral-8x7b"]}, "paidPlans": []},
        "capabilities": ["text-generation", "text-analysis", "code-generation", "summarization", "translation", "api-call"],
        "integrations": ["openrouter"],
        "accessMethod": "api",
        "platformSupport": ["api", "web"],
        "ranking": {"overall": 15, "inCategory": 5, "trend": "rising"},
        "pros": ["Fastest inference available (0.07s for 70B)", "Generous free tier", "OpenAI-compatible API"],
        "cons": ["Only open-source models", "No image/audio", "Limited model selection"],
        "trustScore": 78,
        "firstTracked": "2026-03-28",
        "lastVerified": "2026-03-28"
    },
    {
        "id": "openrouter",
        "name": "OpenRouter",
        "category": "all-in-one",
        "developer": "OpenRouter",
        "url": "https://openrouter.ai/",
        "description": "Unified API for 300+ LLMs from all providers. One API key, OpenAI SDK compatible. Automatic fallbacks, price comparison, free models available.",
        "pricingCAD": {"freeTier": True, "freeTierDetails": "Free models available, pay-per-token for premium", "freeTierLimits": {"requestsPerDay": "varies by model"}, "paidPlans": []},
        "capabilities": ["text-generation", "text-analysis", "code-generation", "summarization", "translation", "api-call"],
        "integrations": ["groq", "claude-api", "openai-api", "gemini-api", "mistral"],
        "accessMethod": "api",
        "platformSupport": ["api", "web"],
        "ranking": {"overall": 12, "inCategory": 2, "trend": "rising"},
        "pros": ["One API for 300+ models", "Automatic fallback if provider down", "Free models available"],
        "cons": ["Adds latency vs direct", "Free models rate-limited"],
        "trustScore": 75,
        "firstTracked": "2026-03-28",
        "lastVerified": "2026-03-28"
    },
    {
        "id": "tavily",
        "name": "Tavily",
        "category": "data-analysis",
        "developer": "Tavily",
        "url": "https://tavily.com/",
        "description": "AI search API for agents. Real-time web search, content extraction, crawling. Returns structured results with relevance scores. 1000 free credits/month.",
        "pricingCAD": {"freeTier": True, "freeTierDetails": "1000 credits/month free (Researcher plan)", "freeTierLimits": {"requestsPerMonth": 1000, "notes": "Search=1 credit, Advanced=5"}, "paidPlans": [{"name": "Analyst", "priceCAD": 58, "period": "month", "details": "10,000 credits/month"}]},
        "capabilities": ["web-search", "web-scraping", "data-analysis", "api-call"],
        "integrations": ["claude-api", "openai-api", "groq"],
        "accessMethod": "api",
        "platformSupport": ["api"],
        "ranking": {"overall": 20, "inCategory": 3, "trend": "rising"},
        "pros": ["Purpose-built for AI agents", "Structured results with scores", "Generous free tier"],
        "cons": ["1000 credits goes fast with daily use", "Text extraction only — no rendering"],
        "trustScore": 72,
        "firstTracked": "2026-03-28",
        "lastVerified": "2026-03-28"
    },
    {
        "id": "mistral",
        "name": "Mistral AI",
        "category": "text-chat",
        "developer": "Mistral AI",
        "url": "https://mistral.ai/",
        "description": "European AI. Mistral Large/Small/Codestral models. OpenAI-compatible API. Strong multilingual support. Open-weight models available.",
        "pricingCAD": {"freeTier": True, "freeTierDetails": "Free Experiment plan (data used for research)", "freeTierLimits": {"requestsPerDay": "limited", "notes": "Requires phone verification"}, "paidPlans": [{"name": "Build", "priceCAD": 36, "period": "month", "details": "No data training, higher limits"}]},
        "capabilities": ["text-generation", "text-analysis", "code-generation", "summarization", "translation", "api-call"],
        "integrations": ["openrouter"],
        "accessMethod": "web+api",
        "platformSupport": ["web", "api"],
        "ranking": {"overall": 18, "inCategory": 6, "trend": "rising"},
        "pros": ["European alternative to US AI", "OpenAI-compatible API", "Good multilingual"],
        "cons": ["Free tier uses your data", "Smaller ecosystem"],
        "trustScore": 74,
        "firstTracked": "2026-03-28",
        "lastVerified": "2026-03-28"
    },
    {
        "id": "ros2",
        "name": "ROS 2 (Robot Operating System)",
        "category": "robotics-ai",
        "developer": "Open Robotics",
        "url": "https://docs.ros.org/",
        "description": "Standard middleware for robotics. Handles communication between sensors, actuators, planners, AI modules. ROS 2 Humble/Iron/Jazzy for production robots.",
        "pricingCAD": {"freeTier": True, "freeTierDetails": "Fully free and open source (Apache 2.0)", "freeTierLimits": {"requestsPerDay": "unlimited"}, "paidPlans": []},
        "capabilities": ["robot-control", "sensor-processing", "path-planning", "simulation", "code-execution"],
        "integrations": ["gazebo", "ros2-nav2", "isaac-sim", "mujoco", "realsense", "opencv", "px4"],
        "accessMethod": "cli",
        "platformSupport": ["linux", "windows"],
        "ranking": {"overall": 25, "inCategory": 1, "trend": "stable"},
        "pros": ["Industry standard for robotics", "Massive package ecosystem", "Simulation integration"],
        "cons": ["Linux-first", "Steep learning curve", "Version fragmentation"],
        "trustScore": 88,
        "firstTracked": "2026-03-28",
        "lastVerified": "2026-03-28"
    }
]

added = 0
for nt in new_tools:
    if nt["id"] not in existing:
        tools.append(nt)
        added += 1
        print(f"  Added: {nt['id']} ({nt['name']})")
    else:
        print(f"  Skipped (exists): {nt['id']}")

with open("data/tools.json", "w", encoding="utf-8") as f:
    json.dump(tools, f, indent=2, ensure_ascii=False)

meta = json.load(open("data/meta.json", "r", encoding="utf-8"))
meta["totalTools"] = len(tools)
with open("data/meta.json", "w", encoding="utf-8") as f:
    json.dump(meta, f, indent=2, ensure_ascii=False)

print(f"\nAdded {added} tools. Total: {len(tools)}")
