# revamp_level29.py — Summary Diagnostic
import os
import json
from datetime import datetime

INPUT_PATH = "output/revamp_level28/vectorized_tags.json"
OUTPUT_DIR = "output/revamp_level29"
OUTPUT_PATH = f"{OUTPUT_DIR}/summary_report.json"

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load vectorized tag data
with open(INPUT_PATH, "r") as f:
    data = json.load(f)

prosody_data = data["fused_vectors"]["features"]["prosody"]
emotion = data["fused_vectors"]["features"].get("emotion", "unknown")
behavior = data["fused_vectors"]["features"].get("behavior", "unknown")

# Build summary per file
summary = {}
for filename, stats in prosody_data.items():
    summary[filename] = {
        "duration_sec": stats.get("duration_sec"),
        "loudness_rms": round(stats.get("avg_rms", 0), 4),
        "pitch_mean": stats.get("pitch_mean"),
        "tempo_bpm": stats.get("tempo_bpm"),
        "emotion_tag": emotion,
        "behavior_tag": behavior
    }

# Save to JSON
with open(OUTPUT_PATH, "w") as f:
    json.dump({
        "summary": summary,
        "timestamp": datetime.now().isoformat()
    }, f, indent=2)

print("📊 Diagnostic Summary — Level 29 Complete")
print(f"✅ Report saved to: {OUTPUT_PATH}")
