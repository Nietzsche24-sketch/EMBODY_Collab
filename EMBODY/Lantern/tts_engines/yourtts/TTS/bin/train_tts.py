from TTS.utils.manage import run
from TTS.utils.audio import AudioProcessor
from TTS.tts.configs.shared_configs import BaseDatasetConfig
from TTS.config.shared_configs import BaseAudioConfig
from TTS.tts.configs.vits_config import VitsConfig
from TTS.tts.models.vits import Vits
from TTS.tts.datasets import load_tts_samples
from TTS.tts.utils.text.tokenizer import TTSTokenizer

def main():
    config = VitsConfig()
    config.audio = BaseAudioConfig()
    config.datasets = [
        BaseDatasetConfig(
            formatter="custom",
            meta_file_train="metadata.csv",
            path="dataset"
        )
    ]
    ap = AudioProcessor.init_from_config(config)
    tokenizer, config = TTSTokenizer.init_from_config(config)
    train_samples, eval_samples = load_tts_samples(config.datasets[0], eval_split=True)
    model = Vits(config, ap, tokenizer, speaker_manager=None)
    run(model, config, train_samples, eval_samples)

if __name__ == "__main__":
    main()
