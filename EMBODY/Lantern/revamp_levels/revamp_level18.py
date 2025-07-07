import os
from pydub import AudioSegment
from datetime import datetime

INPUT_DIR = "output/revamp_level17"
EXPORT_DIR = "output/revamp_level18/exports"
os.makedirs(EXPORT_DIR, exist_ok=True)

print(f"\n🎧 REVAMP Level 18 — {datetime.now().isoformat()}\n")

formats = ['mp3', 'ogg', 'flac']
exported = []

for file in os.listdir(INPUT_DIR):
    if file.endswith(".wav"):
        name = os.path.splitext(file)[0]
        path = os.path.join(INPUT_DIR, file)
        audio = AudioSegment.from_wav(path)

        for fmt in formats:
            out_path = os.path.join(EXPORT_DIR, f"{name}.{fmt}")
            audio.export(out_path, format=fmt)
            exported.append(f"{name}.{fmt}")

if exported:
    print("✅ Exported formats:")
    for f in exported:
        print(f"   • {f}")
else:
    print("⚠️ No WAV files found in Level 17 output.")

print("\n📁 Exports saved to:", EXPORT_DIR)
print("✅ Level 18 complete.\n")
