from dataclasses import dataclass, field
from TTS.config.shared_configs import BaseDatasetConfig

@dataclass
class CustomDatasetConfig(BaseDatasetConfig):
    speaker_name: str = field(default="peter", metadata={"help": "Name of the speaker."})
