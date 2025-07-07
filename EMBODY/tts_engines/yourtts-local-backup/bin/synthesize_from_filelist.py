import argparse
from yourtts.config.loader import load_config
from TTS.tts.utils.synthesizer import Synthesizer

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config_path", required=True)
    parser.add_argument("--model_path", required=True)
    parser.add_argument("--filelist_path", required=True)
    parser.add_argument("--out_path", required=True)
    parser.add_argument("--use_cuda", type=bool, default=False)
    args = parser.parse_args()

    config = load_config(args.config_path)
    synthesizer = Synthesizer(
        config,
        args.model_path,
        use_cuda=args.use_cuda
    )

    with open(args.filelist_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for idx, line in enumerate(lines):
        parts = line.strip().split("|")
        wav_path, text, speaker, emotion = parts
        wav_name = wav_path.strip().split("/")[-1].replace(".wav", "_gen.wav")
        output_path = f"{args.out_path}/{wav_name}"

        wav = synthesizer.tts(text, speaker_name=speaker, emotion=emotion)
        synthesizer.save_wav(wav, output_path)

    print(f"✅ Generated {len(lines)} clips in {args.out_path}")
