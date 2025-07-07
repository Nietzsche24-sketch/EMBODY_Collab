import argparse
from translator import SALTTranslator

parser = argparse.ArgumentParser()
parser.add_argument("--text", type=str, required=True, help="Text to translate")
parser.add_argument("--src", type=str, default="en", help="Source language (default: en)")
parser.add_argument("--tgt", type=str, default="ar", help="Target language (default: ar)")
args = parser.parse_args()

translator = SALTTranslator(src_lang=args.src, tgt_lang=args.tgt)
output = translator.translate(args.text)

print(f"\n🌐 Translated: {output}")
