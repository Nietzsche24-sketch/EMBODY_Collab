import argparse
import os
import sys

# ✅ Make sure EMBODY root is in the import path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from rewriter import SlangRewriter
from salt.translator import SALTTranslator
# Add path to import translator if needed

parser = argparse.ArgumentParser()
parser.add_argument("--text", type=str, required=True, help="Input English text")
parser.add_argument("--emotion", type=str, help="Emotion label (optional)")
parser.add_argument("--style", type=str, help="Style label (optional)")
args = parser.parse_args()

# Step 1: Translate EN → MSA
salt = SALTTranslator()
msa_text = salt.translate(args.text)
print(f"\n🌐 MSA: {msa_text}")

# Step 2: Rewrite via SLANG (includes dialect + emotion)
rewriter = SlangRewriter()
egyptian_text = rewriter.rewrite(msa_text, emotion=args.emotion)

print(f"\n🗣️ Egyptian Rewrite: {egyptian_text}")
