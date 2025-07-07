import argparse
from rewriter import SlangRewriter

parser = argparse.ArgumentParser(description="Test the S.L.A.N.G. rewriter.")
parser.add_argument("--text", type=str, required=True, help="Input English text.")
parser.add_argument("--emotion", type=str, default=None, help="Optional emotion tag (e.g. excited, angry)")

args = parser.parse_args()

rewriter = SlangRewriter()
output = rewriter.rewrite(args.text, emotion=args.emotion)

print(f"\n🔁 Rewritten: {output}")
