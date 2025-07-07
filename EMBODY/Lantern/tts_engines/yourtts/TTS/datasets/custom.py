import os
import json
from TTS.utils.audio import audio_to_waveform
from TTS.utils.text.tokenizer import TTSTokenizer
from TTS.utils.speakers import SpeakerManager

def load_tts_samples(config, eval_split=True):
    input_file = config["datasets"][0]["train_filelist"] if not eval_split else config["datasets"][0]["eval_filelist"]
    samples = []
    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("|")
            if len(parts) < 2:
                continue
            audio_path, text = parts[0], parts[1]

            base_name = os.path.splitext(os.path.basename(audio_path))[0]
            emotion_path = os.path.join("emotions", base_name + ".json")
            
            if not os.path.exists(emotion_path):
                print(f"[WARN] Emotion JSON not found for {base_name}, skipping.")
                continue

            with open(emotion_path, "r", encoding="utf-8") as ef:
                emotion_data = json.load(ef)

            samples.append({
                "text": text,
                "audio_file": audio_path,
                "emotion_vector": emotion_data,
                "language": "ar",
                "speaker_name": "arabic_speaker_001",
                "audio_unique_name": base_name
            })
    return samples
