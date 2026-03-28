# CC-AIProgress — Self-Improving AI Research & Implementation System

## PRIME DIRECTIVE
**Every session should leave this system better than it found it.** Don't just answer questions — research, discover, update data, fix stale information, propose improvements, and execute them. The system improves itself through every interaction.

## What This Is
An autonomous AI research system that:
1. **Discovers** AI tools, capabilities, and developments across ALL domains — automatically
2. **Synthesizes** raw information into actionable intelligence briefings
3. **Updates itself** — data files are living databases, not static documents
4. **Proposes** ambitious projects and EXECUTES them using multi-AI coordination
5. **Overcomes obstacles** — nothing is a brick wall, find workarounds or alternative tools
6. **Improves itself** — every session should upgrade the system's capabilities, data, or architecture

The HTML dashboard is the human interface (viewed on Chromebook/any browser). The JSON data files are the intelligence layer. The scheduled tasks are the automation engine. Any AI can read and update all of it.

## Self-Improvement Protocol
On EVERY session, the AI should:
1. **Read** `data/briefings.json` — check what's changed since last session
2. **Read** `data/automation.json` — check pipeline status and what needs doing
3. **Research** — web search for AI news since the last briefing date
4. **Update** — any stale data in tools.json, strategies.json, etc.
5. **Propose** — new tests, new tools to add, new projects, improvements to the system itself
6. **Execute** — don't just suggest, DO IT (update files, add entries, rewrite stale sections)
7. **Brief** — append a new entry to briefings.json summarizing what was done and found

## Architecture
```
CC-AIProgress/
├── index.html                  # Dashboard interface (human view)
├── data/
│   ├── tools.json              # AI tools database (172+ tools, all domains incl. robotics)
│   ├── news-sources.json       # 167+ intelligence sources (41 non-English)
│   ├── categories.json         # 15 category definitions
│   ├── discovery-methods.json  # 15 methods for auto-generating source/tool lists + 6-layer self-improvement architecture
│   ├── regulations.json        # AI regulations (Canada/USA/EU/World)
│   ├── workflows.json          # Multi-tool pipelines
│   ├── tests.json              # Hands-on testing guides
│   ├── projects.json           # Moonshot projects with phases
│   ├── strategies.json         # Overcoming AI limitations playbook
│   ├── briefings.json          # AI-generated intelligence reports
│   ├── automation.json         # Pipeline definitions and autonomy progress
│   ├── trust-framework.json    # Security incidents, trust scoring dimensions
│   ├── programmatic-sources.json # 15 API endpoints with exact URLs/auth/rate limits
│   └── meta.json               # Version, timestamps, exchange rate
├── assets/
│   ├── css/dashboard.css       # UI styles
│   └── js/dashboard.js         # Dashboard logic
├── scripts/
│   └── daily-research.md       # Scheduled task prompt template
├── docs/
│   ├── initial-prompt.md       # Original project brief
│   ├── decisions.md            # Architecture decisions
│   └── automated-tracking-research.md
└── CLAUDE.md                   # THIS FILE — system instructions
```

## Self-Improvement at ALL Levels
The system doesn't just track AI — it recursively improves how it tracks AI. Six layers, each feeding the others:
1. **Source Discovery** — 15 methods in `discovery-methods.json` auto-generate source lists (backlink crawls, Reddit mining, HF trending, etc.)
2. **Tool Discovery** — Sources feed tool identification. Track which channels find best tools earliest.
3. **Category Evolution** — Tool clusters signal new categories. Monthly: split oversized categories, merge empty ones.
4. **Workflow Discovery** — YouTube/Reddit/GitHub mining for multi-tool pipelines people actually use.
5. **Strategy & Knowledge** — When predictions prove wrong, rewrite them. Track accuracy over time.
6. **System Architecture** — Every friction point triggers a fix. Validation errors → new rules. Slow discovery → pipeline optimization. CLAUDE.md itself gets updated.

**Cross-layer feedback**: Each layer improves the layers above AND below it. Better sources → better tools → better categories → better workflows → better strategies → better architecture → better sources (full loop).

