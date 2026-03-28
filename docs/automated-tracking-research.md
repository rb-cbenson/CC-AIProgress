# Automated AI Tool Tracking: Research Findings

**Date:** 2026-03-27
**Goal:** Build an automated system that catches every new AI tool within days of launch.

---

## 1. How Professionals Stay on Top of New AI Tools

### Methodologies Used by Different Groups

**AI Researchers:**
- Follow arXiv daily (cs.AI, cs.CL, cs.CV, cs.LG sections)
- Monitor Papers With Code for research-to-tool pipeline
- Use RSS readers (Inoreader, Feeder) with 20+ feeds
- Follow key X/Twitter accounts for real-time announcements
- Attend NeurIPS, ICML, ICLR and track accepted papers

**VCs Tracking AI Startups:**
- Crunchbase and PitchBook for funding rounds and company data
- Product Hunt daily for new launches
- YC Demo Day announcements (twice yearly)
- AngelList / Wellfound for early-stage deal flow
- Custom deal flow dashboards pulling from multiple APIs
- Twitter/X lists of AI founders and lab researchers

**Tech Journalists:**
- Multi-source RSS pipelines (TechCrunch, The Verge, Ars Technica)
- Hacker News "Show HN" monitoring for early launches
- Reddit r/MachineLearning, r/artificial for community signal
- Embargoed press releases from AI labs
- Discord communities (Hugging Face, Midjourney, Anthropic)

**Power Users / Builders:**
- AI newsletters stack: The Rundown + TLDR AI + Ben's Bites (daily)
- GitHub Trending filtered to AI/ML topics
- Product Hunt AI topic daily
- YouTube channels (Matt Wolfe, Two Minute Papers) for demos
- Simon Willison's blog for hands-on testing

### Key Insight
The most effective professionals use a **layered system**:
1. **Automated feeds** (RSS, newsletters) for passive intake
2. **Community monitoring** (Reddit, Discord, HN) for emerging tools
3. **Directory scanning** (TAAFT, Futurepedia) for comprehensive coverage
4. **API-driven alerts** (GitHub trending, PH launches) for real-time detection

---

## 2. Every Major AI Tool Directory and Aggregator

### Tier 1: Largest AI-Specific Directories

| Directory | URL | Tools Listed | Key Feature |
|-----------|-----|-------------|-------------|
| There's An AI For That (TAAFT) | https://theresanaiforthat.com/ | 12,800+ | Task-based search, daily updates, 20M+ users |
| TopAI.tools | https://topai.tools/ | 11,000+ | 119 categories, user collections, daily updates |
| Futurepedia | https://www.futurepedia.io/ | 5,700+ | Scored ratings, pros/cons, 54+ categories |
| Toolify.ai | https://www.toolify.ai/ | 5,000+ | Website traffic insights, trend tracking, PH-like launches |
| FutureTools | https://futuretools.io/ | 3,000+ | Matt Wolfe curated, YouTube demo companion |
| LogicBalls | https://logicballs.com/ | 3,500+ | Verified listings, business-ready focus |
| OpenTools AI | https://opentools.ai/ | 3,000+ | Growing fast, surpassed Futurepedia in some metrics |
| AITopTools | https://aitoptools.com/ | 2,000+ | Feature comparisons, pricing breakdowns |

### Tier 2: General Software Directories with AI Categories

| Directory | URL | Focus | API Available? |
|-----------|-----|-------|---------------|
| Product Hunt | https://producthunt.com/topics/artificial-intelligence | Daily launches, community upvotes | Yes (GraphQL V2) |
| G2 | https://g2.com/ | Enterprise reviews, G2 Grid benchmarking | Limited |
| Capterra | https://capterra.com/ | SMB tool discovery, Gartner-owned | No public API |
| SaaSHub | https://saashub.com/ | Alternatives comparison, community reviews | No public API |
| AlternativeTo | https://alternativeto.net/ | "Find alternatives to X" | No public API |
| GetApp | https://getapp.com/ | Gartner-owned, cross-listed with Capterra | No public API |
| TrustRadius | https://trustradius.com/ | In-depth authenticated reviews | Limited |
| SourceForge | https://sourceforge.net/ | Open-source software focus | No |
| PeerSpot | https://peerspot.com/ | Enterprise buyer reviews | No |
| Crozdesk | https://crozdesk.com/ | Business software discovery | No |

### Tier 3: Startup Launch Platforms

