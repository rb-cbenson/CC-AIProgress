#!/usr/bin/env python3
"""
CC-AIProgress Self-Improvement Engine

Runs all improvement checks in sequence, generates a prioritized action list,
and optionally applies safe auto-fixes. Designed to be run at the start of
every AI session or on a schedule.

Usage:
    python scripts/self-improve.py              # Full analysis + auto-fix safe items
    python scripts/self-improve.py --dry-run    # Analysis only, no changes
    python scripts/self-improve.py --report     # Generate improvement-report.json

The engine improves itself: when a new type of gap is discovered manually,
add a check function here so it's caught automatically next time.
"""

import json, sys, os
from datetime import datetime, timedelta
from collections import Counter
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE = Path(__file__).resolve().parent.parent / "data"
DRY_RUN = "--dry-run" in sys.argv
REPORT = "--report" in sys.argv

def load(name):
    try:
        with open(BASE / f"{name}.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return None

def save(name, data):
    if DRY_RUN:
        print(f"  [DRY RUN] Would write {name}.json")
        return
    with open(BASE / f"{name}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  [SAVED] {name}.json")

actions = []  # Collected improvement actions

def action(severity, category, description, auto_fixable=False, fix_fn=None):
    """Register an improvement action."""
    entry = {
        "severity": severity,
        "category": category,
        "description": description,
        "auto_fixable": auto_fixable,
        "timestamp": datetime.now().isoformat()
    }
    actions.append(entry)
    icon = {"critical": "!!!", "moderate": " ! ", "minor": " . ", "info": "   "}
    print(f"  [{icon.get(severity, '   ')}] {description}")
    if auto_fixable and fix_fn and not DRY_RUN:
        fix_fn()
        print(f"        -> AUTO-FIXED")


# ============================================================
# CHECK 1: Data file integrity
# ============================================================
def check_data_integrity():
    print("\n1. DATA INTEGRITY")
    required_files = [
        "tools", "news-sources", "categories", "meta", "briefings",
        "automation", "trust-framework", "discovery-methods", "projects",
        "strategies", "workflows", "tests", "regulations",
        "programmatic-sources"
    ]
    for f in required_files:
        data = load(f)
        if data is None:
            action("critical", "integrity", f"{f}.json is missing or corrupt")
        elif isinstance(data, list) and len(data) == 0:
            action("moderate", "integrity", f"{f}.json is empty (0 entries)")


# ============================================================
# CHECK 2: Cross-reference consistency
# ============================================================
def check_cross_references():
    print("\n2. CROSS-REFERENCE CONSISTENCY")
    tools = load("tools") or []
    categories = load("categories") or []
    trust = load("trust-framework") or {}
    meta = load("meta") or {}

    cat_ids = {c["id"] for c in categories}
    tool_ids = {t["id"] for t in tools}

    # Tools referencing invalid categories
    for t in tools:
        if t.get("category") not in cat_ids:
            action("critical", "cross-ref",
                   f"Tool '{t['id']}' references invalid category '{t.get('category')}'")

    # Trust framework incidents referencing unknown tools
    for inc in trust.get("knownIncidents", []):
        if inc.get("tool") and inc["tool"] not in tool_ids:
            # Some incidents are for non-tracked tools (chrome extensions etc) - only warn
            action("minor", "cross-ref",
                   f"Trust incident references '{inc['tool']}' which is not in tools.json")

    # Meta.json tool count mismatch
    if meta.get("totalTools") != len(tools):
        def fix_meta_count():
            meta["totalTools"] = len(tools)
            save("meta", meta)
        action("moderate", "cross-ref",
               f"meta.json says {meta.get('totalTools')} tools but tools.json has {len(tools)}",
               auto_fixable=True, fix_fn=fix_meta_count)

    # Meta.json category count mismatch
    if meta.get("totalCategories") != len(categories):
        def fix_cat_count():
            meta["totalCategories"] = len(categories)
            save("meta", meta)
        action("minor", "cross-ref",
               f"meta.json says {meta.get('totalCategories')} categories but categories.json has {len(categories)}",
               auto_fixable=True, fix_fn=fix_cat_count)


# ============================================================
# CHECK 3: Staleness detection
# ============================================================
def check_staleness():
    print("\n3. STALENESS")
    tools = load("tools") or []
    today = datetime.now()

    stale_90 = []
    stale_60 = []
    stale_30 = []
    for t in tools:
        lv = t.get("lastVerified", "")
        try:
            d = datetime.fromisoformat(lv)
            delta = (today - d).days
            if delta > 90:
                stale_90.append(t["id"])
            elif delta > 60:
                stale_60.append(t["id"])
            elif delta > 30:
                stale_30.append(t["id"])
        except:
            stale_90.append(t["id"])

    if stale_90:
        action("critical", "staleness",
               f"{len(stale_90)} tools not verified in 90+ days: {', '.join(stale_90[:5])}{'...' if len(stale_90)>5 else ''}")
    if stale_60:
        action("moderate", "staleness",
               f"{len(stale_60)} tools not verified in 60-90 days")
    if stale_30:
        action("minor", "staleness",
               f"{len(stale_30)} tools not verified in 30-60 days")

    # Briefing recency
    briefings = load("briefings") or []
    if briefings:
        dates = [b.get("date", "") for b in briefings]
        latest = max(dates) if dates else ""
        if latest:
            try:
                days_since = (today - datetime.fromisoformat(latest)).days
                if days_since > 7:
                    action("critical", "staleness",
                           f"No briefing in {days_since} days (latest: {latest}). Run research sweep.")
                elif days_since > 3:
                    action("moderate", "staleness",
                           f"No briefing in {days_since} days. Consider running research sweep.")
            except:
                pass


# ============================================================
# CHECK 4: Coverage gaps
# ============================================================
def check_coverage_gaps():
    print("\n4. COVERAGE GAPS")
    tools = load("tools") or []
    sources = load("news-sources") or []
    categories = load("categories") or []

    # Category balance
    counts = Counter(t["category"] for t in tools)
    for c in categories:
        count = counts.get(c["id"], 0)
        if count < 3:
            action("moderate", "coverage",
                   f"Category '{c['name']}' has only {count} tools — needs expansion")
        elif count >= 30:
            action("moderate", "coverage",
                   f"Category '{c['name']}' has {count} tools — consider splitting")

    # Source type diversity
    source_types = Counter(s.get("type", "unknown") for s in sources)
    essential_types = ["company-blog", "newsletter", "news-site", "github", "reddit"]
    for t in essential_types:
        if source_types.get(t, 0) < 3:
            action("minor", "coverage",
                   f"Only {source_types.get(t, 0)} sources of type '{t}' — add more")


# ============================================================
# CHECK 5: Duplicate detection
# ============================================================
def check_duplicates():
    print("\n5. DUPLICATES")
    tools = load("tools") or []

    # Duplicate tool IDs
    id_counts = Counter(t["id"] for t in tools)
    for tid, count in id_counts.items():
        if count > 1:
            action("critical", "duplicates",
                   f"Duplicate tool ID '{tid}' appears {count} times")

    # Duplicate tool names (case-insensitive)
    name_counts = Counter(t["name"].lower().strip() for t in tools)
    for name, count in name_counts.items():
        if count > 1:
            action("moderate", "duplicates",
                   f"Duplicate tool name '{name}' appears {count} times (may be intentional)")

    # Developer name normalization
    dev_variants = {}
    for t in tools:
        dev = t.get("developer", "")
        norm = dev.lower().strip().rstrip(".")
        if norm not in dev_variants:
            dev_variants[norm] = set()
        dev_variants[norm].add(dev)
    for norm, variants in dev_variants.items():
        if len(variants) > 1:
            action("minor", "duplicates",
                   f"Developer name inconsistency: {' vs '.join(sorted(variants))}")


# ============================================================
# CHECK 6: Self-improvement system health
# ============================================================
def check_self_improvement():
    print("\n6. SELF-IMPROVEMENT HEALTH")
    discovery = load("discovery-methods") or {}
    automation = load("automation") or {}

    # How many discovery methods are built?
    methods = discovery.get("discoveryMethods", [])
    built = [m for m in methods if m.get("implementationStatus") != "not-built"]
    total = len(methods)
    if total > 0 and len(built) == 0:
        action("moderate", "self-improvement",
               f"0 of {total} discovery methods are built — the system cannot self-discover yet")
    elif total > 0:
        pct = len(built) / total * 100
        action("info", "self-improvement",
               f"{len(built)} of {total} discovery methods built ({pct:.0f}%)")

    # Pipeline health
    pipelines = automation.get("pipelines", [])
    active = [p for p in pipelines if p.get("status") == "active"]
    ready = [p for p in pipelines if p.get("status") == "ready"]
    action("info", "self-improvement",
           f"Pipelines: {len(active)} active, {len(ready)} ready, {len(pipelines)-len(active)-len(ready)} planned/concept")

    # Automation goal progress
    goals = automation.get("automationGoals", [])
    for g in goals:
        progress = g.get("currentProgress", "0%")
        if progress not in ("100%", "0%"):
            action("info", "self-improvement",
                   f"Level {g['level']} ({g['name']}): {progress}")


# ============================================================
# CHECK 7: Trust & security currency
# ============================================================
def check_trust_currency():
    print("\n7. TRUST & SECURITY")
    trust = load("trust-framework") or {}
    incidents = trust.get("knownIncidents", [])
    today = datetime.now()

    active_incidents = [i for i in incidents if i.get("status") not in ("resolved",)]
    if active_incidents:
        action("info", "trust",
               f"{len(active_incidents)} active security incidents being tracked")
        for inc in active_incidents:
            if inc.get("severity") == "critical":
                action("critical", "trust",
                       f"CRITICAL incident for '{inc['tool']}': {inc.get('description', '')[:80]}...")

    # Check if any incident is old and unresolved
    for inc in active_incidents:
        try:
            d = datetime.fromisoformat(inc.get("date", "2020-01-01"))
            days = (today - d).days
            if days > 90:
                action("moderate", "trust",
                       f"Incident for '{inc['tool']}' is {days} days old and still unresolved — verify current status")
        except:
            pass


# ============================================================
# CHECK 8: Improvement tracking — what got better since last run?
# ============================================================
def check_improvement_trajectory():
    print("\n8. IMPROVEMENT TRAJECTORY")
    report_path = BASE / "improvement-history.json"
    history = []
    if report_path.exists():
        try:
            history = json.load(open(report_path, "r", encoding="utf-8"))
        except:
            pass

    tools = load("tools") or []
    sources = load("news-sources") or []
    briefings = load("briefings") or []

    current = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "tools": len(tools),
        "sources": len(sources),
        "briefings": len(briefings),
        "actions_found": len(actions),
        "critical_count": len([a for a in actions if a["severity"] == "critical"]),
        "moderate_count": len([a for a in actions if a["severity"] == "moderate"])
    }

    if history:
        prev = history[-1]
        delta_tools = current["tools"] - prev.get("tools", 0)
        delta_sources = current["sources"] - prev.get("sources", 0)
        delta_critical = current["critical_count"] - prev.get("critical_count", 0)
        if delta_tools:
            action("info", "trajectory", f"Tools: {prev.get('tools',0)} -> {current['tools']} ({'+' if delta_tools>0 else ''}{delta_tools})")
        if delta_sources:
            action("info", "trajectory", f"Sources: {prev.get('sources',0)} -> {current['sources']} ({'+' if delta_sources>0 else ''}{delta_sources})")
        if delta_critical < 0:
            action("info", "trajectory", f"Critical issues reduced by {abs(delta_critical)}")
        elif delta_critical > 0:
            action("moderate", "trajectory", f"Critical issues increased by {delta_critical}")

    # Save current snapshot
    history.append(current)
    # Keep last 50 snapshots
    history = history[-50:]
    if not DRY_RUN:
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2)


