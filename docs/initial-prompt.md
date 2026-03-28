# Initial Prompt — Preserved Verbatim

## Original Prompt (2026-03-27)

Project: CC-AIProgress

Objective:

Keep up to date with AI automatically

Goals:

Keeping track of AI progress / Stay abreast of AI news
What AI is capable of doing and what programs to use for what?
Ensuring we don't stay with "old" technology for too long
Be able to know what AI to try / experiment with

Requirements:

Potentially create as modular setup
Create it as a program which can be easily viewed in Windows or on a Chromebook (without developer access / Linux ideally)
Versioning progress of this project
Able to revert (in this project) easily - potentially using backups or GitHub
If an executable is needed / Chromebook APP, test first before creating (save tokens)
Create a file noting this initial prompt (keep this as is for reference) then update (in a separate section) as new suggestions are made and decisions are taken
Try to get as far as possible without (my) user input, but ask for my opinion before making any major changes / decisions.

Brainstorming:

Lots of research and group by general categories
Subcategories into free vs paid options for each (include pricing in CAD)
Search online for sites trying to keep up with AI progress
Search online for user reviews, articles, blogs, press releases
Include a section below this for specific applications which are not "general use" but perhaps targeted to specific fields
Create a ranked list for each category, and think about how to treat programs which overlap multiple categories
This can be run "in the background" to stay up to date
Use AI to periodically check if whatever approach reached here should be updated based on news and adapt accordingly (prompt the user?)
Might need several iterations based on user preference
Try to be as complete as possible - you have the entire Internet at your fingertips, and any software program can be downloaded

Considerations:

Easy to view interface: pictures are always nice (I'm a human after all)
Deduplication of everything found (news, articles, tools etc.)
Consider if (and how) AI tools can be used together (AI programming with AI video for example)
Any potential issues with each
Create mutiple tabs if needed?
Regulations which come out (Canada, USA, World etc.)
AI run in the cloud vs. Desktop (like Claude Desktop), or entirely locally?
At what point is it worth NOT considering something? Don't want to be overwhelmed
Can potentially still use AI; but let's try to keep it platform agnostic (potentially via a saved prompt? Open to ideas) and a way to easily recreate it if moved from Claude to another program (ChatGPT for example)
If there's something which can do everyhing outlined here, it's worth noting.
What might be missing from this prompt? Is it worth including what hardware is used / hardware progress?

Examples:

Examples (AI news): RSS feeds ; scraper tools for websites; https://www.therundown.ai/ ; https://www.superhuman.ai/ ; https://ised-isde.canada.ca/site/ised/en/artificial-intelligence-ecosystem https://www.reddit.com/r/AI_Agents/comments/1r4w3aw/how_do_you_stay_up_to_date_with_ai_especially/
Examples (AI tools): ChatGPT from Anthropic (text generation, programming); Claude from Anthropic; Copilot; Gemini; https://chat.z.ai/ etc.
Examples (Categorization): Research, creative writing, media generation (images, videos), programming (stand-alone, website, smartphone APPs, 3D modeling, Electronic design etc.) Feel free to create appropriate categories after all AI have been found) and update as needed
Examples (Ranking): What's best for each category (and why); Best value; Which can do many things (not limited to one category) as well as "up and coming" (recently released as well as being talked about)
Examples (Specific AI tools): https://www.notion.com/

---

## Additional Requirements (2026-03-27)

- Implement Claude auto mode (work autonomously)
- Comparison & Testing: "Try This ASAP" recommendations by category and overall with guided step-by-step instructions
- Testing can involve using multiple tools together, including hardware requirements
- User can choose to: Try, Save for Later, or Delete tests
- Save for Later can check if test is still valid or if something better exists
- Additional AI tools: Kimi, Suno, Qwen, DeepSeek, MeetCody, IDA Pro, Microsoft Copilot
- Additional news: Matt Brown YouTube (https://www.youtube.com/@mattbrwn)
- Example test: Video creation — determine best AI for video gen, auto-generate video with user prompt

---

## Decisions Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-03-27 | Single-page HTML dashboard with JSON data | No build tools needed, works in any browser, easy to version control |
| 2026-03-27 | GitHub Pages for hosting | Free, automatic SSL, tied to version control |
| 2026-03-27 | Tabler UI + ApexCharts via CDN | Professional look without framework complexity |
| 2026-03-27 | Prices in CAD | User is in Canada |
| 2026-03-27 | localStorage for user state (tried/saved/deleted) | No backend needed, works offline |
| 2026-03-27 | Added "Try This ASAP" tab as primary feature | User identified this as potentially most useful part |