| Platform | URL | Focus |
|----------|-----|-------|
| BetaList | https://betalist.com/ | Pre-launch / beta startups |
| Indie Hackers | https://indiehackers.com/ | Founder community, product showcases |
| Wellfound (AngelList) | https://wellfound.com/ | Startup jobs + company profiles |
| StartupBase | https://startupbase.io/ | Startup directory for makers |
| Launching Next | https://launchingnext.com/ | Early adopter discovery |
| SideProjectors | https://sideprojectors.com/ | Side project marketplace |
| DevHunt | https://devhunt.org/ | Developer tool launches |

### Tier 4: Niche / Emerging AI Directories

| Directory | URL | Notes |
|-----------|-----|-------|
| Dang.ai | https://dang.ai/ | Growing AI directory, clean submission |
| AIChief | https://aichief.com/ | Curated "#1 AI Tools Directory" |
| AI Tool Directory | https://aitoolsdirectory.com/ | General AI tools listing |
| Stackviv | https://stackviv.com/ | AI tool discovery |
| ToolFinder | https://toolfinder.co/ | AI tool search |
| Tool Pilot | https://toolpilot.ai/ | AI tool reviews |
| ToolPasta | https://toolpasta.com/ | By Robopost |
| Sales Tools AI | https://salestools.ai/ | Sales-specific AI tools |
| AIBase | https://aibase.com/ | Comprehensive tool database |
| AI Tool Discovery | https://aitooldiscovery.com/ | Reddit-sourced AI tool rankings |

### Curated Lists of Directories
- **GitHub: best-of-ai/ai-directories** - Community-maintained list
- **GitHub: mahseema/awesome-saas-directories** - 80+ SaaS directories with DR scores
- **ListMyAI: 50+ Best AI Directories** - https://listmyai.net/blog/ai-directories-submit-your-tool

---

## 3. Automated Discovery Channels

### RSS Feeds That Announce New Tools

| Feed | URL | What It Catches |
|------|-----|----------------|
| TechCrunch AI | https://techcrunch.com/category/artificial-intelligence/feed/ | Funding, launches, acquisitions |
| The Verge AI | https://www.theverge.com/ai-artificial-intelligence/rss/index.xml | Consumer AI product news |
| Ars Technica AI | https://arstechnica.com/ai/feed/ | Technical AI news |
| VentureBeat AI | https://venturebeat.com/ai/feed/ | Enterprise AI news |
| OpenAI Blog | https://openai.com/blog/rss/ | OpenAI releases |
| Anthropic Blog | https://www.anthropic.com/blog/rss | Claude releases |
| Google AI Blog | https://blog.google/technology/ai/rss/ | Google AI releases |
| Hugging Face Blog | https://huggingface.co/blog/feed.xml | Open-source model releases |
| GitHub Blog AI/ML | https://github.blog/ai-and-ml/feed/ | GitHub AI features, trending |
| arXiv cs.AI | https://rss.arxiv.org/rss/cs.AI | New AI research papers |
| arXiv cs.CL | https://rss.arxiv.org/rss/cs.CL | NLP/LLM papers |
| Papers With Code | https://paperswithcode.com/latest | Research with code releases |

**Curated RSS Collection:** https://github.com/vishalshar/awesome_ML_AI_RSS_feed

### X/Twitter Accounts for AI Tool Launches

**Lab / Company Accounts:**
- @OpenAI - Official OpenAI announcements
- @AnthropicAI - Anthropic/Claude announcements
- @GoogleDeepMind - DeepMind releases
- @MetaAI - Meta AI releases
- @xaboratory - xAI/Grok announcements
- @MistralAI - Mistral releases

**Curators / Journalists:**
- @rowancheung - The Rundown AI (567K followers), daily AI roundups
- @zaaboramit - Superhuman AI newsletter
- @bentossell - Ben's Bites, AI startup launches
- @maboroshi - Matt Wolfe / FutureTools
- @AINEwsfeed - AI news aggregation account

**Researchers / Thought Leaders:**
- @AndrewYNg - Andrew Ng, The Batch
- @ylecun - Yann LeCun, Meta Chief AI Scientist
- @demaboroshi - Demis Hassabis, DeepMind CEO
- @AravSrinivas - Perplexity AI CEO
- @siaborowi - Simon Willison, hands-on AI testing
- @kaborarpathy - Andrej Karpathy, ex-OpenAI/Tesla

**Full Lists:**
- Amperly: 31 Best AI Twitter Accounts - https://amperly.com/best-artificial-intelligence-twitter-accounts/
- Feedspot Top 100 AI Influencers - https://x.feedspot.com/artificial_intelligence_twitter_influencers/
- KDnuggets: 10 Best X Accounts for LLM Updates - https://www.kdnuggets.com/10-best-x-twitter-accounts-to-follow-for-llm-updates

