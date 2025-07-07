import os, json
from datetime import datetime
from pydub import AudioSegment, silence

INPUT_DIR = "output/revamp_fixed_v4"
OUTPUT_DIR = "output/revamp_level13"
SEGMENTS_DIR = os.path.join(OUTPUT_DIR, "chunks")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(SEGMENTS_DIR, exist_ok=True)

print(f"\n🧠 REVAMP Level 13 — {datetime.now().isoformat()}\n")

def process_file(filename):
    filepath = os.path.join(INPUT_DIR, filename)
    audio = AudioSegment.from_wav(filepath)

    silent_ranges = silence.detect_silence(audio, min_silence_len=300, silence_thresh=-40)
    segments = []
    start = 0
    index = 1

    for s_start, s_end in silent_ranges:
        if s_start - start >= 500:
            chunk = audio[start:s_start]
            chunk_path = os.path.join(SEGMENTS_DIR, f"{filename[:-4]}_seg{index}.wav")
            chunk.export(chunk_path, format="wav")

            segments.append({
                "segment": index,
                "start_ms": start,
                "end_ms": s_start,
                "duration_sec": round((s_start - start) / 1000, 2),
                "path": chunk_path
            })
            index += 1
        start = s_end

    report = {
        "original_file": filename,
        "total_duration_sec": round(len(audio) / 1000, 2),
        "segment_count": len(segments),
        "segments": segments
    }

    report_path = os.path.join(OUTPUT_DIR, f"segments_{filename[:-4]}.json")
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)

    print(f"🔍 Segments extracted from {filename}: {len(segments)} saved.")

# 🔁 Loop through all WAVs
for f in os.listdir(INPUT_DIR):
    if f.endswith(".wav"):
        process_file(f)

print(f"\n✅ Level 13 complete.\n")
