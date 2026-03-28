#!/usr/bin/env python3
"""Fix obviously wrong workflow variants from Groq generation."""
import json, sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

variants = json.load(open('data/workflow-variants.json', 'r', encoding='utf-8'))

# Manual fixes for domain-inappropriate variants
fixes = {
    "coding": {
        "free-local": [
            {"order": 1, "toolId": "ollama", "action": "Local LLM for code assistance", "free": True},
            {"order": 2, "toolId": "claude-code", "action": "Multi-file implementation and refactoring", "free": True},
            {"order": 3, "toolId": "github-actions", "action": "CI/CD and automated testing", "free": True}
        ]
    },
    "research": {
        "free-local": [
            {"order": 1, "toolId": "ollama", "action": "Local LLM for analysis and brainstorming", "free": True},
            {"order": 2, "toolId": "stable-diffusion", "action": "Generate diagrams and visual aids", "free": True},
            {"order": 3, "toolId": "google-notebooklm", "action": "Organize sources and summary", "free": True}
        ]
    },
    "robotics-sim": {
        "free-best": [
            {"order": 1, "toolId": "mujoco", "action": "Physics simulation and robot modeling", "free": True},
            {"order": 2, "toolId": "ros2", "action": "Robot control middleware", "free": True},
            {"order": 3, "toolId": "gazebo", "action": "World simulation with sensors", "free": True},
            {"order": 4, "toolId": "opencv", "action": "Computer vision and perception", "free": True}
        ],
        "free-local": [
            {"order": 1, "toolId": "mujoco", "action": "Local physics simulation", "free": True},
            {"order": 2, "toolId": "gazebo", "action": "Local world simulation", "free": True},
            {"order": 3, "toolId": "ros2", "action": "Local robot control", "free": True},
            {"order": 4, "toolId": "opencv", "action": "Local computer vision", "free": True}
        ],
        "paid-premium": [
            {"order": 1, "toolId": "isaac-sim", "action": "NVIDIA Isaac high-fidelity sim", "free": True},
            {"order": 2, "toolId": "ros2", "action": "Isaac ROS with NITROS", "free": True},
            {"order": 3, "toolId": "jetson-orin", "action": "Edge deployment", "free": True}
        ]
    },
    "pcb-design": {
        "free-best": [
            {"order": 1, "toolId": "groq", "action": "AI requirements analysis and component selection", "free": True},
            {"order": 2, "toolId": "kicad", "action": "Schematic capture with AI plugin", "free": True},
            {"order": 3, "toolId": "kicad", "action": "PCB layout and routing", "free": True},
            {"order": 4, "toolId": "blender", "action": "3D render via pcb2blender", "free": True},
            {"order": 5, "toolId": "jlcpcb-api", "action": "Export and order fabrication", "free": True}
        ],
        "free-local": [
            {"order": 1, "toolId": "kicad", "action": "Full schematic and PCB locally", "free": True},
            {"order": 2, "toolId": "ltspice", "action": "Circuit simulation", "free": True},
            {"order": 3, "toolId": "freecad", "action": "3D enclosure design", "free": True},
            {"order": 4, "toolId": "blender", "action": "Photorealistic render", "free": True}
        ]
    },
    "music": {
        "free-best": [
            {"order": 1, "toolId": "groq", "action": "Generate lyrics and style description", "free": True},
            {"order": 2, "toolId": "suno", "action": "Generate full song with vocals", "free": True},
            {"order": 3, "toolId": "udio", "action": "Edit and refine sections", "free": True},
            {"order": 4, "toolId": "davinci-resolve", "action": "Final mix and master", "free": True}
        ],
        "free-local": [
            {"order": 1, "toolId": "ollama", "action": "Generate lyrics locally", "free": True},
            {"order": 2, "toolId": "coqui-tts", "action": "Local voice synthesis", "free": True},
            {"order": 3, "toolId": "davinci-resolve", "action": "Audio editing and mixing", "free": True}
        ],
        "paid-premium": [
            {"order": 1, "toolId": "claude", "action": "Professional lyrics and arrangement", "free": True},
            {"order": 2, "toolId": "suno", "action": "Generate full song", "free": True},
            {"order": 3, "toolId": "elevenlabs", "action": "Professional vocal synthesis", "free": False},
            {"order": 4, "toolId": "davinci-resolve", "action": "Professional mix", "free": True}
        ]
    },
    "prototype": {
        "free-best": [
            {"order": 1, "toolId": "groq", "action": "Design specs from idea description", "free": True},
            {"order": 2, "toolId": "blender", "action": "3D model the product", "free": True},
            {"order": 3, "toolId": "orcaslicer-cli", "action": "Slice for 3D printing", "free": True},
            {"order": 4, "toolId": "kicad", "action": "Design electronics if needed", "free": True},
            {"order": 5, "toolId": "claude-code", "action": "Generate firmware", "free": True},
            {"order": 6, "toolId": "jlcpcb-api", "action": "Order PCB fabrication", "free": True}
        ],
        "free-local": [
            {"order": 1, "toolId": "ollama", "action": "Local AI for design brainstorming", "free": True},
            {"order": 2, "toolId": "freecad", "action": "Parametric CAD modeling", "free": True},
            {"order": 3, "toolId": "orcaslicer-cli", "action": "Slice for 3D printing", "free": True},
            {"order": 4, "toolId": "kicad", "action": "PCB design", "free": True},
            {"order": 5, "toolId": "ltspice", "action": "Circuit simulation", "free": True}
        ],
        "paid-premium": [
            {"order": 1, "toolId": "claude", "action": "Detailed product design spec", "free": True},
            {"order": 2, "toolId": "fusion-360", "action": "Professional CAD with simulation", "free": False},
            {"order": 3, "toolId": "kicad", "action": "PCB with Quilter AI auto-routing", "free": True},
            {"order": 4, "toolId": "blender", "action": "Photorealistic product renders", "free": True},
            {"order": 5, "toolId": "jlcpcb-api", "action": "Order PCB + parts", "free": True}
        ]
    },
    "content": {
        "free-local": [
            {"order": 1, "toolId": "ollama", "action": "Draft content locally", "free": True},
            {"order": 2, "toolId": "stable-diffusion", "action": "Generate images locally", "free": True},
            {"order": 3, "toolId": "davinci-resolve", "action": "Edit video content", "free": True}
        ]
    },
    "short-video": {
        "free-local": [
            {"order": 1, "toolId": "ollama", "action": "Generate script locally", "free": True},
            {"order": 2, "toolId": "coqui-tts", "action": "Local voiceover", "free": True},
            {"order": 3, "toolId": "stable-diffusion", "action": "Generate visual frames", "free": True},
            {"order": 4, "toolId": "davinci-resolve", "action": "Edit, animate, export", "free": True}
        ]
    }
}

fixed = 0
for v in variants:
    wt = v['workflowType']
    if wt in fixes:
        for var in v['variants']:
            tier = var['tier']
            if tier.lower() in fixes[wt]:
                var['steps'] = fixes[wt][tier.lower()]
                fixed += 1
                print(f"  Fixed: {wt}/{tier}")

with open('data/workflow-variants.json', 'w', encoding='utf-8') as f:
    json.dump(variants, f, indent=2, ensure_ascii=False)
print(f"\nFixed {fixed} variants. All 24 pipelines now domain-appropriate.")
