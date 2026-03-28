#!/usr/bin/env python3
"""
CC-AIProgress Gap Analysis — Systematic Blind Spot Detection

Cross-references all data files to find things the system SHOULD cover but doesn't.
Run periodically (weekly recommended) or before research sweeps.

Usage:
    python scripts/gap-analysis.py           # Full analysis
    python scripts/gap-analysis.py --brief   # Summary only
"""

import json, sys, os
from collections import Counter
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE = Path(__file__).resolve().parent.parent / "data"

def load(name):
    try:
        with open(BASE / f"{name}.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"WARNING: Could not load {name}.json: {e}")
        return None

def check_developer_coverage(tools, sources):
    """For every developer in tools.json, check if news-sources.json covers them."""
    gaps = []
    developers = {}
    for t in tools:
        dev = t.get("developer", "Unknown")
        if dev not in developers:
            developers[dev] = []
        developers[dev].append(t["id"])

    source_text = " ".join([
        (s.get("name", "") + " " + s.get("url", "") + " " + s.get("description", "")).lower()
        for s in sources
    ])

    for dev, tool_ids in sorted(developers.items(), key=lambda x: -len(x[1])):
        dev_lower = dev.lower().replace(" inc.", "").replace(" inc", "").replace(" ltd", "").replace(" ai", "").strip()
        # Check if developer name appears in any source
        words = [w for w in dev_lower.split() if len(w) > 2 and w not in ("the", "open", "source", "community", "labs")]
        found = any(w in source_text for w in words) if words else False
        if not found:
            gaps.append({"developer": dev, "tools": tool_ids, "tool_count": len(tool_ids)})

    return sorted(gaps, key=lambda x: -x["tool_count"])

def check_project_tool_alignment(projects, tools):
    """For every tool referenced in projects, check if it exists in tools.json."""
    tool_ids = {t["id"] for t in tools}
    gaps = []
    for p in projects:
        missing = set()
        tracked = set()
        for phase in p.get("phases", []):
            for ai_tool in phase.get("aiTools", []):
                tool_ref = ai_tool.lower().replace(" ", "-")
                if tool_ref in tool_ids:
                    tracked.add(tool_ref)
                else:
                    missing.add(ai_tool)
        if missing:
            gaps.append({
                "project": p["name"],
                "project_id": p["id"],
                "tracked": len(tracked),
                "missing": sorted(missing),
                "missing_count": len(missing)
            })
    return gaps

def check_category_balance(tools, categories):
    """Flag categories that are too small or too large."""
    counts = Counter(t["category"] for t in tools)
    cat_ids = {c["id"] for c in categories}
    gaps = []
    for c in categories:
        count = counts.get(c["id"], 0)
        if count < 5:
            gaps.append({"category": c["name"], "id": c["id"], "count": count, "issue": "underweight (<5 tools)"})
        elif count >= 25:
            gaps.append({"category": c["name"], "id": c["id"], "count": count, "issue": "at split threshold (>=25)"})
    # Check for tools in unknown categories
    for cat, count in counts.items():
        if cat not in cat_ids:
            gaps.append({"category": cat, "id": cat, "count": count, "issue": "INVALID - category not in categories.json"})
    return gaps

def check_source_type_coverage(sources):
    """Check for missing source types that should exist."""
    existing_types = Counter(s.get("type", "unknown") for s in sources)
    expected_types = {
        "patent-database": "Google Patents, USPTO, WIPO — earliest signal of what companies build",
        "job-board": "AI job postings signal what's being built next",
        "academic-lab": "MIT CSAIL, Stanford HAI, Mila — where breakthroughs originate",
        "vc-blog": "a16z, Sequoia, Accel — funding signals which startups matter",
        "benchmark": "LMSYS Chatbot Arena, Open LLM Leaderboard — real-time model rankings",
        "think-tank": "Brookings, CSET, RAND — policy intelligence",
        "government": "NIST AI, EU AI Office, CIFAR — regulatory signals",
        "standards-body": "ISO AI, IEEE, NIST RMF — compliance requirements",
        "podcast": "AI podcast feeds for audio monitoring",
        "youtube": "AI YouTube channels for video content mining",
        "substack": "Independent AI researcher newsletters",
        "app-store": "App store AI categories — consumer tool tracking"
    }
    gaps = []
    for typ, reason in expected_types.items():
        count = existing_types.get(typ, 0)
        if count == 0:
            gaps.append({"type": typ, "count": 0, "reason": reason})
        elif count < 3:
            gaps.append({"type": typ, "count": count, "reason": f"Only {count} source(s) — {reason}"})
    return gaps

def check_geographic_coverage(sources, tools):
    """Check if non-English sources cover countries where tools are being built."""
    source_countries = Counter()
    for s in sources:
        country = s.get("country", "")
        if country:
            source_countries[country] += 1

    # Countries with significant AI ecosystems that should have dedicated sources
    expected_countries = {
        "India": "Krutrim, Sarvam AI, massive developer community",
        "Israel": "AI21 Labs, Run:ai, Hailo, D-ID",
        "Brazil": "Growing AI scene, Portuguese-language community",
        "Canada": "Cohere, Vector Institute, Mila, CIFAR — user's home country",
        "Singapore": "AI Singapore, Sea AI Lab, SEA tech hub",
        "Sweden": "Eriksson AI, KTH research",
        "Netherlands": "ASML AI, TU Delft, Philips AI"
    }
    gaps = []
    for country, reason in expected_countries.items():
        count = source_countries.get(country, 0)
        if count == 0:
            gaps.append({"country": country, "sources": 0, "reason": reason})
        elif count < 2:
            gaps.append({"country": country, "sources": count, "reason": f"Only {count} — {reason}"})
    return gaps

def check_staleness(tools):
    """Check for tools with old lastVerified dates."""
    from datetime import datetime, timedelta
    today = datetime.now()
    buckets = {"over_90_days": [], "over_60_days": [], "over_30_days": [], "fresh": []}
    for t in tools:
        lv = t.get("lastVerified", "")
        if not lv:
            buckets["over_90_days"].append(t["id"])
            continue
        try:
            d = datetime.fromisoformat(lv)
            delta = (today - d).days
            if delta > 90:
                buckets["over_90_days"].append(t["id"])
            elif delta > 60:
                buckets["over_60_days"].append(t["id"])
            elif delta > 30:
                buckets["over_30_days"].append(t["id"])
            else:
                buckets["fresh"].append(t["id"])
        except:
            buckets["over_90_days"].append(t["id"])
    return buckets

def check_developer_duplicates(tools):
    """Find developer name inconsistencies."""
    devs = {}
    for t in tools:
        dev = t.get("developer", "")
        normalized = dev.lower().strip().rstrip(".")
        if normalized not in devs:
            devs[normalized] = set()
        devs[normalized].add(dev)
    return {k: sorted(v) for k, v in devs.items() if len(v) > 1}

def main():
    brief = "--brief" in sys.argv

    tools = load("tools") or []
    sources = load("news-sources") or []
    categories = load("categories") or []
    projects = load("projects") or []

    print("=" * 60)
    print("CC-AIProgress Gap Analysis")
    print("=" * 60)
    print(f"Data: {len(tools)} tools, {len(sources)} sources, {len(categories)} categories, {len(projects)} projects\n")

    # 1. Developer coverage
    dev_gaps = check_developer_coverage(tools, sources)
    multi_tool_devs = [g for g in dev_gaps if g["tool_count"] > 1]
    print(f"DEVELOPER COVERAGE: {len(dev_gaps)} developers with no matching source")
    print(f"  Priority (multi-tool developers): {len(multi_tool_devs)}")
    if not brief:
        for g in dev_gaps[:15]:
            print(f"  - {g['developer']} ({g['tool_count']} tools: {', '.join(g['tools'][:3])}{'...' if len(g['tools'])>3 else ''})")
    print()

    # 2. Project-tool alignment
    proj_gaps = check_project_tool_alignment(projects, tools)
    total_missing = sum(g["missing_count"] for g in proj_gaps)
    print(f"PROJECT-TOOL ALIGNMENT: {total_missing} tool references not in tools.json")
    if not brief:
        for g in proj_gaps:
            print(f"  - {g['project']}: {g['tracked']} tracked, {g['missing_count']} missing")
            for m in g["missing"][:5]:
                print(f"      missing: {m}")
            if len(g["missing"]) > 5:
                print(f"      ... and {len(g['missing'])-5} more")
    print()

    # 3. Category balance
    cat_gaps = check_category_balance(tools, categories)
    print(f"CATEGORY BALANCE: {len(cat_gaps)} categories flagged")
    for g in cat_gaps:
        print(f"  - {g['category']} ({g['id']}): {g['count']} tools — {g['issue']}")
    print()

    # 4. Source type coverage
    type_gaps = check_source_type_coverage(sources)
    print(f"MISSING SOURCE TYPES: {len(type_gaps)} types missing or underweight")
    if not brief:
        for g in type_gaps:
            print(f"  - {g['type']}: {g['count']} sources — {g['reason']}")
    print()

    # 5. Geographic coverage
    geo_gaps = check_geographic_coverage(sources, tools)
    print(f"GEOGRAPHIC GAPS: {len(geo_gaps)} countries underrepresented")
    if not brief:
        for g in geo_gaps:
            print(f"  - {g['country']}: {g['sources']} sources — {g['reason']}")
    print()

    # 6. Staleness
    staleness = check_staleness(tools)
    print(f"STALENESS: {len(staleness['over_90_days'])} tools >90d, {len(staleness['over_60_days'])} >60d, {len(staleness['over_30_days'])} >30d, {len(staleness['fresh'])} fresh")
    print()

    # 7. Developer duplicates
    dupes = check_developer_duplicates(tools)
    if dupes:
        print(f"DEVELOPER NAME DUPLICATES: {len(dupes)} inconsistencies")
        if not brief:
            for norm, variants in dupes.items():
                print(f"  - {' vs '.join(variants)}")
    print()

    # Summary
    print("=" * 60)
    print("PRIORITY FIXES:")
    print("=" * 60)
    if multi_tool_devs:
        print(f"1. Add sources for {len(multi_tool_devs)} multi-tool developers (highest coverage impact)")
    if total_missing > 0:
        print(f"2. Add {total_missing} missing tools referenced by projects")
    if type_gaps:
        missing_types = [g["type"] for g in type_gaps if g["count"] == 0]
        print(f"3. Add {len(missing_types)} missing source types: {', '.join(missing_types[:5])}...")
    if geo_gaps:
        print(f"4. Add sources for {len(geo_gaps)} underrepresented countries")
    if dupes:
        print(f"5. Fix {len(dupes)} developer name inconsistencies")

if __name__ == "__main__":
    main()
