#!/usr/bin/env python3
"""Populate the capabilities field for all tools in tools.json."""

import json
import re
import os

TOOLS_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'tools.json')

# Category-based defaults
CATEGORY_DEFAULTS = {
    "text-chat": ["text-generation", "text-analysis", "summarization"],
    "image-generation": ["image-generation"],
    "video-generation": ["video-generation"],
    "audio-music": ["audio-generation", "music-generation"],
    "coding-assistants": ["code-generation", "code-analysis"],
    "productivity": ["text-editing", "summarization"],
    "3d-cad": ["3d-modeling", "cad-design"],
    "all-in-one": ["text-generation", "text-analysis"],
    "workflow-automation": ["automation"],
    "ai-agents": ["automation", "code-execution"],
    "local-ai": ["text-generation", "text-analysis"],
    "ai-security": ["text-analysis"],
    "speech-voice": ["speech-synthesis", "speech-recognition"],
    "data-analysis": ["data-analysis", "text-analysis"],
    "robotics-ai": ["simulation", "robot-control"],
}

# Specific tool overrides (replace all)
REPLACE_ALL = {
    "orcaslicer-cli": ["3d-slicing", "file-conversion"],
    "ltspice": ["circuit-design", "simulation"],
    "jlcpcb-api": ["pcb-layout", "api-call"],
    "davinci-resolve": ["video-editing", "audio-generation"],
    "mujoco": ["simulation", "robot-control", "path-planning"],
    "gazebo": ["simulation", "robot-control", "sensor-processing"],
    "isaac-sim": ["simulation", "robot-control", "sensor-processing", "path-planning"],
    "px4": ["robot-control", "path-planning", "sensor-processing"],
    "ardupilot": ["robot-control", "path-planning", "sensor-processing"],
    "ros2-nav2": ["robot-control", "path-planning"],
    "realsense": ["sensor-processing", "image-analysis", "3d-modeling"],
    "luxonis-oak": ["sensor-processing", "image-analysis"],
    "edge-impulse": ["sensor-processing", "code-generation", "deployment"],
    "jetson-orin": ["code-execution", "sensor-processing", "robot-control"],
    "whisper-ai": ["speech-recognition"],
    "suno": ["music-generation", "audio-generation"],
    "midjourney": ["image-generation"],
    "stable-diffusion": ["image-generation", "image-editing"],
    "dall-e-api": ["image-generation", "api-call"],
    "github-actions": ["automation", "deployment", "code-execution"],
    "github-pages": ["deployment"],
    "playwright": ["web-scraping", "automation", "code-execution"],
    "puppeteer": ["web-scraping", "automation", "code-execution"],
    "fastapi": ["api-call", "code-execution", "deployment"],
    "cloudflare-tunnel": ["deployment"],
    "n8n": ["automation", "api-call"],
    "zapier": ["automation", "api-call"],
    "make-com": ["automation", "api-call"],
    "power-automate": ["automation"],
    "pubmed-api": ["data-analysis", "web-search", "api-call"],
    "clinicaltrials-api": ["data-analysis", "api-call"],
    "google-scholar-alerts": ["web-search", "data-analysis"],
    "coqui-tts": ["speech-synthesis"],
    "twilio": ["api-call", "speech-synthesis"],
    "youtube": ["video-generation", "deployment"],
    "toggl": ["data-analysis", "automation"],
    "rescuetime": ["data-analysis", "automation"],
}

# Specific tool additions (add to category defaults)
ADD_CAPS = {
    "chatgpt": ["image-generation", "web-search", "code-generation", "code-analysis", "image-analysis", "translation"],
    "claude": ["code-generation", "code-analysis", "translation"],
    "claude-api": ["code-generation", "code-analysis", "api-call", "translation"],
    "gemini": ["image-generation", "code-generation", "translation", "image-analysis", "web-search"],
    "gemini-api": ["code-generation", "api-call", "translation", "image-analysis"],
    "openai-api": ["code-generation", "image-generation", "speech-synthesis", "speech-recognition", "api-call", "translation"],
    "perplexity": ["web-search"],
    "perplexity-api": ["web-search", "api-call"],
    "grok": ["web-search", "code-generation", "image-generation"],
    "github-copilot": ["code-execution"],
    "cursor": ["code-execution"],
    "windsurf": ["code-execution"],
    "blender": ["3d-modeling", "simulation", "code-execution"],
    "freecad": ["3d-modeling", "cad-design"],
    "fusion-360": ["3d-modeling", "cad-design", "simulation"],
    "elevenlabs": ["speech-synthesis", "audio-generation"],
    "runway": ["image-generation", "image-editing", "video-editing"],
}

