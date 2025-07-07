from dataclasses import dataclass, field
from TTS.config.shared_configs import BaseDatasetConfig

@dataclass
class MyDatasetConfig(BaseDatasetConfig):
    speaker_name: str = field(default="peter", metadata={"help": "Default speaker name."})
