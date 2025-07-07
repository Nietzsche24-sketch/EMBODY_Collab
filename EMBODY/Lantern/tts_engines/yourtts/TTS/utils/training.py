class Trainer:
    def __init__(self, config, ap, train_samples, eval_samples):
        self.config = config
        self.ap = ap
        self.train_samples = train_samples
        self.eval_samples = eval_samples

    def fit(self):
        print("[FAKE TRAINING] This is a stubbed Trainer. Training would happen here.")
