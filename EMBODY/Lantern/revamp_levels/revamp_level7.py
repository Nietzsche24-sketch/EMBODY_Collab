import os, sys, json, csv
from datetime import datetime
import matplotlib.pyplot as plt
from pydub import AudioSegment

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from public_tools.firm_module import inspect_audio

# Define paths
INPUT_DIR = "input_audio"
OUTPUT_DIR = "output/revamp_fixed_v7"
REPORT_DIR = "output/reports_v7"
WAVEFORM_DIR = "output/waveforms_v7"
SUMMARY_CSV = "output/summary_v7.csv"
DASHBOARD_HTML = "output/dashboard_v7.html"

# Make folders
for d in [OUTPUT_DIR, REPORT_DIR, WAVEFORM_DIR]:
    os.makedirs(d, exist_ok=True)

print(f"\n🌐 REVAMP Level 7 — {datetime.now().isoformat()}\n")

def generate_waveform(audio, file_path, strategy):
    samples = audio.get_array_of_samples()
    plt.figure(figsize=(8, 2))
    color = "#4CAF50" if strategy == "mild" else "#FF5722"
    plt.plot(samples, linewidth=0.5, color=color)
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(file_path, dpi=150)
    plt.close()

summary_rows = []

def process_file(file):
    try:
        in_path = os.path.join(INPUT_DIR, file)
        out_path = os.path.join(OUTPUT_DIR, file)
        report_path = os.path.join(REPORT_DIR, f"{file}.json")
        waveform_path = os.path.join(WAVEFORM_DIR, f"{file}.png")

        audio = AudioSegment.from_file(in_path)
        audio = audio.set_channels(2).set_sample_width(2).set_frame_rate(44100)

        pre_data = inspect_audio(in_path)
        score = pre_data.get("🔢 Score", 0)

        if score >= 90:
            strategy = "mild"
            repaired = audio.normalize()
        else:
            strategy = "aggressive"
            repaired = audio.low_pass_filter(3000).normalize()

        repaired.export(out_path, format="wav")

        post_data = inspect_audio(out_path)
        post_data["🛠️ Strategy"] = strategy
        post_data["✅ Status"] = "Level 7 Repaired"

        with open(report_path, "w") as f:
            json.dump(post_data, f, indent=2)

        generate_waveform(repaired, waveform_path, strategy)

        summary_rows.append({
            "File": file,
            "Score": score,
            "Strategy": strategy,
            "Waveform": waveform_path,
            "Report": report_path
        })

        print(f"✅ Repaired & logged: {file} ({strategy})")
    except Exception as e:
        print(f"❌ Error processing {file}: {e}")

def batch_process():
    files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith((".wav", ".mp3", ".m4a"))]
    if not files:
        print("⚠️  No audio files found in input_audio/")
        return

    for file in files:
        process_file(file)

    # CSV
    with open(SUMMARY_CSV, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["File", "Score", "Strategy", "Waveform", "Report"])
        writer.writeheader()
        writer.writerows(summary_rows)

    # HTML dashboard
    with open(DASHBOARD_HTML, "w") as f:
        f.write("<html><body><h2>REVAMP Level 7 Results</h2><table border='1' cellpadding='5'>")
        f.write("<tr><th>File</th><th>Score</th><th>Strategy</th><th>Waveform</th><th>Report</th></tr>")
        for row in summary_rows:
            f.write(f"<tr><td>{row['File']}</td><td>{row['Score']}</td><td>{row['Strategy']}</td>")
            f.write(f"<td><img src='{row['Waveform']}' height='40'></td>")
            f.write(f"<td><a href='{row['Report']}'>View JSON</a></td></tr>")
        f.write("</table></body></html>")

if __name__ == "__main__":
    batch_process()
