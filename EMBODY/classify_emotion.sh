MODEL="superb/wav2vec2-base-superb-er"

python3 - <<PYCODE 2>/dev/null
import logging, sys
from transformers import pipeline

# silence all Transformers logs
logging.getLogger("transformers").setLevel(logging.ERROR)

pipe = pipeline(
  "audio-classification",
  model="$MODEL",
  device=-1,    # CPU
  top_k=1       # only the top label
)

for wav in sys.argv[1:]; do
    r = pipe(wav)[0]
    print(f"{wav}\t{r['label']}\t{r['score']:.3f}")
PYCODE
