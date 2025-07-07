import os, json
from datetime import datetime

TRANSCRIPTS_PATH = "output/revamp_level12/transcripts.json"
SEGMENT_SCORES_PATH = "output/revamp_level14/segment_scores.json"
OUTPUT_PATH = "output/revamp_level19/metadata_v19.json"

os.makedirs("output/revamp_level19", exist_ok=True)

print(f"\n🧱 REVAMP Level 19 — {datetime.now().isoformat()}\n")

# Load input data
with open(TRANSCRIPTS_PATH) as f:
    transcripts = json.load(f)

with open(SEGMENT_SCORES_PATH) as f:
    scores = json.load(f)

metadata = {}

for file, data in transcripts.items():
    segments = data.get("segments", [])
    enriched = []
    for i, seg in enumerate(segments):
        enriched.append({
            "text": seg["text"].strip(),
            "start": seg.get("start", 0),
            "end": seg.get("end", 0),
            "score": scores.get(file, {}).get("scores", [])[i] if i < len(scores.get(file, {}).get("scores", [])) else None,
            "length": round(seg.get("end", 0) - seg.get("start", 0), 2),
            "tokens": len(seg["text"].split())
        })
    metadata[file] = {
        "segment_count": len(enriched),
        "segments": enriched
    }

# Save result
with open(OUTPUT_PATH, "w") as f:
    json.dump(metadata, f, indent=2)

print(f"📄 Enriched metadata saved to: {OUTPUT_PATH}")
print("✅ Level 19 complete.\n")
