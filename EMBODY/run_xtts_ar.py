import torch
from TTS.api import TTS

# 1. Allowlist the XTTS config & audio config classes for safe loading
import TTS.tts.configs.xtts_config as _cfg
import TTS.tts.models.xtts as _m
torch.serialization.add_safe_globals([
    _cfg.XttsConfig,
    _m.XttsAudioConfig,
])

# 2. Instantiate the model (will prompt ToS if not already downloaded)
tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2")

# 3. Synthesize to file, passing speaker & language explicitly
tts.tts_to_file(
    text="هذا اختبار للتأكد من أن كل شيء يعمل بشكل كامل.",
    speaker="female-en-5",
    language="ar",
    file_path="final_xtts_arabic.wav",
)

print("✅ Audio written to final_xtts_arabic.wav")
