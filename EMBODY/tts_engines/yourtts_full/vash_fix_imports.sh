echo "🔧 [VASH] Starting circular import repair..."

# Step 1 - Create helpers.py if missing
HELPERS_FILE="TTS/config/helpers.py"
touch $HELPERS_FILE
cat <<EOL > TTS/config/__init__.py
from TTS.config.helpers import load_config, register_config, check_config_and_model_args
EOL

echo "✅ Slimmed down TTS/config/__init__.py to prevent cycles"
echo "🔁 Rewriting imports across codebase..."
grep -rl "from TTS.config import load_config" TTS/ | xargs sed -i '' 's/from TTS.config import load_config/from TTS.config.helpers import load_config/g'
grep -rl "from TTS.config import register_config" TTS/ | xargs sed -i '' 's/from TTS.config import register_config/from TTS.config.helpers import register_config/g'
grep -rl "from TTS.config import check_config_and_model_args" TTS/ | xargs sed -i '' 's/from TTS.config import check_config_and_model_args/from TTS.config.helpers import check_config_and_model_args/g'

cat <<EOL > TTS/configs/base_config.py
class BaseConfig: pass
class BaseAudioConfig: pass
class BaseDatasetConfig: pass
EOL

echo "✅ Injected dummy base config classes"

sed -i '' 's/from TTS.configs.shared_configs import BaseConfig/from TTS.configs.base_config import BaseConfig/g' TTS/configs/config.py
sed -i '' 's/from TTS.configs.shared_configs import BaseAudioConfig/from TTS.configs.base_config import BaseAudioConfig/g' TTS/configs/shared_configs.py
sed -i '' 's/from TTS.configs.shared_configs import BaseDatasetConfig/from TTS.configs.base_config import BaseDatasetConfig/g' TTS/configs/shared_configs.py
sed -i '' 's/from TTS.configs.shared_configs import BaseConfig/from TTS.configs.base_config import BaseConfig/g' TTS/configs/config.py
sed -i '' 's/from TTS.configs.shared_configs import BaseAudioConfig/from TTS.configs.base_config import BaseAudioConfig/g' TTS/configs/shared_configs.py
sed -i '' 's/from TTS.configs.shared_configs import BaseDatasetConfig/from TTS.configs.base_config import BaseDatasetConfig/g' TTS/configs/shared_configs.py

echo "🎉 [VASH] Circular import fix complete. You may now train again:"
echo "python3 TTS/bin/train_tts.py --config_path=config/your_config.json"