## Automation Architecture
- **Tool-Agnostic Execution** — NO pipeline step is hardcoded to a specific AI or service. Every step specifies a CAPABILITY needed (e.g., "web search", "analysis", "code generation"), and the system selects the best available tool at runtime. Today that might be Claude; tomorrow it might be something that doesn't exist yet.
- **Fallback Chains** — Every critical operation has a fallback. If the primary AI is down, try the secondary. If all AI APIs are down, fall back to RSS-only mode (no synthesis, just raw data collection). If even the internet is degraded, use cached data and flag staleness. See `automation.json` for specific chains.
- **Hardcoded Last Resort** — The JSON data files ARE the system. Even if every AI provider and automation engine fails, a human can still read the JSON, update it with a text editor, and the dashboard works. This is by design — no single point of failure.
- **n8n** (planned) — RSS scraping, multi-AI routing, webhook triggers, 24/7 automation
- **GitHub Actions** — Weekly JSON validation, meta refresh, deployment
- **The dashboard** — Just the visualization layer, NOT the product

## Change Safeguards
The system SHOULD auto-update, auto-correct, and even make major architectural changes. But:
- **Breaking change detection**: Before writing any JSON file, validate against schema. If validation fails, DON'T write — log the error and alert.
- **Proportionality alerts**: If a single update would change >20% of a data file (e.g., removing 35 tools at once, or one tool replacing an entire category), PAUSE and alert the user. This could be a genuine evolutionary leap OR a catastrophic error. The user decides.
- **Rollback capability**: Git history is the undo button. Every auto-update should be a distinct commit with a clear message explaining what changed and why.
- **Consolidation signals**: If the system detects one tool genuinely replacing many (e.g., a new model that makes 5 separate tools obsolete), it should: (1) document the evidence, (2) alert the user with the reasoning, (3) NOT auto-remove the displaced tools until confirmed. Mark them as "potentially-displaced-by: [tool-id]" instead.
- **Never silently degrade**: If a pipeline step fails, the output must say so. A briefing generated with only 3 of 10 sources available is still useful — but it must disclose "generated with limited sources due to [reason]."

## Overcoming Limits
- **Session limits**: Use CLAUDE.md + session handoff summaries + multiple parallel sessions
- **Single AI limits**: Coordinate Claude + GPT + Gemini + Perplexity via n8n or API calls. The system should discover and adopt better tools as they appear — including replacing its own components.
- **Infrastructure failure**: Fallback chains ensure no single outage kills the system. RSS works when APIs don't. Static files work when everything's down.
- **Stale data**: Scheduled tasks re-research and rewrite automatically
- **Unknown unknowns**: Search GitHub trending, Reddit, HN, YouTube, TikTok discussions — find what others are doing that we haven't thought of
- **Chromebook constraints**: NONE — all computation is cloud-side (Claude servers, n8n VPS, GitHub Actions). Chromebook is just a browser.

## Data Conventions
- All IDs use kebab-case (e.g., `"text-chat"`, `"chatgpt"`)
- All dates use ISO 8601 format (e.g., `"2026-03-27"`)
- All prices are in CAD with the exchange rate noted in `data/meta.json`
- Tool rankings: lower number = better (1 is best)
- Trend values: `"rising"`, `"stable"`, `"declining"`
- `data-ai-*` HTML attributes make the dashboard machine-readable

## JSON Schemas

### tools.json
```json
[{
  "id": "string",
  "name": "string",
  "category": "string (ref categories.id)",
  "developer": "string",
  "url": "string",
  "description": "string",
  "pricingCAD": {
    "freeTier": true/false,
    "freeTierDetails": "string",
    "paidPlans": [{ "name": "string", "priceCAD": number, "period": "month|year", "details": "string" }]
  },
  "ranking": { "overall": number, "inCategory": number, "trend": "rising|stable|declining" },
  "pros": ["string"],
  "cons": ["string"],
  "lastVerified": "ISO date"
}]
```

