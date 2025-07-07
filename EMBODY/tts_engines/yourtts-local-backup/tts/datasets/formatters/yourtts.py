def yourtts(root_path, meta_file, **kwargs):
    with open(meta_file, "r", encoding="utf-8") as f:
        lines = [line.strip().split("|") for line in f]

    samples = []
    for line in lines:
        wav_path, text, speaker_name, language = line
        samples.append({
            "text": text,
            "speaker_name": speaker_name,
            "audio_file": wav_path,
            "language": language,
        })
    return samples