# ============================================================
# MAIN
# ============================================================
def main():
    print("=" * 60)
    print("CC-AIProgress Self-Improvement Engine")
    print(f"{'DRY RUN — no changes will be made' if DRY_RUN else 'Auto-fixing safe issues'}")
    print("=" * 60)

    check_data_integrity()
    check_cross_references()
    check_staleness()
    check_coverage_gaps()
    check_duplicates()
    check_self_improvement()
    check_trust_currency()
    check_improvement_trajectory()

    # Summary
    by_severity = Counter(a["severity"] for a in actions)
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Critical: {by_severity.get('critical', 0)}")
    print(f"  Moderate: {by_severity.get('moderate', 0)}")
    print(f"  Minor:    {by_severity.get('minor', 0)}")
    print(f"  Info:     {by_severity.get('info', 0)}")
    print(f"  Total:    {len(actions)}")

    auto_fixed = [a for a in actions if a.get("auto_fixable")]
    if auto_fixed and not DRY_RUN:
        print(f"\n  Auto-fixed: {len(auto_fixed)} issues")

    # Generate report if requested
    if REPORT:
        report = {
            "generated": datetime.now().isoformat(),
            "summary": dict(by_severity),
            "actions": actions
        }
        report_path = BASE / "improvement-report.json"
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        print(f"\n  Report saved to {report_path}")

    return by_severity.get("critical", 0)


if __name__ == "__main__":
    exit_code = main()
    sys.exit(1 if exit_code > 0 else 0)
