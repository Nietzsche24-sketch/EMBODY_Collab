import os
import wave
import contextlib
from pydub import AudioSegment

INPUT_DIR = "input_audio/"
OUTPUT_DIR = "output/revamp_level31/sliced/"
SLICE_LENGTH_MS = 3000  # 3 seconds

os.makedirs(OUTPUT_DIR, exist_ok=True)
wav_files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".wav")]

def get_duration(filename):
    with contextlib.closing(wave.open(filename, 'r')) as f:
        return f.getnframes() / float(f.getframerate())

for wav_file in wav_files:
    filepath = os.path.join(INPUT_DIR, wav_file)
    audio = AudioSegment.from_wav(filepath)
    duration = len(audio)
    slice_count = 0

    for start in range(0, duration, SLICE_LENGTH_MS):
        end = min(start + SLICE_LENGTH_MS, duration)
        sliced = audio[start:end]
        base_name = os.path.splitext(wav_file)[0]
        out_path = os.path.join(OUTPUT_DIR, f"{base_name}_slice{slice_count:03}.wav")
        sliced.export(out_path, format="wav")
        slice_count += 1

print(f"✅ Level 31 complete — sliced audio saved to: {OUTPUT_DIR}")