# Keyword-based rules: (condition_func, capabilities_to_add)
def kw(text, *words):
    """Check if ALL words appear in text (case-insensitive)."""
    t = text.lower()
    return all(w in t for w in words)

def kw_any(text, *words):
    """Check if ANY word appears in text (case-insensitive)."""
    t = text.lower()
    return any(w in t for w in words)


def get_keyword_additions(name, description):
    """Return capabilities to add based on keyword matching."""
    combo = (name + " " + description).lower()
    adds = []

    if kw_any(combo, "search", "perplexity"):
        adds.append("web-search")
    if kw_any(combo, "translate"):
        adds.append("translation")
    if kw(combo, "image", "edit"):
        adds.append("image-editing")
    if kw(combo, "image", "analy"):
        adds.append("image-analysis")
    if kw(combo, "video", "edit"):
        adds.append("video-editing")
    if kw_any(combo, "3d print", "slicer", "slicing"):
        adds.append("3d-slicing")
    if kw_any(combo, "circuit", "pcb", "schematic"):
        adds.extend(["circuit-design", "pcb-layout"])
    if kw_any(combo, "firmware", "arduino", "embedded"):
        adds.append("code-generation")
    if kw_any(combo, "speech", "voice", "tts"):
        adds.append("speech-synthesis")
    if kw_any(combo, "transcri", "whisper", "stt"):
        adds.append("speech-recognition")
    if kw_any(combo, "deploy"):
        adds.append("deployment")
    if kw_any(name.lower(), "api"):
        adds.append("api-call")
    if kw_any(combo, "scraping", "crawl"):
        adds.append("web-scraping")
    if kw_any(combo, "sensor"):
        adds.append("sensor-processing")
    if kw(combo, "path", "plan"):
        adds.append("path-planning")
    if kw_any(combo, "drone", "uav"):
        adds.append("robot-control")
    if re.search(r'\bros\b', combo, re.IGNORECASE):
        adds.append("robot-control")
    if kw_any(combo, "simul"):
        adds.append("simulation")

    return adds


def main():
    with open(TOOLS_PATH, 'r', encoding='utf-8') as f:
        tools = json.load(f)

    total = len(tools)
    cap_counts = []

    for tool in tools:
        tid = tool.get("id", "")
        name = tool.get("name", "")
        category = tool.get("category", "")
        description = tool.get("description", "")

        # Check if this tool has a full replacement
        if tid in REPLACE_ALL:
            caps = list(REPLACE_ALL[tid])
        else:
            # Start with category defaults
            caps = list(CATEGORY_DEFAULTS.get(category, []))

            # Add specific tool additions
            if tid in ADD_CAPS:
                caps.extend(ADD_CAPS[tid])

            # Add keyword-based additions
            caps.extend(get_keyword_additions(name, description))

        # Deduplicate while preserving order
        seen = set()
        deduped = []
        for c in caps:
            if c not in seen:
                seen.add(c)
                deduped.append(c)

        tool["capabilities"] = deduped
        cap_counts.append(len(deduped))

    # Write back
    with open(TOOLS_PATH, 'w', encoding='utf-8') as f:
        json.dump(tools, f, indent=2, ensure_ascii=False)

    # Summary
    tools_with_caps = sum(1 for c in cap_counts if c > 0)
    avg = sum(cap_counts) / total if total else 0
    print(f"Total tools: {total}")
    print(f"Tools with capabilities: {tools_with_caps}")
    print(f"Tools without capabilities: {total - tools_with_caps}")
    print(f"Average capabilities per tool: {avg:.1f}")
    print(f"Min: {min(cap_counts)}, Max: {max(cap_counts)}")

    # Show a few examples
    print("\nSample results:")
    for tool in tools[:5]:
        print(f"  {tool['id']}: {tool['capabilities']}")


if __name__ == "__main__":
    main()
