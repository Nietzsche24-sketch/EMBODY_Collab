from TTS.api import TTS
import os

# === Path to your manually downloaded model
model_dir = os.path.expanduser("~/.local/share/tts/tts_models--ar--mai--tacotron2-DDC")

# === Load model
tts = TTS(model_path=os.path.join(model_dir, "model.pth"),
          config_path=os.path.join(model_dir, "config.json"))

# === Synthesize Arabic text
output_path = "cloned_outputs/test_arabic.wav"
os.makedirs("cloned_outputs", exist_ok=True)

tts.tts_to_file(
    text="مرحبا بكم في النسخة التجريبية من النظام العاطفي",
    file_path=output_path
)

print(f"✅ Arabic speech synthesized to: {output_path}")
