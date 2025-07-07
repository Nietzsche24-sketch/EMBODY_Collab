import os, sys, json
import matplotlib.pyplot as plt
from datetime import datetime
from pydub import AudioSegment
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from public_tools.firm_module import inspect_audio

INPUT_DIR = "input_audio"
OUTPUT_DIR = "output/revamp_fixed_v8"
REPORT_DIR = "output/reports_v8"
WAVEFORM_DIR = "output/waveforms_v8"
SUMMARY_PATH = "output/summary_v8.csv"
DASHBOARD_PATH = "output/dashboard_v8.html"

for d in [OUTPUT_DIR, REPORT_DIR, WAVEFORM_DIR]:
    os.makedirs(d, exist_ok=True)

print(f"\n🌐 REVAMP Level 8 — {datetime.now().isoformat()}\n")

def generate_waveform(audio, file_path):
    samples = audio.get_array_of_samples()
    plt.figure(figsize=(8, 2))
    plt.plot(samples, linewidth=0.5)
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(file_path, dpi=150)
    plt.close()

def generate_diagnosis(metadata):
    score = metadata.get("🧠 Score", 0)
    issues = metadata.get("📝 Suggestions", "")
    size_kb = metadata.get("📦 File Size", "0 KB")

    diagnosis = []
    if score >= 90:
        diagnosis.append("Excellent quality. No repair needed.")
    elif score >= 60:
        diagnosis.append("Decent audio. Minor quality issues were detected.")
    else:
        diagnosis.append("Severe damage. The file was heavily corrected.")

    if "File size unusually small" in issues:
        diagnosis.append("⚠️ Warning: File size indicates potential corruption or truncation.")
    if float(size_kb.split()[0]) < 50:
        diagnosis.append("⚠️ File may be incomplete or silent.")
    
    return " ".join(diagnosis)

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
        metadata["🛠️ Status"] = "Level 8 Repaired"
        metadata["💬 Diagnosis"] = generate_diagnosis(metadata)

        json.dump(metadata, open(report_path, "w"), indent=2)
        generate_waveform(repaired, waveform_path)

        print(f"✅ Repaired & logged: {file}")

        return {
            "File": file,
            "Score": metadata.get("🧠 Score", ""),
            "Status": metadata.get("🛠️ Status", ""),
            "Diagnosis": metadata.get("💬 Diagnosis", "")
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

    # CSV Summary
    with open(SUMMARY_PATH, "w") as f:
        f.write("File,Score,Status,Diagnosis\n")
        for row in rows:
            f.write(f"{row['File']},{row['Score']},{row['Status']},{row['Diagnosis']}\n")

    # Simple HTML Dashboard
    with open(DASHBOARD_PATH, "w") as f:
        f.write("<html><head><title>REVAMP Level 8 Report</title></head><body><h1>📊 REVAMP Level 8 Results</h1><table border=1>")
        f.write("<tr><th>File</th><th>Score</th><th>Status</th><th>Diagnosis</th></tr>")
        for row in rows:
            f.write(f"<tr><td>{row['File']}</td><td>{row['Score']}</td><td>{row['Status']}</td><td>{row['Diagnosis']}</td></tr>")
        f.write("</table></body></html>")

if __name__ == "__main__":
    batch_process()
