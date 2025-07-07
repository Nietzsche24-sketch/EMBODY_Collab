import os
import sys
import json
from datetime import datetime
from pydub import AudioSegment

# Allow importing from Lantern/public_tools/ even if script runs from root
sys.path.append(os.path.join(os.path.dirname(__file__), "Lantern", "public_tools"))
from firm_module import inspect_audio  # ✅ pulled from FIRM

# Define paths
INPUT_DIR = "input_audio"
OUTPUT_DIR = "output/revamp_fixed_v2"
REPORT_DIR = "output/reports"

# Ensure folders exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

print(f"\n🛠️  REVAMP Level 2 – {datetime.now().isoformat()}\n")

# 🔁 Core Repair + Log Function
def repair_and_log(file):
    in_path = os.path.join(INPUT_DIR, file)
    out_path = os.path.join(OUTPUT_DIR, file)
    report_path = os.path.join(REPORT_DIR, f"{file}.json")

    try:
        audio = AudioSegment.from_file(in_path)
        repaired = audio.set_channels(2).set_sample_width(2).set_frame_rate(44100)
        repaired = repaired.normalize()

        repaired.export(out_path, format="wav")

        metadata = inspect_audio(out_path)
        metadata["🛠️ Repaired From"] = in_path

        with open(report_path, "w") as f:
            json.dump(metadata, f, indent=2)

        print(f"✅ Repaired & logged: {file}")

    except Exception as e:
        print(f"❌ Error processing {file}: {e}")

# 🔁 Batch Mode
def batch_process():
    files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith((".wav", ".mp3", ".m4a"))]
    if not files:
        print("⚠️  No audio files found in input_audio/")
        return

    for file in files:
        repair_and_log(file)

# 🔁 Start
if __name__ == "__main__":
    batch_process()
