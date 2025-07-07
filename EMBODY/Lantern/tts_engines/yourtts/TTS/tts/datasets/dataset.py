class TTSDataset:
    def __init__(self, config, samples=None):
        self.samples = samples or []

    def __getitem__(self, index):
        return self.samples[index]

    def __len__(self):
        return len(self.samples)
