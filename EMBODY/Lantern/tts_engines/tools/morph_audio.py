import os
import json
from pydub import AudioSegment

def apply_morph(wav_path, vector_path, output_path):
    audio = AudioSegment.from_wav(wav_path)
    audio.export(output_path, format="wav")

def main(args):
    os.makedirs(args.output_dir, exist_ok=True)
    for json_file in sorted(os.listdir(args.vector_dir)):
        if not json_file.endswith(".json"): continue
        base = json_file.replace(".json", "")
        wav_file = os.path.join(args.input_dir, f"{base}_clean.wav")
        if not os.path.exists(wav_file):
            print(f"❌ Missing WAV: {wav_file}")
            continue
        json_path = os.path.join(args.vector_dir, json_file)
        output_path = os.path.join(args.output_dir, f"{base}_clean.wav")
        apply_morph(wav_file, json_path, output_path)
        print(f"✅ Morphed: {output_path}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", required=True)
    parser.add_argument("--vector_dir", required=True)
    parser.add_argument("--output_dir", required=True)
    args = parser.parse_args()
    main(args)
