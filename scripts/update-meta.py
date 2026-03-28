"""
Weekly metadata update script.
Updates lastUpdated date and totalTools count in meta.json.
"""
import json
from datetime import date

META_PATH = "data/meta.json"
TOOLS_PATH = "data/tools.json"

def main():
    # Load current meta
    with open(META_PATH, "r") as f:
        meta = json.load(f)

    # Load tools to get count
    with open(TOOLS_PATH, "r") as f:
        tools = json.load(f)

    # Update fields
    meta["lastUpdated"] = date.today().isoformat()
    meta["totalTools"] = len(tools)

    # Write back
    with open(META_PATH, "w") as f:
        json.dump(meta, f, indent=2)
        f.write("\n")

    print(f"Updated meta.json: {len(tools)} tools, date {meta['lastUpdated']}")

if __name__ == "__main__":
    main()
