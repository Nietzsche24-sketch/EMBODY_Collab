import os
from TTS.tts.datasets.utils import load_tts_samples
from TTS.tts.datasets.formatters.base import BaseDatasetFormatter  # <-- ✅ use the real source
class YourttsFormatter(BaseDatasetFormatter):
    def __init__(self, meta_file_train, meta_file_val, dataset_config, eval_split=True):
        super().__init__(meta_file_train, meta_file_val, dataset_config, eval_split)

    def load_meta_data(self):
        return load_tts_samples(self.meta_file_train, self.meta_file_val, self.dataset_config, self.eval_split)
