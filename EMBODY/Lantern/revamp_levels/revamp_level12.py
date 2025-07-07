import os, json, whisper
from datetime import datetime
from pathlib import Path

INPUT_DIR = "output/revamp_fixed_v4"
OUTPUT_DIR = "output/revamp_level12"
TRANSCRIPTS = "output/revamp_level12/transcripts.json"

os.makedirs(OUTPUT_DIR, exist_ok=True)

print(f"\n🧠 REVAMP Level 12 — {datetime.now().isoformat()}\n")

model = whisper.load_model("base")

transcripts = {}

for filename in os.listdir(INPUT_DIR):
    if not filename.endswith(".wav"):
        continue

    in_path = os.path.join(INPUT_DIR, filename)
    print(f"🔍 Analyzing: {filename}...")

    result = model.transcribe(in_path)
    text = result["text"]

    # Simple heuristic name generation
    stem_words = [w.lower() for w in text.split() if w.isalpha() and len(w) > 3]
    stem = "_".join(stem_words[:4]) or "untitled"
    safe_stem = stem.replace("/", "_").replace("\\", "_")

    new_name = f"{safe_stem}.wav"
    out_path = os.path.join(OUTPUT_DIR, new_name)

    os.rename(in_path, out_path)
    print(f"✅ Renamed to: {new_name}")

    transcripts[filename] = {
        "transcript": text.strip(),
        "new_name": new_name
    }

with open(TRANSCRIPTS, "w") as f:
    json.dump(transcripts, f, indent=2)

print(f"\n📝 Transcripts saved to {TRANSCRIPTS}")
print("✅ Level 12 complete.\n")
