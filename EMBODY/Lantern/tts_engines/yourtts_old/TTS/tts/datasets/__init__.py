from TTS.tts.datasets.formatters import yourtts

def load_tts_samples(*args, **kwargs):
    root_path = "."
    meta_file_train = "filelists/train_filelist.txt"
    meta_file_val = "filelists/val_filelist.txt"
    ignored_speakers = []

    # Create an instance of the formatter
    formatter = yourtts.YourttsFormatter()

    # Load metadata separately
    train_samples = formatter.load_metadata(
        root_path, meta_file_train, ignored_speakers=ignored_speakers
    )
    val_samples = formatter.load_metadata(
        root_path, meta_file_val, ignored_speakers=ignored_speakers
    )

    return train_samples, val_samples
