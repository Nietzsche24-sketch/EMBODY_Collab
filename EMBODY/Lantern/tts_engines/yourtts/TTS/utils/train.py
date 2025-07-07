from TTS.utils.training import Trainer
from TTS.utils.audio import AudioProcessor
from TTS.utils.io import load_config
from TTS.tts.utils.datasets import load_tts_samples

def train():
    config = load_config("config/train_config.json")
    ap = AudioProcessor(**config.audio)
    train_samples, eval_samples = load_tts_samples(**config.datasets[0])
    trainer = Trainer(config, ap, train_samples, eval_samples)
    trainer.fit()
