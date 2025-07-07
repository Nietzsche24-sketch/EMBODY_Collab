# ✅ Explicit import from your new file
from TTS.tts.configs.custom_config import CustomDatasetConfig as BaseDatasetConfig
import json
import os

def load_metadata(dataset_config, eval_split=False):
    meta_file = dataset_config.meta_file_eval if eval_split else dataset_config.meta_file_train
    path = os.path.join(dataset_config.path, meta_file)

    with open(path, encoding='utf-8') as f:
        entries = json.load(f)

    metadata = []
    for entry in entries:
        metadata.append({
            "audio_file": entry["wav"],
            "text": entry["text"],
            "speaker_name": dataset_config.speaker_name,
            "language": dataset_config.language
        })

    return metadata
