# slang/rewriter.py

def rewrite_dialect(msa_text, dialect="egyptian", emotion=None, style=None):
    result = f"[{dialect.upper()}]"
    if emotion:
        result += f"[{emotion.upper()}]"
    if style:
        result += f"[{style.upper()}]"
    result += f" {msa_text}"
    return result
