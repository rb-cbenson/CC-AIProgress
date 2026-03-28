#!/usr/bin/env python3
"""
CC-AIProgress Search Engine — Provider-agnostic web search

Runs search queries from the research sweep and caches results for
AI sessions to analyze. Decouples search from analysis.

Providers (tried in order until one works):
1. Tavily — best quality, 1000 credits/month free
2. Serper — Google results via API (2500 credits free, if signed up)
3. DuckDuckGo — unlimited, no API key needed, lower quality
4. Raw RSS — no search, just pulls latest from known RSS feeds

Usage:
    python scripts/search.py                    # Run default research queries
    python scripts/search.py --query "AI news"  # Single custom query
    python scripts/search.py --status           # Show provider status and credit usage
    python scripts/search.py --provider ddg     # Force specific provider
"""

import json, sys, os, time
from datetime import datetime
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError
import xml.etree.ElementTree as ET

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE = Path(__file__).resolve().parent.parent

# Load API keys from .env
sys.path.insert(0, str(BASE / "scripts"))
from env_loader import load_env
load_env()
DATA = BASE / "data"
CACHE_PATH = DATA / "search-cache.json"
STATUS_PATH = DATA / "search-status.json"

# ============================================================
# DEFAULT RESEARCH QUERIES
# ============================================================

DEFAULT_QUERIES = [
    # Priority 1 — Major outlets
    "AI news today 2026",
    "new AI tool launch March 2026",
    "AI pricing changes 2026",
    "OpenAI announcement 2026",
    "Anthropic Claude announcement 2026",
    # Priority 2 — Community
    "Google Gemini update 2026",
    "AI robotics news 2026",
    "AI security incident vulnerability 2026",
    "Meta AI announcement 2026",
    # Priority 3 — Domain specific
    "AI agent framework new 2026",
    "open source LLM release 2026",
    "AI hardware dedicated chip 2026",
]


# ============================================================
# PROVIDER: TAVILY
# ============================================================

def search_tavily(query, max_results=5):
    """Tavily search API. 1 credit per call."""
    api_key = os.environ.get("TAVILY_API_KEY", "")
    if not api_key:
        return None, "No TAVILY_API_KEY env var"

    try:
        from tavily import TavilyClient
        client = TavilyClient(api_key=api_key)
        result = client.search(query, max_results=max_results)
        results = []
        for r in result.get("results", []):
            results.append({
                "title": r.get("title", ""),
                "url": r.get("url", ""),
                "snippet": r.get("content", "")[:500],
                "score": r.get("score", 0)
            })
        return results, None
    except ImportError:
        return None, "tavily-python not installed"
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "quota" in error_msg.lower() or "limit" in error_msg.lower():
            return None, "Tavily quota exceeded"
        return None, f"Tavily error: {error_msg[:200]}"


def research_tavily(query):
    """Tavily deep research. 5 credits per call."""
    api_key = os.environ.get("TAVILY_API_KEY", "")
    if not api_key:
        return None, "No TAVILY_API_KEY env var"

    try:
        from tavily import TavilyClient
        client = TavilyClient(api_key=api_key)
        result = client.search(query, search_depth="advanced", max_results=10)
        results = []
        for r in result.get("results", []):
            results.append({
                "title": r.get("title", ""),
                "url": r.get("url", ""),
                "snippet": r.get("content", "")[:500],
                "score": r.get("score", 0)
            })
        return results, None
    except Exception as e:
        return None, f"Tavily research error: {str(e)[:200]}"


# ============================================================
# PROVIDER: SERPER (Google Search API)
# ============================================================

def search_serper(query, max_results=5):
    """Serper.dev Google search API. Free tier: 2500 queries."""
    api_key = os.environ.get("SERPER_API_KEY", "")
    if not api_key:
        return None, "No SERPER_API_KEY env var"

    try:
        import json as j
        data = j.dumps({"q": query, "num": max_results}).encode()
        req = Request(
            "https://google.serper.dev/search",
            data=data,
            headers={"X-API-KEY": api_key, "Content-Type": "application/json"}
        )
        with urlopen(req, timeout=15) as resp:
            result = j.loads(resp.read())

        results = []
        for r in result.get("organic", [])[:max_results]:
            results.append({
                "title": r.get("title", ""),
                "url": r.get("link", ""),
                "snippet": r.get("snippet", "")[:500],
                "score": r.get("position", 0)
            })
        return results, None
    except Exception as e:
        return None, f"Serper error: {str(e)[:200]}"


