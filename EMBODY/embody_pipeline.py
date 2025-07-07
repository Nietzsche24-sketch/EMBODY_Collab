from vibe.morpher import generate_wav
# embody_pipeline.py

import argparse
from salt.translate import translate_to_msa
from slang.rewriter import rewrite_dialect

def embody_pipeline(text, dialect="egyptian", emotion=None, style=None):
    # Step 1: Translate English to Modern Standard Arabic (MSA)
    msa = translate_to_msa(text)

    # Step 2: Rephrase MSA into dialect + emotion + style
    dialect_output = rewrite_dialect(
        msa,
        dialect=dialect,
        emotion=emotion,
        style=style,
    )

    return dialect_output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="EMBODY CLI: English to Arabic emotional dialect translator")

    parser.add_argument("--text", required=True, help="English sentence input")
    parser.add_argument("--dialect", default="egyptian", help="Dialect: egyptian, gulf, levant, etc.")
    parser.add_argument("--emotion", default=None, help="Emotion label, e.g., sad, angry, excited")
    parser.add_argument("--style", default=None, help="Style tag, e.g., poetic, sarcastic")

    args = parser.parse_args()

    output = embody_pipeline(
        text=args.text,
        dialect=args.dialect,
        emotion=args.emotion,
        style=args.style,
    )

    print("🗣️ Final Arabic Output:", output)
    generate_wav(output, emotion=args.emotion or "neutral", output_filename="output.wav")
