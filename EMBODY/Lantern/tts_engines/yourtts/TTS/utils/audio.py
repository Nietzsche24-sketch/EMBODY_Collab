class AudioProcessor:
    def __init__(self, config):
        self.sample_rate = config.get("audio", {}).get("sample_rate", 22050)

    def load_wav(self, path):
        print(f"[AUDIO STUB] Pretending to load WAV from {path}")
        return None

    def save_wav(self, audio, path):
        print(f"[AUDIO STUB] Pretending to save WAV to {path}")
