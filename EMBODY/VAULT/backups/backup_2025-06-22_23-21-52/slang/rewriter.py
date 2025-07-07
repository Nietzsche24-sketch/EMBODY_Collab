import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)
import json
import re
import random
from .emotion_templates import templates
from .style_templates import styles

# Dialect conversion: MSA → selected dialect (default = Egyptian)
def dialectify(text, dialect="egy"):
    path = f"slang/dialects/{dialect}.json"
    with open(path, encoding="utf-8") as f:
        mapping = json.load(f)
    for pattern, replacement in mapping.items():
        text = re.sub(pattern, replacement, text)
    return text

# S.L.A.N.G. engine
class SlangRewriter:
    def __init__(self, slang_path="slang/slang_map.json"):
        with open(slang_path, encoding="utf-8") as f:
            self.slang_map = json.load(f)

    def rewrite(self, text, emotion=None, style=None, dialect="egy"):
        # Normalize curly quotes
        text = text.replace("’", "'").replace("‘", "'")

        # Step 1: MSA → Dialect
        text = dialectify(text, dialect=dialect)

        # Step 2: Slang replacement
        for pattern, replacement in self.slang_map.items():
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

        # Step 3: Emotion template
        if emotion and emotion in templates:
            template = random.choice(templates[emotion])
            text = template.replace("{text}", text)

        # Step 4: Style template
        if style and style in styles:
            template = random.choice(styles[style])
            text = template.replace("{text}", text)

        return text
