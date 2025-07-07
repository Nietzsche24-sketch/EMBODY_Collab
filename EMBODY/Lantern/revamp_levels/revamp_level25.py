import json
import os
import datetime

behavior_path = "output/revamp_level23/behavior_tags.json"
emotion_path = "output/revamp_level24/emotion_tags.json"
output_path = "output/revamp_level25/unified_tags.json"

os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(behavior_path) as f:
    behavior_data = json.load(f).get("tagged_files", {})

with open(emotion_path) as f:
    emotion_data = json.load(f).get("tagged_files", {})

# Merge tags
unified = {}
all_keys = set(behavior_data.keys()) | set(emotion_data.keys())

for key in all_keys:
    unified[key] = {
        "emotion": emotion_data.get(key, "unknown"),
        "behavior": behavior_data.get(key, "unknown")
    }

# Save
with open(output_path, "w") as f:
    json.dump({
        "tagged_files": unified,
        "timestamp": str(datetime.datetime.now())
    }, f, indent=2)

print(f"✅ Unified tags saved to: {output_path}")
