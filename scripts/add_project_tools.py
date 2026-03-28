#!/usr/bin/env python3
"""Add ~30 tools referenced by projects.json that are missing from tools.json."""

import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_PATH = os.path.join(BASE_DIR, "data", "tools.json")
META_PATH = os.path.join(BASE_DIR, "data", "meta.json")

NEW_TOOLS = [
    # === AI APIs ===
    {
        "id": "claude-api",
        "name": "Anthropic Claude API",
        "category": "text-chat",
        "developer": "Anthropic",
        "url": "https://docs.anthropic.com/en/docs/welcome",
        "description": "Programmatic access to Claude models (Opus, Sonnet, Haiku) via REST API. Supports text, vision, tool use, and streaming. Pay-per-token pricing.",
        "pricingCAD": {
            "freeTier": True,
            "freeTierDetails": "Free tier with limited credits for new accounts",
            "paidPlans": [
                {"name": "Pay-as-you-go", "priceCAD": 0, "period": "month", "details": "Opus: ~$21.60/$108 per MTok in/out; Sonnet: ~$4.32/$21.60; Haiku: ~$0.36/$1.80 (CAD)"}
            ]
        },
        "ranking": {"overall": 173, "inCategory": 6, "trend": "rising"},
        "pros": ["Full programmatic control over Claude models", "Excellent documentation and SDKs (Python, TypeScript)", "Tool use and structured output support"],
        "cons": ["Costs scale with usage — can get expensive at volume", "Rate limits on free tier", "No built-in UI — developer-focused"],
        "logoUrl": "",
        "lastVerified": "2026-03-28",
        "trustScore": 88
    },
    {
        "id": "openai-api",
        "name": "OpenAI API",
        "category": "text-chat",
        "developer": "OpenAI",
        "url": "https://platform.openai.com/",
        "description": "Comprehensive AI API offering GPT-4o/GPT-5, DALL-E 3, Whisper, TTS, embeddings, and fine-tuning. The most widely integrated AI API with extensive third-party ecosystem.",
        "pricingCAD": {
            "freeTier": True,
            "freeTierDetails": "Free credits for new accounts",
            "paidPlans": [
                {"name": "Pay-as-you-go", "priceCAD": 0, "period": "month", "details": "GPT-4o: ~$3.60/$14.40 per MTok in/out; GPT-5: ~$14.40/$43.20 (CAD)"}
            ]
        },
        "ranking": {"overall": 174, "inCategory": 7, "trend": "stable"},
        "pros": ["Largest third-party integration ecosystem", "Widest model selection (text, image, audio, embeddings)", "Mature SDKs and tooling"],
        "cons": ["Complex pricing across many models", "Rate limits can be restrictive on lower tiers", "Data usage policies require careful review"],
        "logoUrl": "",
        "lastVerified": "2026-03-28",
        "trustScore": 85
    },
    {
        "id": "gemini-api",
        "name": "Google Gemini API",
        "category": "text-chat",
        "developer": "Google",
        "url": "https://ai.google.dev/",
        "description": "Multimodal AI API via Google AI Studio or Vertex AI. Access Gemini 2.5 Pro/Flash models with text, image, video, and audio understanding. Generous free tier.",
        "pricingCAD": {
            "freeTier": True,
            "freeTierDetails": "Generous free tier via Google AI Studio (rate-limited)",
            "paidPlans": [
                {"name": "Pay-as-you-go", "priceCAD": 0, "period": "month", "details": "Gemini 2.5 Pro: ~$1.80/$14.40 per MTok in/out (CAD). Free tier available."}
            ]
        },
        "ranking": {"overall": 175, "inCategory": 8, "trend": "rising"},
        "pros": ["Very generous free tier for prototyping", "Native multimodal (text, image, video, audio)", "Deep integration with Google Cloud ecosystem"],
        "cons": ["Vertex AI setup can be complex", "Smaller third-party ecosystem than OpenAI", "Model naming/versioning can be confusing"],
        "logoUrl": "",
        "lastVerified": "2026-03-28",
        "trustScore": 85
    },
    {
        "id": "perplexity-api",
        "name": "Perplexity API",
        "category": "text-chat",
        "developer": "Perplexity AI",
        "url": "https://docs.perplexity.ai/",
        "description": "Search-augmented AI API that combines LLM reasoning with real-time web search. Returns cited, up-to-date answers. Ideal for research and fact-checking pipelines.",
        "pricingCAD": {
            "freeTier": False,
            "freeTierDetails": "",
            "paidPlans": [
                {"name": "Pay-as-you-go", "priceCAD": 0, "period": "month", "details": "Sonar Pro: ~$4.32/$21.60 per MTok in/out + $7.20/1K searches (CAD)"}
            ]
        },
        "ranking": {"overall": 176, "inCategory": 9, "trend": "rising"},
        "pros": ["Built-in web search with citations", "Always returns current information", "Simple API — no need to build RAG pipelines"],
        "cons": ["No free tier for API access", "Search costs add up at scale", "Smaller model selection than competitors"],
        "logoUrl": "",
        "lastVerified": "2026-03-28",
        "trustScore": 78
    },
    {
        "id": "dall-e-api",
        "name": "OpenAI DALL-E API",
        "category": "image-generation",
        "developer": "OpenAI",
        "url": "https://platform.openai.com/docs/guides/images",
        "description": "Image generation API endpoint supporting DALL-E 3 and GPT Image 1.5. Create, edit, and vary images programmatically. Integrated into many third-party apps.",
        "pricingCAD": {
            "freeTier": False,
            "freeTierDetails": "",
            "paidPlans": [
                {"name": "Pay-per-image", "priceCAD": 0, "period": "month", "details": "DALL-E 3: ~$0.06-$0.17 CAD/image depending on resolution"}
            ]
        },
        "ranking": {"overall": 177, "inCategory": 8, "trend": "stable"},
        "pros": ["Easy API integration for image generation", "Supports inpainting and variations", "Well-documented with broad SDK support"],
        "cons": ["No free tier — pay per image", "Content policy restrictions can be aggressive", "Quality trails some newer competitors"],
        "logoUrl": "",
        "lastVerified": "2026-03-28",
        "trustScore": 84
    },
    {
        "id": "suno-api",
        "name": "Suno API",
        "category": "audio-music",
        "developer": "Suno",
        "url": "https://suno.com/",
        "description": "Music generation API for creating songs from text prompts. Generates vocals, instrumentals, and full productions. Used for automated music creation pipelines.",
        "pricingCAD": {
            "freeTier": True,
            "freeTierDetails": "Limited free generations via web interface",
            "paidPlans": [
                {"name": "Pro", "priceCAD": 14, "period": "month", "details": "2,500 credits/month, commercial use"},
                {"name": "Premier", "priceCAD": 43, "period": "month", "details": "10,000 credits/month, commercial use"}
            ]
        },
        "ranking": {"overall": 178, "inCategory": 5, "trend": "rising"},
        "pros": ["Full song generation from text prompts", "Includes vocals and instrumentals", "API access for automation pipelines"],
        "cons": ["API access may require higher-tier plan", "Copyright concerns around training data", "Limited fine control over musical structure"],
        "logoUrl": "",
        "lastVerified": "2026-03-28",
        "trustScore": 72
    },
    {
        "id": "runway-api",
        "name": "Runway API",
        "category": "video-generation",
        "developer": "Runway",
        "url": "https://docs.runwayml.com/",
        "description": "Video generation API providing programmatic access to Gen-3 Alpha and other Runway models. Create videos from text or images via REST API.",
        "pricingCAD": {
            "freeTier": False,
            "freeTierDetails": "",
            "paidPlans": [
                {"name": "Standard", "priceCAD": 17, "period": "month", "details": "625 credits/month"},
                {"name": "Pro", "priceCAD": 43, "period": "month", "details": "2,250 credits/month, higher resolution"}
            ]
        },
        "ranking": {"overall": 179, "inCategory": 5, "trend": "rising"},
        "pros": ["Industry-leading video generation quality", "API enables automated video pipelines", "Active development with frequent model updates"],
        "cons": ["Credits consumed quickly for video generation", "No free API tier", "Generation times can be slow for longer clips"],
        "logoUrl": "",
        "lastVerified": "2026-03-28",
        "trustScore": 80
    },

    # === Developer/Automation Tools ===
    {
        "id": "github-actions",
        "name": "GitHub Actions",
        "category": "workflow-automation",
        "developer": "GitHub (Microsoft)",
        "url": "https://github.com/features/actions",
        "description": "CI/CD and workflow automation platform built into GitHub. Run scheduled tasks, deploy code, validate data, and automate any software workflow. Free for public repos.",
        "pricingCAD": {
            "freeTier": True,
            "freeTierDetails": "2,000 minutes/month free for public repos, 500 min for private",
            "paidPlans": [
                {"name": "Team", "priceCAD": 5.76, "period": "month", "details": "Per user, 3,000 minutes/month"},
                {"name": "Enterprise", "priceCAD": 30.24, "period": "month", "details": "Per user, 50,000 minutes/month, advanced features"}
            ]
        },
        "ranking": {"overall": 180, "inCategory": 3, "trend": "stable"},
        "pros": ["Free for public repositories", "Massive marketplace of pre-built actions", "Native GitHub integration — triggers on push, PR, schedule"],
        "cons": ["YAML configuration can be complex", "Debugging failed workflows is painful", "Minutes quota burns fast on private repos"],
        "logoUrl": "",
        "lastVerified": "2026-03-28",
        "trustScore": 92
    },
    {
        "id": "github-pages",
        "name": "GitHub Pages",
        "category": "workflow-automation",
        "developer": "GitHub (Microsoft)",
        "url": "https://pages.github.com/",
        "description": "Free static site hosting directly from GitHub repositories. Supports custom domains, HTTPS, and Jekyll. Perfect for dashboards, docs, and project sites.",
        "pricingCAD": {
            "freeTier": True,
            "freeTierDetails": "Free hosting for public repos, 100GB bandwidth/month",
            "paidPlans": []
        },
        "ranking": {"overall": 181, "inCategory": 4, "trend": "stable"},
        "pros": ["Completely free for public repos", "Automatic deployment from git push", "Custom domain and HTTPS support"],
        "cons": ["Static sites only — no server-side code", "1GB repo size limit recommended", "Build times can be slow for large sites"],
        "logoUrl": "",
        "lastVerified": "2026-03-28",
        "trustScore": 92
    },
    {
        "id": "claude-scheduled-tasks",
        "name": "Claude Scheduled Tasks",
        "category": "workflow-automation",
        "developer": "Anthropic",
        "url": "https://claude.ai/",
        "description": "Recurring Claude prompts that run automatically on Anthropic servers. Execute research, data updates, and analysis on a schedule without manual intervention.",
        "pricingCAD": {
            "freeTier": False,
            "freeTierDetails": "",
            "paidPlans": [
                {"name": "Included with Pro", "priceCAD": 29, "period": "month", "details": "Available as part of Claude Pro subscription"}
            ]
        },
        "ranking": {"overall": 182, "inCategory": 5, "trend": "rising"},
        "pros": ["Runs autonomously on schedule", "Full Claude capabilities including web search", "No infrastructure to manage"],
        "cons": ["Requires Claude Pro subscription", "Limited scheduling granularity", "Output visibility can be limited"],
        "logoUrl": "",
        "lastVerified": "2026-03-28",
        "trustScore": 85
    },
    {
        "id": "puppeteer",
        "name": "Puppeteer",
        "category": "coding-assistants",
        "developer": "Google",
        "url": "https://pptr.dev/",
        "description": "Headless Chrome/Chromium browser automation library for Node.js. Scrape web pages, generate PDFs, take screenshots, and automate browser interactions programmatically.",
        "pricingCAD": {
            "freeTier": True,
            "freeTierDetails": "Fully open source (Apache 2.0)",
            "paidPlans": []
        },
        "ranking": {"overall": 183, "inCategory": 10, "trend": "stable"},
        "pros": ["Official Google Chrome automation tool", "Excellent for web scraping and testing", "Large community and extensive documentation"],
        "cons": ["Chrome/Chromium only — no Firefox/Safari", "High memory usage for many concurrent pages", "Stealth mode needed to avoid bot detection"],
        "logoUrl": "",
        "lastVerified": "2026-03-28",
        "trustScore": 88
    },
    {
        "id": "playwright",
        "name": "Playwright",
        "category": "coding-assistants",
        "developer": "Microsoft",
        "url": "https://playwright.dev/",
        "description": "Cross-browser automation framework supporting Chromium, Firefox, and WebKit. Modern alternative to Puppeteer with auto-waiting, tracing, and parallel execution.",
        "pricingCAD": {
            "freeTier": True,
            "freeTierDetails": "Fully open source (Apache 2.0)",
            "paidPlans": []
        },
        "ranking": {"overall": 184, "inCategory": 11, "trend": "rising"},
        "pros": ["Cross-browser support (Chrome, Firefox, Safari/WebKit)", "Built-in auto-waiting eliminates flaky tests", "Excellent debugging with trace viewer"],
        "cons": ["Slightly steeper learning curve than Puppeteer", "Larger dependency footprint", "Some advanced features are Node.js-centric"],
        "logoUrl": "",
        "lastVerified": "2026-03-28",
        "trustScore": 88
    },
    {
        "id": "fastapi",
        "name": "FastAPI",
        "category": "coding-assistants",
        "developer": "Sebastián Ramírez (Open Source)",
        "url": "https://fastapi.tiangolo.com/",
        "description": "Modern Python web framework for building APIs. Automatic OpenAPI docs, async support, type validation via Pydantic. One of the fastest Python frameworks available.",
        "pricingCAD": {
            "freeTier": True,
            "freeTierDetails": "Fully open source (MIT license)",
            "paidPlans": []
        },
        "ranking": {"overall": 185, "inCategory": 12, "trend": "rising"},
        "pros": ["Automatic interactive API documentation", "Very fast performance (Starlette + Pydantic)", "Excellent type safety and validation"],
        "cons": ["Python-only — no other language support", "Smaller ecosystem than Django/Flask", "Async patterns can be confusing for beginners"],
        "logoUrl": "",
        "lastVerified": "2026-03-28",
        "trustScore": 82
    },
    {
        "id": "cloudflare-tunnel",
        "name": "Cloudflare Tunnel",
        "category": "workflow-automation",
        "developer": "Cloudflare",
        "url": "https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/",
        "description": "Expose local services to the internet securely without port forwarding. Free tier available. Useful for webhooks, n8n, and local AI model serving.",
        "pricingCAD": {
            "freeTier": True,
            "freeTierDetails": "Free for personal use with Cloudflare account",
            "paidPlans": [
                {"name": "Zero Trust (Teams)", "priceCAD": 10.08, "period": "month", "details": "Per user, advanced access controls and logging"}
            ]
        },
        "ranking": {"overall": 186, "inCategory": 6, "trend": "rising"},
        "pros": ["Free tier for personal use", "No port forwarding or firewall changes needed", "Built-in DDoS protection and SSL"],
        "cons": ["Requires Cloudflare account and DNS setup", "Dependent on Cloudflare infrastructure", "Can add latency for some use cases"],
        "logoUrl": "",
        "lastVerified": "2026-03-28",
        "trustScore": 88
    },

    # === 3D/CAD/Manufacturing ===
    {
        "id": "blender",
        "name": "Blender",
        "category": "3d-cad",
        "developer": "Blender Foundation",
        "url": "https://www.blender.org/",
        "description": "Industry-standard open-source 3D creation suite. Modeling, sculpting, animation, rendering, compositing, and video editing. Massive addon ecosystem including AI plugins.",
        "pricingCAD": {
            "freeTier": True,
            "freeTierDetails": "Completely free and open source (GPL)",
            "paidPlans": []
        },
        "ranking": {"overall": 187, "inCategory": 2, "trend": "stable"},
        "pros": ["Completely free — no subscription or license fees", "Professional-grade features rivaling paid software", "Huge community and addon ecosystem"],
        "cons": ["Steep learning curve for beginners", "UI can be overwhelming", "Some CAD/engineering features are less polished than dedicated tools"],
        "logoUrl": "",
        "lastVerified": "2026-03-28",
        "trustScore": 90
    },
    {
        "id": "freecad",
        "name": "FreeCAD",
        "category": "3d-cad",
        "developer": "FreeCAD Community",
        "url": "https://www.freecad.org/",
        "description": "Open-source parametric 3D CAD modeler for engineering and product design. Supports STEP, IGES, STL, and many other formats. Python scriptable.",
        "pricingCAD": {
            "freeTier": True,
            "freeTierDetails": "Completely free and open source (LGPL)",
            "paidPlans": []
        },
        "ranking": {"overall": 188, "inCategory": 3, "trend": "stable"},
        "pros": ["Free parametric CAD — rare in engineering software", "Supports industry-standard file formats", "Python scripting for automation"],
        "cons": ["Less polished UI than commercial alternatives", "Can be unstable with complex models", "Smaller community than Blender or Fusion 360"],
        "logoUrl": "",
        "lastVerified": "2026-03-28",
        "trustScore": 75
    },
    {
        "id": "fusion-360",
        "name": "Autodesk Fusion 360",
        "category": "3d-cad",
        "developer": "Autodesk",
        "url": "https://www.autodesk.com/products/fusion-360/",
        "description": "Professional cloud-based CAD/CAM/CAE platform. Parametric modeling, simulation, generative design, and CNC toolpath generation. Industry standard for product design.",
        "pricingCAD": {
            "freeTier": True,
            "freeTierDetails": "Free for personal/hobby use with limited features",
            "paidPlans": [
                {"name": "Commercial", "priceCAD": 828, "period": "year", "details": "Full features including simulation and generative design"}
            ]
        },
        "ranking": {"overall": 189, "inCategory": 1, "trend": "stable"},
        "pros": ["Industry-standard CAD with cloud collaboration", "Free hobby tier is very capable", "Integrated CAM for CNC machining"],
        "cons": ["Expensive commercial license ($828 CAD/yr)", "Cloud-dependent — limited offline use", "Can be slow with very large assemblies"],
        "logoUrl": "",
        "lastVerified": "2026-03-28",
        "trustScore": 85
    },
    {
        "id": "orcaslicer-cli",
        "name": "OrcaSlicer",
        "category": "3d-cad",
        "developer": "SoftFever (Bambu Lab fork)",
        "url": "https://github.com/SoftFever/OrcaSlicer",
        "description": "Open-source 3D print slicer forked from Bambu Studio. Supports most FDM printers. CLI mode enables automated slicing pipelines. Advanced multi-material support.",
        "pricingCAD": {
            "freeTier": True,
            "freeTierDetails": "Completely free and open source (AGPL)",
            "paidPlans": []
        },
        "ranking": {"overall": 190, "inCategory": 4, "trend": "rising"},
        "pros": ["Free with excellent Bambu Lab printer support", "CLI mode for automation pipelines", "Active development with frequent updates"],
        "cons": ["Primarily FDM-focused — limited resin support", "Fork fragmentation risk", "Some features lag behind PrusaSlicer"],
        "logoUrl": "",
        "lastVerified": "2026-03-28",
        "trustScore": 76
    },

    # === Electronics ===
    {
        "id": "ltspice",
        "name": "LTspice",
        "category": "3d-cad",
        "developer": "Analog Devices",
        "url": "https://www.analog.com/en/resources/design-tools-and-calculators/ltspice-simulator.html",
        "description": "Industry-standard SPICE circuit simulator. Schematic capture, waveform viewer, and simulation of analog/mixed-signal circuits. Completely free with no limits.",
        "pricingCAD": {
            "freeTier": True,
            "freeTierDetails": "Completely free with no feature restrictions",
            "paidPlans": []
        },
        "ranking": {"overall": 191, "inCategory": 5, "trend": "stable"},
        "pros": ["Completely free with no restrictions", "Industry-standard SPICE simulation accuracy", "Huge component library from Analog Devices"],
        "cons": ["Dated UI — Windows-centric design", "No native Linux support (Wine works)", "Schematic editor is less intuitive than modern tools"],
        "logoUrl": "",
        "lastVerified": "2026-03-28",
        "trustScore": 85
    },
    {
        "id": "jlcpcb-api",
        "name": "JLCPCB",
        "category": "3d-cad",
        "developer": "JLCPCB",
        "url": "https://jlcpcb.com/",
        "description": "Low-cost PCB manufacturing service with API ordering capabilities. Supports PCB fabrication, SMT assembly, and 3D printing. Popular for prototyping and small batch production.",
        "pricingCAD": {
            "freeTier": False,
            "freeTierDetails": "",
            "paidPlans": [
                {"name": "Per-order", "priceCAD": 0, "period": "month", "details": "Starting ~$2.88 CAD for 5 PCBs (2-layer). Assembly from ~$11.52 CAD setup."}
            ]
        },
        "ranking": {"overall": 192, "inCategory": 6, "trend": "stable"},
        "pros": ["Extremely low-cost PCB manufacturing", "Fast turnaround (24-72 hours production)", "API enables automated ordering pipelines"],
        "cons": ["Shipping from China adds time and cost", "Assembly parts library is limited", "Quality varies — inspect critical boards carefully"],
        "logoUrl": "",
        "lastVerified": "2026-03-28",
        "trustScore": 78
    },

    # === Video/Media Production ===
    {
        "id": "davinci-resolve",
        "name": "DaVinci Resolve",
        "category": "video-generation",
        "developer": "Blackmagic Design",
        "url": "https://www.blackmagicdesign.com/products/davinciresolve",
        "description": "Professional video editing, color grading, VFX, and audio post-production suite. Free version includes nearly all features. Industry standard for color grading.",
        "pricingCAD": {
            "freeTier": True,
            "freeTierDetails": "Free version with most professional features included",
            "paidPlans": [
                {"name": "Studio", "priceCAD": 468, "period": "year", "details": "One-time purchase. Neural Engine AI tools, HDR, stereoscopic 3D, multi-GPU."}
            ]
        },
        "ranking": {"overall": 193, "inCategory": 6, "trend": "stable"},
        "pros": ["Free version is incredibly capable", "Industry-leading color grading tools", "All-in-one: edit, color, VFX, audio, delivery"],
        "cons": ["Steep learning curve — very professional-oriented", "High system requirements for 4K+ editing", "Some AI features require paid Studio version"],
        "logoUrl": "",
        "lastVerified": "2026-03-28",
        "trustScore": 90
    },

    # === Voice/Communication ===
    {
        "id": "coqui-tts",
        "name": "Coqui TTS",
        "category": "speech-voice",
        "developer": "Coqui (Open Source Community)",
        "url": "https://github.com/coqui-ai/TTS",
        "description": "Open-source text-to-speech library supporting multiple languages and voice cloning. Runs locally for privacy. Includes XTTS v2 for high-quality multilingual synthesis.",
        "pricingCAD": {
            "freeTier": True,
            "freeTierDetails": "Fully open source (MPL 2.0)",
            "paidPlans": []
        },
        "ranking": {"overall": 194, "inCategory": 4, "trend": "stable"},
        "pros": ["Runs completely locally — full privacy", "Voice cloning from short audio samples", "Multiple languages and models available"],
        "cons": ["Requires decent GPU for real-time synthesis", "Quality below commercial TTS services", "Company shut down — community-maintained now"],
        "logoUrl": "",
        "lastVerified": "2026-03-28",
        "trustScore": 70
    },
    {
        "id": "twilio",
        "name": "Twilio",
        "category": "speech-voice",
        "developer": "Twilio",
        "url": "https://www.twilio.com/",
        "description": "Cloud communication APIs for voice calls, SMS, video, and messaging. Programmable voice enables AI-powered phone systems. Widely used for automated communication.",
        "pricingCAD": {
            "freeTier": True,
            "freeTierDetails": "Free trial with credits (~$22 CAD)",
            "paidPlans": [
                {"name": "Pay-as-you-go", "priceCAD": 0, "period": "month", "details": "Voice: ~$0.02 CAD/min, SMS: ~$0.01 CAD/msg, Phone numbers: ~$1.50 CAD/mo"}
            ]
        },
        "ranking": {"overall": 195, "inCategory": 5, "trend": "stable"},
        "pros": ["Industry-standard communication APIs", "Excellent documentation and SDKs", "Supports voice, SMS, video, and WhatsApp"],
        "cons": ["Costs add up quickly at scale", "Complex pricing structure", "Phone number regulations vary by country"],
        "logoUrl": "",
        "lastVerified": "2026-03-28",
        "trustScore": 88
    },

    # === Productivity/Monitoring ===
    {
        "id": "power-automate",
        "name": "Microsoft Power Automate",
        "category": "productivity",
        "developer": "Microsoft",
        "url": "https://powerautomate.microsoft.com/",
        "description": "Low-code workflow automation platform. Connect Microsoft 365, third-party apps, and AI services. Desktop flows for RPA, cloud flows for API automation.",
        "pricingCAD": {
            "freeTier": True,
            "freeTierDetails": "Free with Microsoft 365 subscription (limited connectors)",
            "paidPlans": [
                {"name": "Premium", "priceCAD": 21.60, "period": "month", "details": "Per user, all connectors, AI Builder credits"},
                {"name": "Process", "priceCAD": 216, "period": "month", "details": "Per bot, unattended RPA"}
            ]
        },
        "ranking": {"overall": 196, "inCategory": 5, "trend": "stable"},
        "pros": ["Deep Microsoft 365 integration", "Low-code — accessible to non-developers", "Desktop RPA for legacy application automation"],
        "cons": ["Premium connectors require paid plan", "Can be slow for complex workflows", "Debugging flow errors is frustrating"],
        "logoUrl": "",
        "lastVerified": "2026-03-28",
        "trustScore": 85
    },
    {
        "id": "toggl",
        "name": "Toggl Track",
        "category": "productivity",
        "developer": "Toggl",
        "url": "https://toggl.com/track/",
        "description": "Simple time tracking tool for individuals and teams. One-click timer, detailed reports, and project-based tracking. Integrates with 100+ tools.",
        "pricingCAD": {
            "freeTier": True,
            "freeTierDetails": "Free for up to 5 users with basic tracking",
            "paidPlans": [
                {"name": "Starter", "priceCAD": 13, "period": "month", "details": "Per user, billable rates, project time estimates"},
                {"name": "Premium", "priceCAD": 26, "period": "month", "details": "Per user, time audits, scheduled reports"}
            ]
        },
        "ranking": {"overall": 197, "inCategory": 6, "trend": "stable"},
        "pros": ["Very simple one-click time tracking", "Free tier is generous for individuals", "Excellent reporting and data export"],
        "cons": ["Limited project management features", "Mobile app can be buggy", "No built-in invoicing"],
        "logoUrl": "",
        "lastVerified": "2026-03-28",
        "trustScore": 80
    },
    {
        "id": "rescuetime",
        "name": "RescueTime",
        "category": "productivity",
        "developer": "RescueTime",
        "url": "https://www.rescuetime.com/",
        "description": "Automatic time tracking and productivity monitoring. Runs in the background categorizing app and website usage. Focus sessions and distraction blocking.",
        "pricingCAD": {
            "freeTier": True,
            "freeTierDetails": "Free Lite version with basic tracking",
            "paidPlans": [
                {"name": "Premium", "priceCAD": 17.28, "period": "month", "details": "Detailed reports, focus sessions, distraction blocking, goal setting"}
            ]
        },
        "ranking": {"overall": 198, "inCategory": 7, "trend": "stable"},
        "pros": ["Completely automatic — no manual tracking needed", "Detailed productivity insights and trends", "Focus session and distraction blocking"],
        "cons": ["Privacy concern — monitors all computer activity", "Free tier is very limited", "Can feel surveillance-like for team use"],
        "logoUrl": "",
        "lastVerified": "2026-03-28",
        "trustScore": 75
    },

    # === Research/Medical ===
    {
        "id": "pubmed-api",
        "name": "PubMed API (E-utilities)",
        "category": "data-analysis",
        "developer": "National Center for Biotechnology Information (NCBI)",
        "url": "https://www.ncbi.nlm.nih.gov/home/develop/api/",
        "description": "Free API for searching and retrieving biomedical literature from PubMed's 36M+ citations. E-utilities provide programmatic access to search, fetch, and link biomedical data.",
        "pricingCAD": {
            "freeTier": True,
            "freeTierDetails": "Completely free. 3 requests/sec without API key, 10/sec with key.",
            "paidPlans": []
        },
        "ranking": {"overall": 199, "inCategory": 4, "trend": "stable"},
        "pros": ["Completely free access to 36M+ biomedical citations", "Well-documented REST API", "Authoritative source for medical/scientific research"],
        "cons": ["Rate-limited — need API key for higher throughput", "XML-heavy responses require parsing", "Search syntax has a learning curve"],
        "logoUrl": "",
        "lastVerified": "2026-03-28",
        "trustScore": 95
    },
    {
        "id": "clinicaltrials-api",
        "name": "ClinicalTrials.gov API",
        "category": "data-analysis",
        "developer": "National Library of Medicine (NLM)",
        "url": "https://clinicaltrials.gov/data-api/api",
        "description": "Free API for searching the world's largest clinical trial registry (400K+ studies). Query by condition, intervention, location, and status. Essential for medical research.",
        "pricingCAD": {
            "freeTier": True,
            "freeTierDetails": "Completely free with no authentication required",
            "paidPlans": []
        },
        "ranking": {"overall": 200, "inCategory": 5, "trend": "stable"},
        "pros": ["Completely free with no API key needed", "Comprehensive database of 400K+ clinical trials", "JSON responses — modern and easy to parse"],
        "cons": ["Data quality varies — submitted by sponsors", "Complex query syntax for advanced searches", "Some fields may be incomplete or outdated"],
        "logoUrl": "",
        "lastVerified": "2026-03-28",
        "trustScore": 95
    },
    {
        "id": "google-scholar-alerts",
        "name": "Google Scholar Alerts",
        "category": "data-analysis",
        "developer": "Google",
        "url": "https://scholar.google.com/",
        "description": "Email notifications for new academic papers matching search queries or citing specific papers. Free monitoring of research topics. No API — email-based alerts.",
        "pricingCAD": {
            "freeTier": True,
            "freeTierDetails": "Completely free with Google account",
            "paidPlans": []
        },
        "ranking": {"overall": 201, "inCategory": 6, "trend": "stable"},
        "pros": ["Completely free academic paper monitoring", "Covers vast majority of scholarly publications", "Citation alerts for tracking paper impact"],
        "cons": ["No API — email-only delivery", "Alert frequency is not configurable", "Can miss some publications — coverage gaps exist"],
        "logoUrl": "",
        "lastVerified": "2026-03-28",
        "trustScore": 85
    },

    # === Platform ===
    {
        "id": "youtube",
        "name": "YouTube",
        "category": "video-generation",
        "developer": "Google",
        "url": "https://www.youtube.com/",
        "description": "World's largest video platform with emerging AI features. Auto-captions, Dream Screen AI backgrounds, video summarization. Essential distribution channel for AI-generated content.",
        "pricingCAD": {
            "freeTier": True,
            "freeTierDetails": "Free to upload and watch, ad-supported",
            "paidPlans": [
                {"name": "Premium", "priceCAD": 16.49, "period": "month", "details": "Ad-free, background play, YouTube Music, downloads"}
            ]
        },
        "ranking": {"overall": 202, "inCategory": 7, "trend": "stable"},
        "pros": ["Largest video audience in the world", "Free hosting with unlimited storage", "AI auto-captions and translation features"],
        "cons": ["Aggressive content moderation and demonetization", "Algorithm changes unpredictably", "Compression reduces video quality"],
        "logoUrl": "",
        "lastVerified": "2026-03-28",
        "trustScore": 88
    },
]


def main():
    # Read existing tools
    with open(TOOLS_PATH, "r", encoding="utf-8") as f:
        tools = json.load(f)

    existing_ids = {t["id"] for t in tools}
    added = 0
    skipped = 0

    for tool in NEW_TOOLS:
        if tool["id"] in existing_ids:
            print(f"  SKIP (already exists): {tool['id']}")
            skipped += 1
        else:
            tools.append(tool)
            existing_ids.add(tool["id"])
            added += 1
            print(f"  ADDED: {tool['id']}")

    # Write updated tools
    with open(TOOLS_PATH, "w", encoding="utf-8") as f:
        json.dump(tools, f, indent=2, ensure_ascii=False)

    print(f"\nTotal tools now: {len(tools)}")
    print(f"Added: {added}, Skipped: {skipped}")

    # Update meta.json
    with open(META_PATH, "r", encoding="utf-8") as f:
        meta = json.load(f)

    meta["totalTools"] = len(tools)
    meta["lastUpdated"] = "2026-03-28"

    with open(META_PATH, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)

    print(f"Updated meta.json: totalTools={len(tools)}")


if __name__ == "__main__":
    main()