# ============================================================
# PROVIDER: DUCKDUCKGO (no API key needed)
# ============================================================

def search_ddg(query, max_results=5):
    """DuckDuckGo search via duckduckgo-search package. No API key."""
    try:
        from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            raw = list(ddgs.text(query, max_results=max_results))
        results = []
        for r in raw:
            results.append({
                "title": r.get("title", ""),
                "url": r.get("href", ""),
                "snippet": r.get("body", "")[:500],
                "score": 0
            })
        return results, None
    except ImportError:
        return None, "duckduckgo-search not installed (pip install duckduckgo-search)"
    except Exception as e:
        return None, f"DDG error: {str(e)[:200]}"


# ============================================================
# PROVIDER: RSS FEEDS (last resort, no search — just latest items)
# ============================================================

RSS_FEEDS = [
    ("https://techcrunch.com/tag/artificial-intelligence/feed/", "TechCrunch AI"),
    ("https://www.theverge.com/rss/ai-artificial-intelligence/index.xml", "The Verge AI"),
    ("https://hnrss.org/newest?q=AI+OR+LLM&points=50", "Hacker News AI"),
    ("http://export.arxiv.org/rss/cs.AI", "arXiv cs.AI"),
    ("http://export.arxiv.org/rss/cs.RO", "arXiv cs.RO"),
]

def search_rss(query=None, max_results=5):
    """Pull latest items from RSS feeds. No search capability — just latest."""
    results = []
    for url, source_name in RSS_FEEDS:
        try:
            req = Request(url, headers={"User-Agent": "CC-AIProgress/1.0"})
            with urlopen(req, timeout=10) as resp:
                xml = resp.read()
            root = ET.fromstring(xml)

            # Handle both RSS and Atom formats
            items = root.findall(".//item") or root.findall(".//{http://www.w3.org/2005/Atom}entry")
            for item in items[:2]:  # 2 per feed
                title = item.findtext("title") or item.findtext("{http://www.w3.org/2005/Atom}title") or ""
                link = item.findtext("link") or ""
                if not link:
                    link_el = item.find("{http://www.w3.org/2005/Atom}link")
                    if link_el is not None:
                        link = link_el.get("href", "")
                desc = item.findtext("description") or item.findtext("{http://www.w3.org/2005/Atom}summary") or ""

                results.append({
                    "title": title[:200],
                    "url": link,
                    "snippet": desc[:300].replace("<", "").replace(">", ""),
                    "score": 0,
                    "source": source_name
                })
        except Exception:
            continue

        if len(results) >= max_results:
            break

    if results:
        return results[:max_results], None
    return None, "All RSS feeds failed"


# ============================================================
# SEARCH ENGINE — tries providers in order
# ============================================================

PROVIDERS = [
    ("tavily", search_tavily),
    ("serper", search_serper),
    ("ddg", search_ddg),
    ("rss", search_rss),
]

def search(query, max_results=5, force_provider=None):
    """Search using the best available provider with automatic fallback."""
    if force_provider:
        for name, fn in PROVIDERS:
            if name == force_provider:
                results, error = fn(query, max_results)
                return results or [], name, error
        return [], force_provider, f"Unknown provider: {force_provider}"

    for name, fn in PROVIDERS:
        results, error = fn(query, max_results)
        if results is not None:
            return results, name, None
        # Log fallback
        print(f"  [{name}] failed: {error} — trying next...")

    return [], "none", "All search providers failed"


# ============================================================
# STATUS TRACKING
# ============================================================

def load_status():
    if STATUS_PATH.exists():
        try:
            return json.load(open(STATUS_PATH, "r", encoding="utf-8"))
        except:
            pass
    return {"calls": [], "daily_totals": {}}

def save_status(status):
    with open(STATUS_PATH, "w", encoding="utf-8") as f:
        json.dump(status, f, indent=2)

