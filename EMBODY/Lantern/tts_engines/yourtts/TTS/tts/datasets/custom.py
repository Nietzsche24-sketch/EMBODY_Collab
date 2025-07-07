import os
import csv

# ✅ Minimal BaseFormatter dummy for YourTTS
class BaseFormatter:
    def __init__(self, *args, **kwargs):
        pass

def load_metadata(root_path, meta_file, ignored_speakers=None):
    path = os.path.join(root_path, meta_file)
    metadata = []

    with open(path, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="|")
        for row in reader:
            if len(row) < 2:
                continue
            wav_file, text = row[0], row[1]
            metadata.append({
                "audio_file": wav_file.strip(),
                "text": text.strip(),
                "speaker_name": "peter",
                "language": "ar"
            })

    return metadata

class CustomFormatter(BaseFormatter):
    pass
