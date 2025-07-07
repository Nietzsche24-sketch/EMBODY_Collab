import os
import datetime
import subprocess
import json

INPUT_DIR = "input_audio"
OUTPUT_DIR = "output/revamp_level10"
TRANSCRIPTS_DIR = os.path.join(OUTPUT_DIR, "transcripts")
REPORT_FILE = os.path.join(OUTPUT_DIR, "report_v10.json")

os.makedirs(TRANSCRIPTS_DIR, exist_ok=True)
report = {}

print(f"\n🧠 REVAMP Level 10 — {datetime.datetime.now().isoformat()}\n")

for filename in os.listdir(INPUT_DIR):
    if not filename.lower().endswith((".wav", ".mp3", ".m4a")):
        continue

    base = os.path.splitext(filename)[0]
    input_path = os.path.join(INPUT_DIR, filename)
    transcript_txt = os.path.join(TRANSCRIPTS_DIR, f"{base}.txt")
    transcript_json = os.path.join(TRANSCRIPTS_DIR, f"{base}.json")

    print(f"🔍 Transcribing {filename}...")

    # Transcribe using Whisper CLI (make sure it's installed globally)
    result = subprocess.run([
        "whisper", input_path,
        "--model", "base",
        "--output_format", "all",
        "--output_dir", TRANSCRIPTS_DIR
    ], capture_output=True, text=True)

    if result.returncode != 0:
        print(f"❌ Whisper failed on {filename}: {result.stderr}")
        continue

    # Load timestamped transcript
    try:
        with open(transcript_json, "r") as f:
            transcript_data = json.load(f)
    except Exception as e:
        print(f"❌ Failed to read JSON for {filename}: {e}")
        continue

    # Basic diagnostics
    duration = transcript_data.get("duration", 0)
    segments = transcript_data.get("segments", [])
    word_count = sum(len(seg.get("text", "").split()) for seg in segments)
    silences = sum(1 for seg in segments if seg["text"].strip() == "")

    report[filename] = {
        "duration_seconds": round(duration, 2),
        "word_count": word_count,
        "empty_segments": silences,
        "segments": segments
    }

    print(f"✅ Transcribed & analyzed: {filename}")

# Save full report
with open(REPORT_FILE, "w") as f:
    json.dump(report, f, indent=2)

print(f"\n📄 Full report saved to: {REPORT_FILE}")
print("✅ Level 10 complete.\n")