def log_call(status, provider, query, result_count):
    today = datetime.now().strftime("%Y-%m-%d")
    status["calls"].append({
        "timestamp": datetime.now().isoformat(),
        "provider": provider,
        "query": query[:100],
        "results": result_count
    })
    # Keep last 200 calls
    status["calls"] = status["calls"][-200:]

    # Daily totals
    if today not in status.get("daily_totals", {}):
        status["daily_totals"] = {k: v for k, v in status.get("daily_totals", {}).items()
                                   if k >= (datetime.now().strftime("%Y-%m-01"))}  # Keep current month
        status["daily_totals"][today] = {}
    day = status["daily_totals"][today]
    day[provider] = day.get(provider, 0) + 1


# ============================================================
# MAIN
# ============================================================

def run_research(queries=None, force_provider=None):
    """Run a full set of research queries and cache results."""
    queries = queries or DEFAULT_QUERIES
    status = load_status()

    all_results = {
        "generated": datetime.now().isoformat(),
        "query_count": len(queries),
        "queries": []
    }

    providers_used = set()
    total_results = 0

    for i, query in enumerate(queries):
        print(f"  [{i+1}/{len(queries)}] {query[:60]}...")
        results, provider, error = search(query, max_results=5, force_provider=force_provider)
        providers_used.add(provider)
        total_results += len(results)

        all_results["queries"].append({
            "query": query,
            "provider": provider,
            "error": error,
            "result_count": len(results),
            "results": results
        })

        log_call(status, provider, query, len(results))

        # Brief pause between calls to respect rate limits
        if provider == "tavily":
            time.sleep(0.5)
        elif provider == "ddg":
            time.sleep(1)

    all_results["providers_used"] = sorted(providers_used)
    all_results["total_results"] = total_results

    # Save cache
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)

    save_status(status)

    print(f"\nDone: {total_results} results from {len(queries)} queries")
    print(f"Providers used: {', '.join(providers_used)}")
    print(f"Cache saved to: {CACHE_PATH}")
    return all_results


def show_status():
    status = load_status()
    today = datetime.now().strftime("%Y-%m-%d")
    month = datetime.now().strftime("%Y-%m")

    print("SEARCH ENGINE STATUS")
    print("=" * 50)

    # Monthly usage by provider
    monthly = {}
    for day, counts in status.get("daily_totals", {}).items():
        if day.startswith(month):
            for provider, count in counts.items():
                monthly[provider] = monthly.get(provider, 0) + count

    print(f"\nThis month ({month}):")
    for provider, count in sorted(monthly.items()):
        limit = ""
        if provider == "tavily":
            limit = f" / 1000 ({count/10:.0f}% used)"
        elif provider == "serper":
            limit = f" / 2500 ({count/25:.0f}% used)"
        elif provider in ("ddg", "rss"):
            limit = " (unlimited)"
        print(f"  {provider:15s} {count:5d} calls{limit}")

    today_counts = status.get("daily_totals", {}).get(today, {})
    if today_counts:
        print(f"\nToday ({today}):")
        for provider, count in today_counts.items():
            print(f"  {provider:15s} {count:5d} calls")

    # Provider availability
    print(f"\nProvider availability:")
    print(f"  tavily:  {'API key set' if os.environ.get('TAVILY_API_KEY') else 'NO API KEY'}")
    print(f"  serper:  {'API key set' if os.environ.get('SERPER_API_KEY') else 'NO API KEY (optional)'}")
    print(f"  ddg:     always available (no key needed)")
    print(f"  rss:     always available ({len(RSS_FEEDS)} feeds)")


def main():
    args = sys.argv[1:]

    if "--status" in args:
        show_status()
        return

    force = None
    if "--provider" in args:
        idx = args.index("--provider")
        if idx + 1 < len(args):
            force = args[idx + 1]

    if "--query" in args:
        idx = args.index("--query")
        if idx + 1 < len(args):
            query = " ".join(args[idx + 1:])
            results, provider, error = search(query, force_provider=force)
            print(f"Provider: {provider}")
            if error:
                print(f"Error: {error}")
            for r in results:
                print(f"  {r['title'][:70]}")
                print(f"  {r['url']}")
                print()
            return

    print("CC-AIProgress Search Engine")
    print("=" * 50)
    run_research(force_provider=force)


if __name__ == "__main__":
    main()
