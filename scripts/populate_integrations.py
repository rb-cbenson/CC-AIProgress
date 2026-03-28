#!/usr/bin/env python3
"""Populate integrations field for tools — which tools work with which."""
import json, sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

tools = json.load(open('data/tools.json', 'r', encoding='utf-8'))
tool_ids = {t['id'] for t in tools}

# Integration map: tool_id -> [tools it integrates with]
# Only include integrations where tools ACTUALLY connect
# (API compatibility, file format exchange, plugin/extension, built-in support)
integrations = {
    # --- TEXT/CHAT LLMs — they integrate with each other via OpenRouter ---
    'chatgpt': ['openai-api', 'dall-e-api', 'openrouter'],
    'claude': ['claude-api', 'openrouter'],
    'gemini': ['gemini-api', 'openrouter'],
    'grok': ['openrouter'],
    'perplexity': ['perplexity-api', 'openrouter'],

    # --- APIs — integrate with orchestration tools ---
    'claude-api': ['openrouter', 'n8n', 'zapier', 'make-com', 'tavily', 'groq'],
    'openai-api': ['openrouter', 'n8n', 'zapier', 'make-com', 'dall-e-api', 'tavily'],
    'gemini-api': ['openrouter', 'n8n', 'tavily'],
    'perplexity-api': ['openrouter', 'n8n', 'tavily'],
    'dall-e-api': ['openai-api', 'n8n', 'zapier'],
    'groq': ['openrouter', 'tavily', 'n8n'],
    'mistral': ['openrouter', 'n8n'],
    'openrouter': ['claude-api', 'openai-api', 'gemini-api', 'groq', 'mistral'],
    'tavily': ['claude-api', 'openai-api', 'groq', 'n8n'],

    # --- CODING ---
    'github-copilot': ['cursor', 'windsurf', 'github-actions', 'github-pages'],
    'cursor': ['github-copilot', 'claude-api', 'openai-api'],
    'windsurf': ['claude-api', 'openai-api'],
    'claude-code': ['claude-api', 'github-actions', 'github-pages', 'playwright', 'puppeteer'],
    'tabnine': ['cursor', 'windsurf'],

    # --- AUTOMATION ---
    'n8n': ['claude-api', 'openai-api', 'gemini-api', 'zapier', 'make-com', 'github-actions', 'tavily', 'groq'],
    'zapier': ['n8n', 'make-com', 'openai-api', 'claude-api', 'notion-ai', 'google-notebooklm'],
    'make-com': ['n8n', 'zapier', 'openai-api', 'claude-api'],
    'github-actions': ['github-pages', 'claude-code', 'n8n', 'playwright', 'puppeteer'],
    'github-pages': ['github-actions'],
    'power-automate': ['openai-api'],

    # --- BROWSER AUTOMATION ---
    'playwright': ['claude-code', 'github-actions', 'puppeteer', 'fastapi'],
    'puppeteer': ['claude-code', 'github-actions', 'playwright', 'fastapi'],

    # --- IMAGE ---
    'midjourney': ['runway', 'davinci-resolve'],
    'stable-diffusion': ['runway', 'davinci-resolve', 'blender', 'ollama', 'lm-studio'],
    'dall-e-api': ['openai-api', 'chatgpt', 'runway'],
    'adobe-firefly': ['davinci-resolve', 'runway'],

    # --- VIDEO ---
    'runway': ['midjourney', 'stable-diffusion', 'dall-e-api', 'davinci-resolve', 'elevenlabs', 'suno'],
    'kling': ['davinci-resolve', 'elevenlabs'],
    'pika': ['davinci-resolve', 'elevenlabs'],
    'davinci-resolve': ['runway', 'kling', 'pika', 'elevenlabs', 'suno', 'midjourney', 'blender'],

    # --- AUDIO/VOICE ---
    'elevenlabs': ['runway', 'davinci-resolve', 'kling', 'pika', 'openai-api'],
    'suno': ['davinci-resolve', 'runway'],
    'suno-api': ['n8n', 'davinci-resolve'],
    'runway-api': ['n8n', 'openai-api'],
    'coqui-tts': ['ros2', 'fastapi'],

    # --- 3D/CAD ---
    'blender': ['freecad', 'fusion-360', 'orcaslicer-cli', 'stable-diffusion', 'davinci-resolve', 'kicad'],
    'freecad': ['blender', 'kicad', 'orcaslicer-cli', 'fusion-360'],
    'fusion-360': ['blender', 'freecad', 'kicad', 'orcaslicer-cli', 'jlcpcb-api'],
    'orcaslicer-cli': ['blender', 'freecad', 'fusion-360'],

    # --- ELECTRONICS ---
    'kicad': ['jlcpcb-api', 'freecad', 'blender', 'ltspice', 'fusion-360'],
    'ltspice': ['kicad'],
    'jlcpcb-api': ['kicad', 'fusion-360'],

    # --- ROBOTICS ---
    'ros2': ['gazebo', 'ros2-nav2', 'isaac-sim', 'mujoco', 'realsense', 'opencv', 'px4', 'ardupilot', 'jetson-orin', 'foxglove'],
    'gazebo': ['ros2', 'ros2-nav2', 'px4', 'ardupilot'],
    'isaac-sim': ['ros2', 'mujoco', 'ros2-nav2', 'jetson-orin', 'realsense'],
    'mujoco': ['ros2', 'isaac-sim', 'drake'],
    'drake': ['ros2', 'mujoco'],
    'ros2-nav2': ['ros2', 'gazebo', 'isaac-sim', 'realsense'],
    'px4': ['ros2', 'gazebo', 'ardupilot', 'qgroundcontrol'],
    'ardupilot': ['ros2', 'gazebo', 'px4'],
    'realsense': ['ros2', 'opencv', 'jetson-orin', 'isaac-sim', 'ros2-nav2'],
    'luxonis-oak': ['ros2', 'opencv', 'jetson-orin'],
    'opencv': ['ros2', 'realsense', 'luxonis-oak', 'jetson-orin', 'blender'],
    'jetson-orin': ['ros2', 'opencv', 'realsense', 'luxonis-oak', 'isaac-sim', 'edge-impulse'],
    'edge-impulse': ['jetson-orin', 'ros2', 'arduino'],
    'foxglove': ['ros2', 'gazebo'],
    'unitree-sdk': ['ros2', 'isaac-sim', 'mujoco'],

    # --- LOCAL AI ---
    'ollama': ['lm-studio', 'openrouter', 'stable-diffusion'],
    'lm-studio': ['ollama'],
    'llama-cpp': ['ollama', 'lm-studio'],

    # --- PRODUCTIVITY ---
    'notion-ai': ['zapier', 'make-com'],
    'google-notebooklm': ['gemini'],
    'grammarly': ['notion-ai'],

    # --- DATA/RESEARCH ---
    'pubmed-api': ['clinicaltrials-api', 'google-scholar-alerts', 'claude-api'],
    'clinicaltrials-api': ['pubmed-api', 'claude-api'],
    'google-scholar-alerts': ['pubmed-api', 'claude-api'],

    # --- DEPLOYMENT ---
    'fastapi': ['claude-code', 'playwright', 'cloudflare-tunnel'],
    'cloudflare-tunnel': ['fastapi', 'github-pages'],
    'twilio': ['fastapi', 'n8n', 'zapier'],
}

updated = 0
for t in tools:
    tid = t['id']
    if tid in integrations:
        # Only include integrations that reference tools we actually have
        valid = [i for i in integrations[tid] if i in tool_ids]
        if valid:
            t['integrations'] = sorted(set(valid))
            updated += 1

# Make integrations bidirectional — if A integrates with B, B should list A
for t in tools:
    tid = t['id']
    for other_id in t.get('integrations', []):
        other = next((x for x in tools if x['id'] == other_id), None)
        if other:
            other_ints = other.get('integrations', [])
            if tid not in other_ints:
                other_ints.append(tid)
                other['integrations'] = sorted(set(other_ints))

final_count = sum(1 for t in tools if t.get('integrations') and len(t['integrations']) > 0)

with open('data/tools.json', 'w', encoding='utf-8') as f:
    json.dump(tools, f, indent=2, ensure_ascii=False)

print(f'Populated integrations for {updated} tools directly')
print(f'Total tools with integrations after bidirectional fill: {final_count}')
print(f'Tools still empty: {len(tools) - final_count}')
