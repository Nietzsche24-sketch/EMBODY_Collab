import os
from pydub import AudioSegment
from datetime import datetime

CHUNKS_DIR = "output/revamp_level13/chunks"
OUTPUT_DIR = "output/revamp_level16/reassembled"
os.makedirs(OUTPUT_DIR, exist_ok=True)

print(f"\n🧩 REVAMP Level 16 — {datetime.now().isoformat()}\n")

# Organize chunks by base filename
chunks_map = {}
for f in os.listdir(CHUNKS_DIR):
    if f.endswith(".wav") and "_" in f:
        base = f.split("_chunk")[0]
        chunks_map.setdefault(base, []).append(f)

# Merge chunks in order
for base, files in chunks_map.items():
    files.sort(key=lambda x: int(x.split("_chunk")[1].split(".")[0]))
    merged = AudioSegment.empty()
    for f in files:
        path = os.path.join(CHUNKS_DIR, f)
        merged += AudioSegment.from_file(path)
    output_path = os.path.join(OUTPUT_DIR, base + "_reassembled.wav")
    merged.export(output_path, format="wav")
    print(f"✅ Reassembled: {base}_reassembled.wav")

print(f"\n✅ Level 16 complete.")
