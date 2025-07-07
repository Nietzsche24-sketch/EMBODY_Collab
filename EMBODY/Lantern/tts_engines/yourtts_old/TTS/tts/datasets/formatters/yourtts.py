from TTS.tts.datasets.formatters.base import BaseDatasetFormatter
import os

class YourttsFormatter(BaseDatasetFormatter):
    def load_metadata(self, root_path, meta_file, **kwargs):
        with open(meta_file, encoding="utf-8") as f:
            lines = f.readlines()
        return [self.parse_item(line, root_path, meta_file) for line in lines]

    def parse_item(self, line, root_path, meta_path):
        parts = line.strip().split("|")
        wav_path = os.path.join(root_path, parts[0])
        text = parts[1]
        language = parts[2] if len(parts) > 2 else "en"
        speaker = "peter"  # fixed speaker name
        audio_name = os.path.splitext(os.path.basename(wav_path))[0]

        return {
            "text": text,
            "audio_file": wav_path,
            "language": language,
            "speaker_name": speaker,
            "audio_unique_name": audio_name
        }
