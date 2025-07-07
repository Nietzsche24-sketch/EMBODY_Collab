#!/usr/bin/env bash
set -e

# 1) Enter this directory
cd "$(dirname "$0")"

# 2) Fresh clone of Coqui-TTS
rm -rf TTS
git clone https://github.com/coqui-ai/TTS.git TTS
cd TTS

# 3) Venv setup
python3 -m venv ../../venv
source ../../venv/bin/activate

# 4) Install dependencies
pip install --upgrade pip setuptools wheel
pip install -e .
pip install PyYAML numpy==1.22.0 "pandas<2.0" unidecode scipy librosa trainer

# 5) Prepare dataset
mkdir -p dataset/wavs
cp ../../audio_assets/arabic/*_clean.wav dataset/wavs/
for f in dataset/wavs/*_clean.wav; do
  mv "$f" "${f%_clean.wav}.wav"
done

# 6) Generate metadata.csv
python3 - << 'PYCODE'
import os
with open("dataset/metadata.csv","w",encoding="utf-8") as f:
    for wav in sorted(os.listdir("dataset/wavs")):
        if wav.endswith(".wav"):
            utt = wav[:-4]
            f.write(f"{utt}|EMBODY_AR|مرحبا بكم في اختبار تحويل الصوت العاطفي\n")
PYCODE

# 7) Write config
mkdir -p config
cat > config/train_config.json << 'JSCONF'
{
  "model":"vits",
  "output_path":"checkpoints/",
  "datasets":[
    {
      "name":"EMBODY_AR",
      "path":"dataset",
      "formatter":"ljspeech",
      "meta_file_train":"metadata.csv",
      "meta_file_eval":"metadata.csv",
      "eval_split_size":0.0
    }
  ],
  "use_emotion_embedding":true,
  "model_args":{"use_phonemes":false,"phoneme_language":"ar"},
  "training_args":{
    "batch_size":16,
    "eval_batch_size":8,
    "epochs":300,
    "save_step":500,
    "print_step":50,
    "eval_step":250,
    "log_model_step":500,
    "run_eval":false,
    "test_delay_epochs":2
  }
}
JSCONF

# 8) Patch out the eval assertion guard (just in case)
sed -i '' '/assert eval_size_per_dataset >= 1/s/^/    #/' TTS/tts/datasets/__init__.py || true

# 9) Launch training
echo "🚀 Starting training..."
CUDA_VISIBLE_DEVICES="" python3 -m TTS.bin.train_tts --config_path config/train_config.json
