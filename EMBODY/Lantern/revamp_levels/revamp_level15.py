import os, json
from datetime import datetime
from pydub import AudioSegment

INPUT_DIR = "output/revamp_level13/chunks"
SCORES_PATH = "output/revamp_level14/segment_scores.json"
OUTPUT_DIR = "output/revamp_level15/fixed_chunks"
os.makedirs(OUTPUT_DIR, exist_ok=True)

print(f"\n🛠️ REVAMP Level 15 — {datetime.now().isoformat()}\n")

# Load health scores
with open(SCORES_PATH) as f:
    scores = json.load(f)

fixed_count = 0

for file, data in scores.items():
    status = data.get("🧪 Status", "")
    if "Issues" in status or "Likely" in status:
        in_path = os.path.join(INPUT_DIR, file)
        out_path = os.path.join(OUTPUT_DIR, file)
        try:
            audio = AudioSegment.from_file(in_path)
            repaired = audio.set_channels(2).set_sample_width(2).set_frame_rate(44100)
            repaired.export(out_path, format="wav")
            print(f"🧬 Repaired: {file}")
            fixed_count += 1
        except Exception as e:
            print(f"❌ Failed to repair {file}: {e}")

print(f"\n✅ Level 15 complete. Segments repaired: {fixed_count}")
