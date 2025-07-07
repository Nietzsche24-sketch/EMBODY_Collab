from TTS.tts.datasets.formatters import BaseFormatter

class yourtts(BaseFormatter):
    def parse_item(self, line: str):
        parts = line.strip().split("|")
        if len(parts) == 5:
            wav_path, text, lang, speaker, style = parts
        elif len(parts) == 3:
            wav_path, text, speaker = parts
            lang = "en"
            style = "neutral"
        else:
            raise ValueError(f"Line format incorrect: {line}")
        return {
            "wav": wav_path,
            "text": text,
            "language": lang,
            "speaker_name": speaker,
            "style_wav": None,
            "style": style,
        }
