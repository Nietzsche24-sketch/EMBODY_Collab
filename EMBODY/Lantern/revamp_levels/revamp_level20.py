import os, json
from datetime import datetime

INPUT_PATH = "output/revamp_level19/metadata_v19.json"
TRANSCRIPTS_PATH = "output/revamp_level12/transcripts.json"
OUTPUT_PATH = "output/revamp_level20/report_v20.json"

os.makedirs("output/revamp_level20", exist_ok=True)

print(f"\n🧽 REVAMP Level 20 — {datetime.now().isoformat()}\n")

with open(INPUT_PATH) as f:
    metadata = json.load(f)

with open(TRANSCRIPTS_PATH) as f:
    transcripts = json.load(f)

final_report = {}

for file, meta in metadata.items():
    cleaned_segments = [
        s for s in meta["segments"]
        if s["text"].strip() and s["length"] > 0
    ]
    final_name = file.replace("untitled", "processed").replace(".wav", "").strip()

    final_report[final_name] = {
        "segment_count": len(cleaned_segments),
        "total_words": sum(s["tokens"] for s in cleaned_segments),
        "total_duration": round(sum(s["length"] for s in cleaned_segments), 2),
        "segments": cleaned_segments
    }

with open(OUTPUT_PATH, "w") as f:
    json.dump(final_report, f, indent=2)

print(f"📄 Final report saved to: {OUTPUT_PATH}")
print("✅ Level 20 complete.\n")
