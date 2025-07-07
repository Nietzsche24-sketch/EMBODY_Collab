import sys, os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import os, sys, json
import matplotlib.pyplot as plt
from datetime import datetime
from pydub import AudioSegment
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from public_tools.firm_module import inspect_audio

INPUT_DIR = "input_audio"
OUTPUT_DIR = "output/revamp_fixed_v4"
REPORT_DIR = "output/reports_v4"
WAVEFORM_DIR = "output/waveforms_v4"

# Ensure output directories exist
for d in [OUTPUT_DIR, REPORT_DIR, WAVEFORM_DIR]:
    os.makedirs(d, exist_ok=True)

print(f"\n🧪 REVAMP Level 4 – {datetime.now().isoformat()}\n")

def generate_waveform(audio, file_path):
    samples = audio.get_array_of_samples()
    plt.figure(figsize=(8, 2))
    plt.plot(samples, linewidth=0.5)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(file_path, dpi=150)
    plt.close()

def process_file(file):
    try:
        in_path = os.path.join(INPUT_DIR, file)
        out_path = os.path.join(OUTPUT_DIR, file)
        report_path = os.path.join(REPORT_DIR, f"{file}.json")
        waveform_path = os.path.join(WAVEFORM_DIR, f"{file}.png")

        audio = AudioSegment.from_file(in_path)
        repaired = audio.set_channels(2).set_sample_width(2).set_frame_rate(44100)
        repaired = repaired.normalize()
        repaired.export(out_path, format="wav")

        metadata = inspect_audio(out_path)
        metadata["✅ Status"] = "Level 4 Repaired"
        json.dump(metadata, open(report_path, "w"), indent=2)

        generate_waveform(repaired, waveform_path)
        print(f"✅ Repaired & logged: {file}")

    except Exception as e:
        print(f"❌ Error processing {file}: {e}")

def batch_process():
    files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith((".wav", ".mp3", ".m4a"))]
    if not files:
        print("⚠️  No audio files found in input_audio/")
        return
    for file in files:
        process_file(file)

if __name__ == "__main__":
    batch_process()