### briefings.json
```json
[{
  "id": "briefing-YYYY-MM-DD",
  "date": "ISO date",
  "type": "daily|weekly|alert",
  "title": "string",
  "summary": "string (executive summary)",
  "sections": [{
    "heading": "string",
    "content": "string (real analysis)",
    "impact": "high|medium|low",
    "affectedTools": ["tool-id"],
    "affectedProjects": ["project-id"],
    "actionItems": ["string"]
  }],
  "toolUpdates": [{ "toolId": "string", "change": "string", "verified": true }],
  "newDiscoveries": [{ "name": "string", "url": "string", "category": "string", "why": "string" }],
  "generatedBy": "claude-scheduled-task|claude-session|n8n"
}]
```

### automation.json
```json
{
  "pipelines": [{ "id": "string", "name": "string", "description": "string", "schedule": "string", "status": "active|planned|concept", "engine": "claude-scheduled|n8n|github-actions", "steps": [{ "order": number, "action": "string", "tool": "string", "details": "string" }], "outputs": ["string"], "lastRun": "ISO date|null" }],
  "aiAccounts": [{ "service": "string", "purpose": "string", "status": "active|pending-setup" }],
  "automationGoals": [{ "level": 0-4, "name": "string", "description": "string", "currentProgress": "string", "blockers": ["string"], "nextSteps": ["string"] }]
}
```

### strategies.json
```json
[{
  "id": "string",
  "category": "string",
  "title": "string",
  "description": "string",
  "currentState": "string (MUST be re-verified by scheduled task — goes stale)",
  "strategies": [{ "name": "string", "how": "string", "tools": ["string"], "difficulty": "beginner|intermediate|advanced", "cost": "free|low|medium|high" }],
  "futureState": "string (MUST be re-verified — predictions go stale)",
  "relevantTools": ["tool-id"]
}]
```

### projects.json
```json
[{
  "id": "string", "name": "string", "status": "in-progress|planned|concept",
  "ambition": "high|moonshot", "description": "string",
  "currentState": "string", "targetState": "string",
  "phases": [{ "phase": number, "name": "string", "status": "string", "description": "string", "tasks": ["string"], "aiTools": ["string"], "estimatedCost": "string", "blockers": ["string"], "workarounds": ["string"] }],
  "biggestRisk": "string", "mitigation": "string", "lastUpdated": "ISO date"
}]
```

### tests.json / news-sources.json / categories.json / regulations.json / workflows.json
See existing files for schema — each follows the same kebab-case ID + ISO date conventions.

## Moonshot Projects
1. **AI-Progress v2** — Self-evolving intelligence system with multi-AI orchestration
2. **Idea Machine** — Voice-first AI assistant on phone + PC
3. **Boundary Pusher** — Systematic capability testing across all AI tools
4. **Text-to-3D-Print** — AI 3D design to physical manufacturing
5. **AI Electronics Lab** — AI-designed PCBs from text
6. **Workplace Automation** — AI handles daily tasks + phone
7. **Solo AI Film Studio** — Video production with zero camera/crew
8. **Medical AI Research** — Multi-source condition analysis
9. **AI Feature Film** — 60-minute movie production
10. **Multi-AI Coordinator** — One prompt routes to best AI automatically (n8n + API keys)

## Key Principles
- **Autonomous work** — Research, compile, propose, implement. Minimal interruptions.
- **Self-improvement** — Every session leaves the system better. Update CLAUDE.md itself if needed.
- **Think bigger** — Don't just track tools. Propose what's possible. Dream.
- **Nothing is a brick wall** — Every obstacle has a workaround or an alternative path.
- **Adapt automatically** — When new information changes a strategy, update the strategy. Don't leave stale predictions.
- **Show what others are doing** — GitHub repos, YouTube demos, TikTok discoveries, Reddit experiments. Find what we haven't thought of.
- **Tool-agnostic** — Never hardcode to one AI or service. Specify capabilities, not vendors. The best tool today may be obsolete tomorrow. The system should discover and adopt replacements, including replacing its own components.
- **Graceful degradation** — Every operation has a fallback chain. Full AI → secondary AI → RSS-only → manual → cached data. Total failure should be impossible.
- **Bold changes, safe execution** — Auto-update aggressively, but alert the user on consolidation events (one tool replacing many), mass changes (>20% of a file), or removals. Could be evolution or error — let the user decide.
