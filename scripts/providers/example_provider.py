"""
Example: How to add a new AI provider to the CC-AIProgress AI Engine.

Drop any .py file in this directory (scripts/providers/) and it will be
auto-loaded by ai-engine.py. Files starting with _ are skipped.

Your file must have a register(register_fn) function that registers
one or more providers.

A provider is just a function: prompt_string_in -> response_string_out.
That's it. Wrap any AI API, local model, or even a web scraper in that
interface and it works.
"""

def register(register_fn):
    """Called automatically by ai-engine.py on startup."""

    def my_custom_ai(prompt):
        """Replace this with your actual AI call."""
        # Example: call a custom API
        # import requests
        # r = requests.post("https://my-ai.example.com/v1/chat", json={"prompt": prompt})
        # return r.json()["response"]
        return '{"actions": [], "summary": "Example provider - replace with real implementation"}'

    register_fn(
        "example",              # Provider name (used in config)
        my_custom_ai,           # The function
        "Example provider - copy and modify this file"  # Description shown in --providers
    )
