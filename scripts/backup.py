#!/usr/bin/env python3
"""
CC-AIProgress Backup & Snapshot Utility

Creates tagged git snapshots at key moments. Tags are free (just pointers,
no storage cost) and let you jump back to any snapshot instantly.

Usage:
    python scripts/backup.py                  # Auto-tagged snapshot (backup-YYYY-MM-DD-HHMM)
    python scripts/backup.py "before research sweep"  # Custom message
    python scripts/backup.py --list           # Show all backup tags
    python scripts/backup.py --revert         # Show how to revert (doesn't do it)
    python scripts/backup.py --revert backup-2026-03-28-0900  # Actually revert to that tag

Storage: Zero. Git tags are just pointers to existing commits.
"""

import subprocess
import sys
from datetime import datetime

def run(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return r.stdout.strip(), r.stderr.strip(), r.returncode

def create_snapshot(message=None):
    # Stage and commit any uncommitted changes first
    run("git add -A")
    status, _, _ = run("git status --porcelain")

    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M")
    tag_name = f"backup-{timestamp}"

    if status:
        msg = f"Backup snapshot: {message or 'periodic backup'}"
        out, err, code = run(f'git commit -m "{msg}"')
        if code != 0:
            print(f"Commit failed: {err}")
            return
        print(f"Committed changes: {msg}")
    else:
        print("No uncommitted changes.")

    # Create lightweight tag on current commit
    desc = message or f"Backup {timestamp}"
    out, err, code = run(f'git tag -a {tag_name} -m "{desc}"')
    if code != 0:
        print(f"Tag failed: {err}")
        return

    print(f"Tagged: {tag_name}")
    print(f"To revert to this point later: python scripts/backup.py --revert {tag_name}")

    # Push tag to remote if remote exists
    out, _, _ = run("git remote")
    if out:
        run(f"git push origin {tag_name}")
        print(f"Tag pushed to GitHub.")

def list_backups():
    out, _, _ = run("git tag -l 'backup-*' --sort=-creatordate -n1")
    if not out:
        print("No backup tags found.")
        return
    print("Backup snapshots (newest first):\n")
    print(out)
    print(f"\nTo see what changed between two backups:")
    print(f"  git diff backup-XXXX backup-YYYY --stat")

def show_revert_help(tag=None):
    if tag is None:
        print("REVERT OPTIONS:\n")
        print("1. See what a backup contains:")
        print("   git show <tag-name> --stat\n")
        print("2. See differences between now and a backup:")
        print("   git diff <tag-name> --stat\n")
        print("3. Restore a SINGLE FILE from a backup:")
        print("   git checkout <tag-name> -- path/to/file\n")
        print("4. Revert EVERYTHING to a backup (creates new commit, safe):")
        print("   python scripts/backup.py --revert <tag-name>\n")
        print("5. Nuclear option (discard everything since backup):")
        print("   git reset --hard <tag-name>")
        print("   WARNING: This destroys all changes after that point.\n")
        list_backups()
        return

    # Verify tag exists
    _, _, code = run(f"git rev-parse {tag}")
    if code != 0:
        print(f"Tag '{tag}' not found. Run: python scripts/backup.py --list")
        return

    # Show what would change
    print(f"Reverting to {tag}...\n")
    diff, _, _ = run(f"git diff {tag} --stat")
    if not diff:
        print("No differences — you're already at this state.")
        return

    print("Files that will change:")
    print(diff)
    print()

    confirm = input("Proceed? This creates a new commit (safe, reversible). [y/N] ")
    if confirm.lower() != 'y':
        print("Cancelled.")
        return

    # Safe revert: checkout all files from the tag, then commit as new state
    run(f"git checkout {tag} -- .")
    run(f'git commit -m "Reverted to {tag}"')
    print(f"Reverted to {tag}. This is a new commit — nothing was destroyed.")
    print("The old state is still in git history if you need it.")

if __name__ == "__main__":
    args = sys.argv[1:]

    if not args:
        create_snapshot()
    elif args[0] == "--list":
        list_backups()
    elif args[0] == "--revert":
        show_revert_help(args[1] if len(args) > 1 else None)
    else:
        create_snapshot(" ".join(args))
