# revamp_level32.py — Prosody Embedding for Sliced WAVs
import os
import torchaudio
import json
from datetime import datetime

INPUT_DIR = "output/revamp_level31/sliced"
OUTPUT_PATH = "output/revamp_level32/prosody_embeddings.json"
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

def extract_prosody(wav_path):
    waveform, sample_rate = torchaudio.load(wav_path)
    duration_sec = waveform.size(1) / sample_rate
    rms = waveform.pow(2).mean().sqrt().item()
    zcr = torchaudio.transforms.ComputeDeltas()(waveform).abs().mean().item()
    pitch_mean = waveform.mean().item() * 1000
    pitch_std = waveform.std().item() * 1000
    return {
        "duration_sec": round(duration_sec, 2),
        "avg_rms": round(rms, 5),
        "zcr": round(zcr, 5),
        "pitch_mean": round(pitch_mean, 2),
        "pitch_std": round(pitch_std, 2)
    }

embeddings = {}

for fname in os.listdir(INPUT_DIR):
    if fname.endswith(".wav"):
        fpath = os.path.join(INPUT_DIR, fname)
        print(f"🔍 Extracting: {fname}")
        embeddings[fname] = extract_prosody(fpath)

# Save result
with open(OUTPUT_PATH, "w") as f:
    json.dump({
        "prosody_embeddings": embeddings,
        "timestamp": datetime.now().isoformat()
    }, f, indent=2)

print(f"✅ Level 32 complete — embeddings saved to: {OUTPUT_PATH}")
