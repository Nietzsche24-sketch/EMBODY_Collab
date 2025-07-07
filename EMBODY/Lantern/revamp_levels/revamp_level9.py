import os, sys, json
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from pydub import AudioSegment, silence
import scipy.io.wavfile as wav
from scipy.signal import spectrogram

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from public_tools.firm_module import inspect_audio

INPUT_DIR = "input_audio"
OUTPUT_DIR = "output/revamp_fixed_v9"
REPORT_DIR = "output/reports_v9"
WAVEFORM_DIR = "output/waveforms_v9"
SPECTRO_DIR = "output/spectrograms_v9"
SUMMARY_PATH = "output/summary_v9.csv"

for d in [OUTPUT_DIR, REPORT_DIR, WAVEFORM_DIR, SPECTRO_DIR]:
    os.makedirs(d, exist_ok=True)

print(f"\n🌐 REVAMP Level 9 — {datetime.now().isoformat()}\n")

def generate_waveform(audio, file_path):
    samples = audio.get_array_of_samples()
    plt.figure(figsize=(8, 2))
    plt.plot(samples, linewidth=0.5)
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(file_path, dpi=150)
    plt.close()

def generate_spectrogram(wav_path, out_path):
    rate, data = wav.read(wav_path)
    if len(data.shape) > 1:  # stereo to mono
        data = data.mean(axis=1)
    f, t, Sxx = spectrogram(data, fs=rate)
    plt.pcolormesh(t, f, 10 * np.log10(Sxx), shading='gouraud')
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [s]')
    plt.title("Spectrogram")
    plt.colorbar(label='Intensity [dB]')
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()

def detect_silence(audio):
    silences = silence.detect_silence(audio, min_silence_len=2000, silence_thresh=-40)
    return len(silences), silences

def generate_diagnosis(metadata, num_silences):
    score = metadata.get("🧠 Score", 0)
    diagnosis = []
    if score >= 90:
        diagnosis.append("🎧 High fidelity.")
    elif score >= 60:
        diagnosis.append("🟡 Moderate quality.")
    else:
        diagnosis.append("🔴 Audio issues detected.")

    if num_silences > 0:
        diagnosis.append(f"⚠️ {num_silences} silent segment(s) detected.")

    return " ".join(diagnosis)

def process_file(file):
    try:
        in_path = os.path.join(INPUT_DIR, file)
        out_path = os.path.join(OUTPUT_DIR, file)
        report_path = os.path.join(REPORT_DIR, f"{file}.json")
        waveform_path = os.path.join(WAVEFORM_DIR, f"{file}.png")
        spectro_path = os.path.join(SPECTRO_DIR, f"{file}.png")

        audio = AudioSegment.from_file(in_path)
        repaired = audio.set_channels(2).set_sample_width(2).set_frame_rate(44100).normalize()
        repaired.export(out_path, format="wav")

        metadata = inspect_audio(out_path)
        num_silences, silent_ranges = detect_silence(repaired)
        metadata["🔇 Silences"] = num_silences
        metadata["🛠️ Status"] = "Level 9 Repaired"
        metadata["💬 Diagnosis"] = generate_diagnosis(metadata, num_silences)

        json.dump(metadata, open(report_path, "w"), indent=2)
        generate_waveform(repaired, waveform_path)
        generate_spectrogram(out_path, spectro_path)

        print(f"✅ Repaired & logged: {file}")
        return {
            "File": file,
            "Score": metadata.get("🧠 Score", ""),
            "Silences": num_silences,
            "Status": metadata["🛠️ Status"],
            "Diagnosis": metadata["💬 Diagnosis"]
        }

    except Exception as e:
        print(f"❌ Error processing {file}: {e}")
        return None

def batch_process():
    files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith((".wav", ".mp3", ".m4a"))]
    if not files:
        print("⚠️ No audio files found in input_audio/")
        return
    
    rows = []
    for f in files:
        result = process_file(f)
        if result:
            rows.append(result)

    with open(SUMMARY_PATH, "w") as f:
        f.write("File,Score,Silences,Status,Diagnosis\n")
        for r in rows:
            f.write(f"{r['File']},{r['Score']},{r['Silences']},{r['Status']},{r['Diagnosis']}\n")

if __name__ == "__main__":
    batch_process()
