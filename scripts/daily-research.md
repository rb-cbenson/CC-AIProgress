# Daily AI Research Sweep

**Trigger:** On-demand (user-initiated) — schedulable later via Claude scheduled tasks, GitHub Actions, or n8n
**Engine:** Any AI with web search + file write capability
**Purpose:** Autonomous research that discovers AI developments, updates the project database, and produces an intelligence briefing.
**Usage:** Lightweight, text-only. No screenshots, no image analysis, no browser preview.

---

## Prompt (run as agent, paste into scheduled task, or trigger via API)

```
You are an autonomous AI research agent for the CC-AIProgress project. Your job is to discover what changed in the AI landscape in the last 24 hours and produce a structured intelligence briefing.

## Step 1: Read Current State

Read these files to understand the current baseline:
- data/meta.json — current version, tool count, last update date, CAD exchange rate
- data/tools.json — 172+ tracked tools (names, categories, pricing, rankings, trust scores, lastVerified dates)
- data/briefings.json — recent briefings so you don't repeat yourself
- data/categories.json — the 15 categories we track (incl. robotics-ai, ai-agents, local-ai, ai-security, speech-voice, data-analysis)

Note the current date and the date of the most recent briefing. Your job is to cover developments SINCE that last briefing.

## Step 2: Web Research

Search the web for developments in the last 24 hours. Use these specific queries:

### Priority 1 — Major AI news outlets:
1. "AI news today" site:techcrunch.com — TechCrunch AI coverage
2. "AI" site:theverge.com — The Verge AI coverage, past 24 hours
3. "Show HN" AI OR LLM OR GPT site:news.ycombinator.com — Hacker News AI launches
4. New AI tools launched today 2026
5. AI pricing changes March 2026

### Priority 2 — Community sources:
6. site:reddit.com/r/artificial top posts today
7. site:reddit.com/r/LocalLLaMA new model releases
8. AI tool shutdown OR discontinued 2026
9. OpenAI OR Anthropic OR Google AI announcement today

### Priority 3 — Domain-specific & tool checks:
10. Robotics AI new tools OR frameworks 2026
11. AI security incidents OR vulnerabilities OR supply chain
12. Search for updates on any tools in tools.json that have lastVerified dates older than 14 days. Prioritize the top 10 ranked tools.

For each search result, assess:
- Is this genuinely new (not already covered in a previous briefing)?
- Does this affect any tools we track?
- Does this affect any of our projects?
- Is this high/medium/low impact?

## Step 3: Categorize Findings

Sort your findings into these buckets:

**TOOL UPDATES** — Changes to tools we already track:
- Pricing changes (free tier changes, plan additions/removals, price increases/decreases)
- New model releases or major feature additions
- Shutdowns, pivots, or acquisition announcements
- Benchmark results that affect rankings

**NEW DISCOVERIES** — Tools or services we don't track yet:
- New AI tools that fit our categories
- Existing tools we missed that are gaining traction
- New categories emerging that we should add

**INDUSTRY TRENDS** — Broader patterns:
- Funding rounds that signal market direction
- Regulatory developments (especially Canada, US, EU)
- Technical breakthroughs from research labs
- Platform shifts (e.g., new APIs, new integrations)

**PROJECT-RELEVANT** — Items that directly affect our moonshot projects:
- ai-progress-v2: Anything about AI automation, scheduled tasks, orchestration
- idea-machine: Voice AI, personal assistants, phone integration
- boundary-pusher: AI capability limits, new benchmarks
- text-to-3d-print: 3D generation, CAD AI, manufacturing
- ai-electronics-lab: PCB design, electronic design automation
- workplace-automation: Task automation, computer use, AI agents
- solo-ai-film-studio: Video generation, AI filmmaking
- medical-ai-research: Medical AI, literature search, health data
- ai-feature-film: Long-form video, narrative AI, creative tools

## Step 4: Write Briefing

Create a new briefing entry following this exact JSON structure:

```json
{
  "id": "briefing-YYYY-MM-DD",
  "date": "YYYY-MM-DD",
  "type": "daily",
  "title": "string — descriptive title reflecting the day's biggest finding",
  "summary": "2-3 sentence executive summary. Lead with the most important finding. Be specific, not vague.",
  "sections": [
    {
      "heading": "string — section title",
      "content": "string — 3-5 sentences of actual analysis. Not a summary of headlines — your synthesis of what this means, why it matters, and what to do about it.",
      "impact": "high|medium|low",
      "affectedTools": ["tool-id-from-tools-json"],
      "affectedProjects": ["project-id"],
      "actionItems": ["Specific, actionable next steps"]
    }
  ],
  "toolUpdates": [
    {
      "toolId": "tool-id-from-tools-json",
      "change": "string — what changed",
      "verified": true
    }
  ],
  "newDiscoveries": [
    {
      "name": "string",
      "url": "string",
      "category": "category-id-from-categories-json",
      "why": "string — why this matters to the project"
    }
  ],
  "generatedBy": "claude-scheduled-task"
}
```

Rules for the briefing:
- ONLY include genuinely new information not covered in previous briefings
- Every section must have real analysis, not just "X happened"
- Every actionItem must be specific enough to act on
- Use tool IDs that match tools.json (e.g., "chatgpt" not "ChatGPT")
- If nothing significant happened, say so honestly — a short briefing is better than a padded one
- If something is VERY significant (major launch, pricing earthquake, tool shutdown), set type to "alert" instead of "daily"

## Step 5: Update Data Files

If your research found changes that affect tracked tools, update tools.json:

- **Pricing changes**: Update the pricingCAD object. Recalculate CAD using the rate in meta.json.
- **New features**: Update the description field.
- **Ranking shifts**: If a tool clearly moved up or down, adjust overall and inCategory rankings. Update trend to "rising" or "declining" as appropriate.
- **Set lastVerified** to today's date for any tool you checked.

If you discovered new tools worth tracking:
- Add them to the newDiscoveries array in the briefing (do NOT add directly to tools.json — that requires human review)
- Include enough detail for the human to decide: name, URL, category, and why it matters

## CHANGE SAFEGUARDS (mandatory)

Auto-approved: updating prices/URLs/descriptions, fixing broken URLs, writing briefings, updating lastVerified dates.

REQUIRES USER ALERT (write alert briefing with type "alert", do NOT auto-execute):
- Removing any tool or source (mark as "deprecated" instead)
- Changing >20% of a data file in one update
- One tool replacing 3+ others (add "potentiallyDisplacedBy" field, don't remove)
- Creating or removing categories
- Modifying system files (CLAUDE.md, automation.json, discovery-methods.json)
- Trust score crash below 30 for a previously trusted tool
- Security incident detected for any tracked tool

Update meta.json:
- Set lastUpdated to today's date
- Update totalTools if any were added or removed

## Step 6: Append Briefing to briefings.json

Read the current briefings.json, append your new briefing to the array, and write it back. Keep all existing briefings — do not overwrite.

## Quality Standards

Before finalizing, check:
- [ ] Did I search at least 5 different sources?
- [ ] Is every claim in my briefing backed by a specific source I found today?
- [ ] Did I check if this was already covered in the last briefing?
- [ ] Are my tool IDs valid (matching tools.json)?
- [ ] Are my project IDs valid (matching projects.json)?
- [ ] Is my analysis substantive (not just restating headlines)?
- [ ] Did I update lastVerified for tools I actually checked?
- [ ] Is my briefing type correct (daily vs. alert)?

## If Nothing Significant Found

Write a minimal briefing:
```json
{
  "id": "briefing-YYYY-MM-DD",
  "date": "YYYY-MM-DD",
  "type": "daily",
  "title": "Daily Check: No Significant Developments",
  "summary": "Routine daily scan completed. No major tool launches, pricing changes, or announcements detected across monitored sources. All tracked tools appear stable.",
  "sections": [],
  "toolUpdates": [],
  "newDiscoveries": [],
  "generatedBy": "claude-scheduled-task"
}
```

This is still valuable — it confirms the system is running and the landscape is quiet.

## Error Handling

- If web search fails or returns no results: Note this in the briefing summary. Try alternative search queries. Do not fabricate findings.
- If tools.json cannot be read: Write the briefing based on web research alone. Flag the read error in the summary.
- If briefings.json cannot be read: Create a new array with just your briefing entry.
- If you are unsure whether something is true: Mark it as unverified in the briefing and add "Verify: [claim]" as an action item.
```

---

## Setup Instructions

1. Go to Claude Scheduled Tasks (or use `claude schedule create`)
2. Create a new task with schedule: `0 7 * * *` (7 AM ET daily)
3. Paste the prompt above
4. Set the working directory to the CC-AIProgress repository root
5. Ensure the task has read/write access to the `data/` directory
6. Run once manually to verify output quality before relying on scheduled execution

## Expected Output

Each run should:
- Take 2-5 minutes of Claude processing time
- Produce 1 briefing entry (500-2000 words depending on news volume)
- Update 0-10 tool entries in tools.json (most days will be 0-3)
- Update meta.json lastUpdated timestamp
- Cost approximately $0.05-0.15 per run on Claude's scheduled task pricing

## Iteration Plan

After the first week of runs, review:
1. Are the briefings catching real news? Compare against manual checks.
2. Are there too many false positives (noise)?
3. Are there false negatives (missed real developments)?
4. Adjust search queries based on what sources are most productive.
5. Consider adding/removing Priority 2 and 3 queries based on signal quality.
