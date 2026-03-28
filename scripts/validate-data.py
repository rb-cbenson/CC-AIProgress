#!/usr/bin/env python3
"""
CC-AIProgress Data Validator
Catches the kind of errors that shouldn't make it into production:
- URL mismatches (adam.ai vs adam.new)
- Duplicate IDs
- Missing required fields
- Category references to non-existent categories
- Stale data (>90 days unverified)
- URL reachability (optional, with --check-urls flag)
- Trust score sanity checks
- JSON syntax errors

Run: python scripts/validate-data.py
With URL checks: python scripts/validate-data.py --check-urls
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime, timedelta

# Fix Windows console encoding for emoji
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Resolve project root (script lives in scripts/)
ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

errors = []
warnings = []

def error(msg):
    errors.append(f"❌ ERROR: {msg}")

def warn(msg):
    warnings.append(f"⚠️  WARN: {msg}")

def info(msg):
    print(f"  ✓ {msg}")

def load_json(filename):
    path = DATA / filename
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        error(f"{filename}: Invalid JSON — {e}")
        return None
    except FileNotFoundError:
        error(f"{filename}: File not found")
        return None

def validate_tools(tools, categories):
    """Validate tools.json"""
    print("\n📦 Validating tools.json...")
    if not tools:
        error("tools.json is empty or failed to load")
        return

    cat_ids = {c['id'] for c in categories} if categories else set()
    seen_ids = set()
    required_fields = ['id', 'name', 'category', 'developer', 'url', 'description', 'pricingCAD', 'ranking', 'pros', 'cons', 'lastVerified']
    today = datetime.now()

    for i, tool in enumerate(tools):
        tid = tool.get('id', f'<missing-id-index-{i}>')

        # Duplicate ID check
        if tid in seen_ids:
            error(f"Duplicate tool ID: '{tid}'")
        seen_ids.add(tid)

        # Required fields
        for field in required_fields:
            if field not in tool:
                error(f"Tool '{tid}': missing required field '{field}'")

        # Category exists
        if cat_ids and tool.get('category') not in cat_ids:
            error(f"Tool '{tid}': category '{tool.get('category')}' not in categories.json")

        # URL format
        url = tool.get('url', '')
        if not url.startswith('http'):
            error(f"Tool '{tid}': invalid URL '{url}'")

        # URL vs name mismatch detection (the adam.ai problem)
        # Flag when URL domain doesn't contain any part of the tool name
        if url:
            try:
                from urllib.parse import urlparse
                domain = urlparse(url).hostname or ''
                name_lower = tool.get('name', '').lower().replace(' ', '').replace('-', '').replace('.', '')
                domain_clean = domain.replace('www.', '').replace('.com', '').replace('.ai', '').replace('.io', '').replace('.dev', '').replace('.new', '').replace('.app', '')
                # Loose check: if neither the domain contains part of the name nor vice versa
                if len(name_lower) > 3 and len(domain_clean) > 3:
                    if name_lower[:4] not in domain_clean and domain_clean[:4] not in name_lower:
                        warn(f"Tool '{tid}': URL domain '{domain}' may not match name '{tool.get('name')}' — verify manually")
            except Exception:
                pass

        # Staleness check
        last_verified = tool.get('lastVerified', '')
        if last_verified:
            try:
                verified_date = datetime.strptime(last_verified, '%Y-%m-%d')
                age = (today - verified_date).days
                if age > 180:
                    error(f"Tool '{tid}': data is {age} days old — needs re-verification")
                elif age > 90:
                    warn(f"Tool '{tid}': data is {age} days old — approaching stale")
            except ValueError:
                error(f"Tool '{tid}': invalid date format '{last_verified}' (expected YYYY-MM-DD)")

        # Pricing structure
        pricing = tool.get('pricingCAD', {})
        if not isinstance(pricing, dict):
            error(f"Tool '{tid}': pricingCAD should be an object")
        elif 'freeTier' not in pricing:
            error(f"Tool '{tid}': pricingCAD missing 'freeTier' boolean")

        # Ranking structure
        ranking = tool.get('ranking', {})
        if not isinstance(ranking, dict):
            error(f"Tool '{tid}': ranking should be an object")
        else:
            if ranking.get('trend') not in ('rising', 'stable', 'declining'):
                error(f"Tool '{tid}': invalid trend '{ranking.get('trend')}' — must be rising|stable|declining")
            if not isinstance(ranking.get('overall'), int) or ranking['overall'] < 1:
                error(f"Tool '{tid}': overall ranking must be a positive integer")

        # Trust score range
        ts = tool.get('trustScore')
        if ts is not None and (not isinstance(ts, (int, float)) or ts < 0 or ts > 100):
            error(f"Tool '{tid}': trustScore {ts} outside valid range 0-100")

        # Empty description
        if len(tool.get('description', '')) < 10:
            warn(f"Tool '{tid}': description seems too short")

        # Empty pros/cons
        if not tool.get('pros'):
            warn(f"Tool '{tid}': no pros listed")
        if not tool.get('cons'):
            warn(f"Tool '{tid}': no cons listed")

    info(f"{len(tools)} tools validated, {len(seen_ids)} unique IDs")

    # Check for ranking gaps/duplicates
    overall_ranks = [t['ranking']['overall'] for t in tools if 'ranking' in t and 'overall' in t.get('ranking', {})]
    dup_ranks = [r for r in set(overall_ranks) if overall_ranks.count(r) > 1]
    if dup_ranks:
        warn(f"Duplicate overall rankings: {sorted(dup_ranks)[:10]}{'...' if len(dup_ranks)>10 else ''}")

def validate_categories(categories):
    """Validate categories.json"""
    print("\n📂 Validating categories.json...")
    if not categories:
        error("categories.json is empty or failed to load")
        return

    seen = set()
    for cat in categories:
        cid = cat.get('id', '<missing>')
        if cid in seen:
            error(f"Duplicate category ID: '{cid}'")
        seen.add(cid)
        for field in ['id', 'name', 'icon', 'color', 'description']:
            if field not in cat:
                error(f"Category '{cid}': missing '{field}'")

    info(f"{len(categories)} categories validated")

def validate_meta(meta, tools, categories):
    """Validate meta.json consistency"""
    print("\n📋 Validating meta.json...")
    if not meta:
        error("meta.json is empty or failed to load")
        return

    if tools and meta.get('totalTools') != len(tools):
        error(f"meta.json says {meta.get('totalTools')} tools but tools.json has {len(tools)}")
    if categories and meta.get('totalCategories') != len(categories):
        error(f"meta.json says {meta.get('totalCategories')} categories but categories.json has {len(categories)}")

    info(f"meta.json: v{meta.get('version')}, {meta.get('totalTools')} tools, {meta.get('totalCategories')} categories")

def validate_trust_framework(framework, tools):
    """Validate trust-framework.json"""
    print("\n🛡️  Validating trust-framework.json...")
    if not framework:
        warn("trust-framework.json not found or empty")
        return

    incidents = framework.get('knownIncidents', [])
    tool_ids = {t['id'] for t in tools} if tools else set()

    for inc in incidents:
        if inc.get('tool') not in tool_ids and inc.get('tool') not in ('chrome-ai-extensions',):
            warn(f"Incident for '{inc.get('tool')}' — tool not in database (may be intentional for non-tracked tools)")
        if inc.get('severity') not in ('critical', 'high', 'medium', 'low'):
            error(f"Incident '{inc.get('tool')}': invalid severity '{inc.get('severity')}'")

    info(f"{len(incidents)} known incidents, {len(framework.get('exampleScores', []))} example scores")

def check_urls(tools):
    """Optional: Check if tool URLs are reachable"""
    print("\n🌐 Checking URLs (this may take a while)...")
    import urllib.request
    import ssl

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    unreachable = []
    redirected = []

    for i, tool in enumerate(tools):
        url = tool.get('url', '')
        tid = tool.get('id', '?')
        if not url.startswith('http'):
            continue
        try:
            req = urllib.request.Request(url, method='HEAD', headers={'User-Agent': 'Mozilla/5.0 CC-AIProgress Validator'})
            resp = urllib.request.urlopen(req, timeout=10, context=ctx)
            final_url = resp.geturl()
            if final_url.rstrip('/') != url.rstrip('/'):
                # Check if it's a significant redirect (not just http->https or trailing slash)
                if final_url.replace('https://', '').replace('http://', '').replace('www.', '').rstrip('/') != url.replace('https://', '').replace('http://', '').replace('www.', '').rstrip('/'):
                    redirected.append((tid, url, final_url))
                    warn(f"Tool '{tid}': URL redirects: {url} → {final_url}")
        except Exception as e:
            unreachable.append((tid, url, str(e)[:80]))
            warn(f"Tool '{tid}': URL unreachable: {url} — {str(e)[:80]}")

        # Progress indicator
        if (i + 1) % 20 == 0:
            print(f"    ...checked {i+1}/{len(tools)}")

    info(f"Checked {len(tools)} URLs: {len(unreachable)} unreachable, {len(redirected)} redirected")

def main():
    print("=" * 60)
    print("CC-AIProgress Data Validator")
    print("=" * 60)

    # Load all data
    tools = load_json("tools.json")
    categories = load_json("categories.json")
    meta = load_json("meta.json")
    trust = load_json("trust-framework.json")

    # Run validations
    validate_categories(categories)
    validate_tools(tools, categories)
    validate_meta(meta, tools, categories)
    validate_trust_framework(trust, tools)

    # Optional URL checking
    if '--check-urls' in sys.argv and tools:
        check_urls(tools)

    # Summary
    print("\n" + "=" * 60)
    if warnings:
        print(f"\n⚠️  {len(warnings)} warnings:")
        for w in warnings:
            print(f"  {w}")
    if errors:
        print(f"\n❌ {len(errors)} errors:")
        for e in errors:
            print(f"  {e}")
        print(f"\n💥 VALIDATION FAILED — {len(errors)} errors, {len(warnings)} warnings")
        sys.exit(1)
    else:
        print(f"\n✅ VALIDATION PASSED — 0 errors, {len(warnings)} warnings")
        sys.exit(0)

if __name__ == '__main__':
    main()
