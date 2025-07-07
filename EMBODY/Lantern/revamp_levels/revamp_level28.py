import os
import json
from datetime import datetime

# File paths
emotion_path = "output/revamp_level24/emotion_tags.json"
behavior_path = "output/revamp_level23/behavior_tags.json"
prosody_path = "output/revamp_level27/prosody_features.json"
output_path = "output/revamp_level28/vectorized_tags.json"

# Load all previous data
with open(emotion_path, "r") as f:
    emotion_data = json.load(f)["tagged_files"]

with open(behavior_path, "r") as f:
    behavior_data = json.load(f)["tagged_files"]

with open(prosody_path, "r") as f:
    prosody_data = json.load(f)

# Build final fused vector per file
fused = {}
for filename in prosody_data:
    fused[filename] = {
        "emotion": emotion_data.get(filename, "unknown"),
        "behavior": behavior_data.get(filename, "unknown"),
        "prosody": prosody_data[filename]  # includes pitch, energy, duration, etc.
    }

# Save output
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, "w") as f:
    json.dump({
        "fused_vectors": fused,
        "timestamp": str(datetime.now())
    }, f, indent=2)

print(f"✅ Level 28 complete — fused tags saved to: {output_path}")