### GitHub Trending for AI

- **GitHub Trending page:** https://github.com/trending?since=daily (filter by language: Python)
- **No official API** -- use community solutions:
  - huchenme/github-trending-api: https://github.com/huchenme/github-trending-api
  - NiklasTiede/Github-Trending-API: https://github.com/NiklasTiede/Github-Trending-API (FastAPI)
  - Apify Actor: https://apify.com/saswave/github-trending-repositories-developers/api

### Papers With Code (Research to Tool Pipeline)

- **Website:** https://paperswithcode.com/
- **REST API:** https://paperswithcode.com/api/v1/docs/
- **Python Client:** https://github.com/paperswithcode/paperswithcode-client
- **Key endpoints:** paper_list, paper_repository_list, task_list, method_list, dataset_list
- **Use case:** Monitor new papers that include code repos -- these often become tools within weeks

### Hacker News "Show HN" AI Posts

- **Show HN page:** https://news.ycombinator.com/show
- **Firebase API:** https://hacker-news.firebaseio.com/v0/
  - `/v0/showstories.json` - Up to 200 latest Show HN stories
  - `/v0/topstories.json` - Top 500 stories
  - `/v0/newstories.json` - Newest 500 stories
- **Algolia Search API:** http://hn.algolia.com/api/v1/search?tags=show_hn&query=AI
  - Filter by tags: `show_hn`, `story`, `comment`
  - Search by keyword: add `&query=AI` or `&query=LLM`
- **No rate limit** on Firebase API
- **No API key required**
- **MCP Server:** https://github.com/karanb192/hn-mcp (for AI assistant integration)

### Reddit AI Communities

**Key Subreddits for Tool Discovery:**
- r/MachineLearning (3M members) - Research + tools tagged [P] for projects
- r/artificial / r/ArtificialIntelligence (1.4M) - Broad AI news + tools
- r/SideProject - Indie AI tool launches
- r/ChatGPT (9M) - ChatGPT ecosystem tools
- r/LocalLLaMA - Open-source model tools
- r/StableDiffusion - Image generation tools
- r/generativeAI - Multi-modal AI tools

**API Access:** Reddit API via OAuth, 100 QPM free tier (non-commercial)

### Product Hunt Daily AI Launches

- **AI Topic Page:** https://producthunt.com/topics/artificial-intelligence
- **Daily launches:** New AI products every day with community upvotes
- **API:** GraphQL V2 at https://api.producthunt.com/v2/docs
- **Scopes:** Public (read), Private (user-specific), Write (actions)

### YC Demo Day Announcements

- Twice yearly (Winter + Summer batches)
- YC company directory: https://www.ycombinator.com/companies
- Filter by "Artificial Intelligence" tag
- No public API, but structured HTML is scrapeable

### AI Newsletters (Automated Digest)

| Newsletter | Frequency | Subscribers | Best For |
|------------|-----------|-------------|----------|
| The Rundown AI | Daily | 1.75M+ | Comprehensive daily briefing |
| TLDR AI | Daily | 1.25M+ | Technical focus, paper summaries |
| Superhuman AI | Daily | 1M+ | Tool of the day + prompt |
| The Neuron | Daily | 550K+ | Beginner-friendly, 3-min read |
| Ben's Bites | 2x/week | 120K+ | Startup launches, builder focus |
| The Batch (Andrew Ng) | Weekly | 500K+ | Research + authoritative analysis |
| Neatprompts | Weekly | 110K+ | Prompt engineering, execution |
| Future Tools (Matt Wolfe) | Weekly | 300K+ | Tool curation with YouTube demos |

---

## 4. APIs and Data Sources for Programmatic Tracking

### Free APIs (No Key or Free Tier)

| API | URL | Data | Auth | Rate Limit |
|-----|-----|------|------|-----------|
| Hacker News Firebase | https://hacker-news.firebaseio.com/v0/ | Stories, comments, users | None | No limit |
| Hacker News Algolia | http://hn.algolia.com/api | Full-text search of HN | None | Generous |
| Papers With Code | https://paperswithcode.com/api/v1/ | Papers, repos, tasks, benchmarks | None | Moderate |
| arXiv API | https://arxiv.org/help/api | Research papers metadata | None | 1 req/3 sec |
| GitHub Trending (unofficial) | github-trending-api (npm/self-host) | Trending repos/devs | None | N/A |

### APIs Requiring Free Registration

