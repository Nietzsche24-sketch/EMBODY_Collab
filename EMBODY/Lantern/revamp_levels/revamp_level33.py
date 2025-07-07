# revamp_level33.py — Slice Fusion into EMBODY format
import os, json
from datetime import datetime

EMOTION_PATH = "output/revamp_level24/emotion_tags.json"
BEHAVIOR_PATH = "output/revamp_level23/behavior_tags.json"
PROSODY_PATH = "output/revamp_level32/prosody_embeddings.json"
OUTPUT_PATH = "output/revamp_level33/embody_vectors.json"
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

with open(EMOTION_PATH) as f: emotion_data = json.load(f)["tagged_files"]
with open(BEHAVIOR_PATH) as f: behavior_data = json.load(f)["tagged_files"]
with open(PROSODY_PATH) as f: prosody_data = json.load(f)["prosody_embeddings"]

fused = {}
for fname, prosody in prosody_data.items():
    fused[fname] = {
        "emotion": emotion_data.get(fname, "unknown"),
        "behavior": behavior_data.get(fname, {}).get("behavior_tags", ["unknown"]),
        "prosody": prosody
    }

# Save
with open(OUTPUT_PATH, "w") as f:
    json.dump({
        "fused_embeddings": fused,
        "timestamp": datetime.now().isoformat()
    }, f, indent=2)

print(f"✅ Level 33 complete — EMBODY vectors saved to: {OUTPUT_PATH}")
