"""
Load .env file into os.environ. Import this at the top of any script
that needs API keys. No external dependencies.

Usage:
    from env_loader import load_env
    load_env()
    # Now os.environ has all keys from .env
"""

import os
from pathlib import Path


def load_env(env_path=None):
    """Load .env file into os.environ. Doesn't override existing vars."""
    if env_path is None:
        env_path = Path(__file__).resolve().parent.parent / ".env"

    if not env_path.exists():
        return False

    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip()
            # Don't override existing env vars
            if key not in os.environ:
                os.environ[key] = value

    return True