| API | URL | Data | Free Tier |
|-----|-----|------|-----------|
| Product Hunt V2 | https://api.producthunt.com/v2/docs | Launches, upvotes, topics | OAuth, public scope |
| GitHub REST API | https://docs.github.com/en/rest | Repos, stars, activity | 60 req/hr unauth, 5000/hr with token |
| Reddit API | https://www.reddit.com/dev/api/ | Posts, comments, subreddits | 100 QPM (non-commercial, OAuth) |
| Google Trends API | https://developers.google.com/search/apis/trends | Search trend data | Alpha access (apply), rolling 5-year window |
| HuggingFace API | https://huggingface.co/docs/api-inference | Models, datasets, spaces | Free tier available |

### Paid APIs

| API | URL | Data | Pricing |
|-----|-----|------|---------|
| Crunchbase | https://data.crunchbase.com/docs | Company profiles, funding, M&A | Free (basic), $49/mo (Pro), API = enterprise custom |
| Reddit (Commercial) | https://www.reddit.com/dev/api/ | Full commercial access | $12,000+/year |
| Google Trends (via scraping) | pytrends (unofficial) | Trend data | Free but fragile |

### Scraper-Based Data Sources (via Apify or self-built)

| Source | Tool | Data | Cost |
|--------|------|------|------|
| TAAFT (full database) | Apify: lovely_sequoia/taaft-scraper | 46,500+ tools, 29+ fields each | Apify credits |
| TAAFT (basic) | Apify: fatihtahta scraper | Categories, frontpage, search | $20/mo |
| GitHub Trending | Apify: saswave actor | Trending repos + devs | Apify credits |
| Product Hunt | Apify: various actors | Daily launches | Apify credits |

### Multi-Source Aggregation Tools

| Tool | URL | What It Does |
|------|-----|-------------|
| idea-reality-mcp | https://github.com/mnemox-ai/idea-reality-mcp | MCP server scanning GitHub, HN, npm, PyPI, Product Hunt simultaneously |
| Crawl4AI | https://github.com/unclecode/crawl4ai | Open-source LLM-friendly web crawler for building custom scrapers |
| Firecrawl | https://github.com/firecrawl/firecrawl | Converts any URL to structured data, batch processing, change tracking |

---

## 5. Recommended Architecture for Automated Tracking

### Data Source Priority (by speed of detection)

1. **Same day:** Hacker News Show HN, Product Hunt daily, GitHub Trending, X/Twitter
2. **Within 2-3 days:** Reddit posts, AI newsletters, TechCrunch/Verge coverage
3. **Within 1 week:** AI directories (TAAFT, Futurepedia), blog posts, YouTube reviews
4. **Within 2-4 weeks:** G2/Capterra reviews, Crunchbase funding data, benchmark results

### Proposed Pipeline

```
[Scheduled Triggers - GitHub Actions / Cron]
        |
        v
[Data Collection Layer]
  - HN Firebase API --> /v0/showstories + Algolia search "AI"
  - Product Hunt API --> Daily AI topic launches
  - GitHub Trending API --> Python/ML repos, daily
  - Reddit API --> r/MachineLearning [P] tags, r/SideProject "AI"
  - Papers With Code API --> New papers with repos
  - RSS Feeds --> 15+ AI blogs/labs (TechCrunch, OpenAI, etc.)
  - TAAFT Scraper --> New tools added today
        |
        v
[Deduplication & Classification]
  - Match by name, URL, GitHub repo
  - Classify by category (text, image, code, audio, etc.)
  - Score by signal strength (upvotes, stars, mentions)
        |
        v
[AI Summarization Layer]
  - Claude/GPT summarizes each new tool
  - Extract: name, category, pricing, key features
  - Match to existing tools.json schema
        |
        v
[Output]
  - Update data/tools.json with new entries
  - Update data/meta.json counts
  - Generate weekly digest
  - Flag "Try This ASAP" candidates for tests.json
```

### Minimum Viable Version (Free, No API Keys)

These three sources alone would catch ~80% of new AI tools within days:

1. **Hacker News Show HN** (Firebase API, free, no auth, no rate limit)
   - Poll `/v0/showstories.json` daily
   - Search Algolia for "AI", "LLM", "GPT" in Show HN

2. **GitHub Trending** (unofficial API or scrape)
   - Daily trending Python repos
   - Filter by AI/ML keywords in description

3. **RSS Feeds** (free, no auth)
   - TechCrunch AI, OpenAI Blog, Anthropic Blog, HuggingFace Blog
   - 15-minute poll interval

