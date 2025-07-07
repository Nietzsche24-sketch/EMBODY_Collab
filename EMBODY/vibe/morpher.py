# vibe/morpher.py

import os
import subprocess

YOURTTS_DIR = "tts_engines/yourtts_full"
WAV_OUTPUT_DIR = "audio_assets/final_wav"

os.makedirs(WAV_OUTPUT_DIR, exist_ok=True)

def generate_wav(text, emotion="neutral", output_filename="output.wav"):
    output_path = os.path.join(WAV_OUTPUT_DIR, output_filename)

    command = [
        "python3",
        f"{YOURTTS_DIR}/inference.py",
        "--text", text,
        "--emotion", emotion,
        "--output_path", output_path,
    ]

    print("🌀 Synthesizing voice...")
    subprocess.run(command, check=True)
    print(f"✅ Saved to: {output_path}")

    return output_path
