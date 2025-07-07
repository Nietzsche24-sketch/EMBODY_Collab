import os
import sys
from datetime import datetime

# Add the Lantern/public_tools directory explicitly to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), "Lantern", "public_tools"))

from firm_module import inspect_audio  # From FIRM
from pydub import AudioSegment

INPUT_DIR = "input_audio"
REPAIRED_DIR = "output/revamp_fixed"

os.makedirs(REPAIRED_DIR, exist_ok=True)

print(f"\n🛠️  REVAMP Batch Audio Repair – {datetime.now().isoformat()}\n")

def batch_repair():
    files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith((".mp3", ".wav", ".m4a"))]
    if not files:
        print("⚠️  No audio files found in input_audio/")
        return

    for file in files:
        in_path = os.path.join(INPUT_DIR, file)
        out_path = os.path.join(REPAIRED_DIR, file)

        try:
            audio = AudioSegment.from_file(in_path)
            repaired = audio.set_channels(2).set_sample_width(2).set_frame_rate(44100)
            repaired.export(out_path, format="wav")
            print(f"✅ Repaired: {file}")
        except Exception as e:
            print(f"❌ Failed to repair {file}: {e}")

batch_repair()