### Full Version (With API Keys)

Add these for comprehensive coverage:

4. **Product Hunt API** (free OAuth) - Daily AI launches
5. **Reddit API** (free non-commercial) - r/MachineLearning, r/SideProject
6. **Papers With Code API** (free) - Research-to-tool pipeline
7. **Google Trends API** (alpha, apply) - Detect rising AI tool names
8. **Crunchbase** (paid) - Funding rounds for AI startups
9. **TAAFT Scraper** (Apify credits) - Comprehensive directory monitoring

---

## Sources

- [Futurepedia AI Tools Directory](https://www.futurepedia.io/ai-tools)
- [AI Tool Directories Compared: Top 15 Ranked by Traffic](https://aiblewmymind.substack.com/p/how-to-find-the-right-ai-tools-for)
- [Best Free AI Tools Directories 2026](https://logicballs.com/blog/best-free-ai-tools-directories-2026)
- [50+ Best AI Directories to Submit Your Tool](https://listmyai.net/blog/ai-directories-submit-your-tool)
- [Top AI SaaS Listing Platforms 2025](https://www.rivalsee.com/blog/best-ai-saas-listing-platforms-directories)
- [awesome-saas-directories on GitHub](https://github.com/mahseema/awesome-saas-directories)
- [Build Your Own AI News Bot with Claude + GitHub Actions](https://medium.com/@fengliu_367/build-your-own-ai-news-bot-automated-daily-digests-with-claude-and-github-actions-bc3d48e67d98)
- [awesome_ML_AI_RSS_feed on GitHub](https://github.com/vishalshar/awesome_ML_AI_RSS_feed)
- [AI Tool Discovery Guide 2025 - PeerPush](https://peerpush.net/blog/ai-tool-discovery-guide-2025)
- [Hacker News Official API on GitHub](https://github.com/HackerNews/API)
- [Hacker News API: Complete Guide (Firebase + Algolia)](https://cotera.co/articles/hacker-news-api-guide)
- [Product Hunt API V2 Documentation](https://api.producthunt.com/v2/docs)
- [Product Hunt API Wiki on GitHub](https://github.com/producthunt/producthunt-api/wiki/Product-Hunt-APIs)
- [idea-reality-mcp on GitHub](https://github.com/mnemox-ai/idea-reality-mcp)
- [Papers With Code API Docs](https://paperswithcode.com/api/v1/docs/)
- [Papers With Code Python Client](https://github.com/paperswithcode/paperswithcode-client)
- [Google Trends API (Alpha) Announcement](https://developers.google.com/search/blog/2025/07/trends-api)
- [Google Trends API Documentation](https://developers.google.com/search/apis/trends)
- [Crunchbase Data API Docs](https://data.crunchbase.com/docs/using-the-api)
- [Crunchbase Pricing Review 2026](https://easyvc.ai/vs/crunchbase-pricing/)
- [Reddit Data API Wiki](https://support.reddithelp.com/hc/en-us/articles/16160319875092-Reddit-Data-API-Wiki)
- [Reddit API Rate Limits 2026 Guide](https://painonsocial.com/blog/reddit-api-rate-limits-guide)
- [Complete Guide to Reddit API Pricing 2026](https://www.bbntimes.com/technology/complete-guide-to-reddit-api-pricing-and-usage-tiers-in-2026)
- [Top 10 AI Newsletters 2026 - DemandSage](https://www.demandsage.com/ai-newsletters/)
- [15 Best AI Newsletters 2026 - Readless](https://www.readless.app/newsletters/best-ai-newsletters-2025)
- [31 Best AI Twitter Accounts 2026 - Amperly](https://amperly.com/best-artificial-intelligence-twitter-accounts/)
- [Top 13 AI Influencers on X 2026 - TweetStorm](https://tweetstorm.ai/blog/top-ai-influencers)
- [Top 100 AI Influencers - Feedspot](https://x.feedspot.com/artificial_intelligence_twitter_influencers/)
- [TAAFT Scraper on Apify](https://apify.com/lovely_sequoia/taaft-scraper)
- [Stanford HAI AI Index Report 2025](https://hai-production.s3.amazonaws.com/files/hai_ai_index_report_2025.pdf)
- [GitHub Trending API (huchenme)](https://github.com/huchenme/github-trending-api)
- [Crawl4AI on GitHub](https://github.com/unclecode/crawl4ai)
- [Firecrawl on GitHub](https://github.com/firecrawl/firecrawl)
- [hn-mcp: Hacker News MCP Server](https://github.com/karanb192/hn-mcp)
