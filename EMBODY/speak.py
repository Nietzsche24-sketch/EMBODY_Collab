#!/usr/bin/env python3
# speak.py — EMBODY | V.I.B.E. Arabic TTS CLI

import os
import sys
import json
import torch
import argparse
from pathlib import Path
from typing import Literal

# === Inject YourTTS local path ===
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), "Lantern", "tts_engines", "yourtts_src")
))

# === YourTTS core imports ===
from TTS.tts.models.vits import Vits
from TTS.utils.audio import AudioProcessor
from TTS.config import load_config
from TTS.utils.synthesizer import Synthesizer

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("text", type=str, help="🗣 Arabic text to synthesize")
    parser.add_argument("output_path", type=str, help="📁 Path to save output .wav")
    parser.add_argument("--run-dir", type=str,
                        default="Lantern/tts_engines/yourtts_src/train_output/embody_run-Jun-18-2025_05+53-Arabic",
                        help="📦 Path to model dir with config.json + best_model.pth")
    parser.add_argument("--device", type=str, choices=["cpu", "cuda"], default="cpu",
                        help="⚙️  Device to run inference on")
    args = parser.parse_args()

    print(f"📂 Injected TTS path: {sys.path[0]}")
    config_path = os.path.join(args.run_dir, "config.json")
    model_path = os.path.join(args.run_dir, "best_model.pth")

    print("📥 Loading model + config...")
    config = load_config(config_path)
    model = Vits.init_from_config(config)
    model.load_checkpoint(config, model_path, eval=True)
    model.to(args.device)

    ap = AudioProcessor.init_from_config(config)
    speaker = config.speakers[0] if hasattr(config, "speakers") and config.speakers else ""
    synthesizer = Synthesizer(model, config, None, speaker_manager=None, use_cuda=(args.device == "cuda"))

    print(f"🗣 Synthesizing: {args.text}")
    wav = synthesizer.tts(args.text, speaker_name=speaker)
    ap.save_wav(wav, args.output_path)
    print(f"✅ Output saved: {args.output_path}")

if __name__ == "__main__":
    main()
