import os
from pydub import AudioSegment, effects
from datetime import datetime

INPUT_DIR = "output/revamp_level16/reassembled"
OUTPUT_DIR = "output/revamp_level17/mastered"
os.makedirs(OUTPUT_DIR, exist_ok=True)

print(f"\n🎛️ REVAMP Level 17 — {datetime.now().isoformat()}\n")

for filename in os.listdir(INPUT_DIR):
    if filename.endswith(".wav"):
        path = os.path.join(INPUT_DIR, filename)
        audio = AudioSegment.from_wav(path)

        # Normalize volume and apply light mastering effects
        enhanced = effects.normalize(audio)
        enhanced = effects.low_pass_filter(enhanced, cutoff=15000)  # soften harsh highs
        enhanced = effects.high_pass_filter(enhanced, cutoff=60)    # remove sub-bass rumble

        output_path = os.path.join(OUTPUT_DIR, filename.replace(".wav", "_mastered.wav"))
        enhanced.export(output_path, format="wav")
        print(f"✅ Mastered: {output_path}")

print(f"\n✅ Level 17 complete.")
