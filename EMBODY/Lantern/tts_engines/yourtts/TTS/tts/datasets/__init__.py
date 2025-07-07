from TTS.tts.datasets.custom import CustomFormatter as custom  # ✅ DIRECT IMPORT
import sys
import TTS.tts.datasets.custom  # ✅ ← Plain import, not "as custom"
from .custom import load_metadata as custom   # <-- this makes “custom” visible
from TTS.tts.datasets.dataset import *

def _get_formatter_by_name(name):
    if name.lower() == "custom":
        return TTS.tts.datasets.custom.load_metadata  # ✅ Fully qualified path

    thismodule = sys.modules[__name__]
    return getattr(thismodule, name.lower())
