#!/usr/bin/env python3
import argparse
from TTS.api import TTS

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--text",       required=True)
    parser.add_argument("--emotion",    default="neutral")
    parser.add_argument("--output_path",required=True)
    args = parser.parse_args()

    # load your trained model (replace with your paths)
    tts = TTS(
      model_path="output/best_model.pth",
      config_path="output/config.json",
    )
    wav = tts.tts(
      args.text,
      speaker_idx=0,
      style_wav=None,
      emotion=args.emotion,
    )
    tts.save_wav(wav, args.output_path)

if __name__=="__main__":
    main()
