#!/bin/bash
# Usage: ./tools/extract_text.sh books_clean/book.pdf books_clean/book.txt

PDF="$1"
TXT="$2"

if [[ ! -f "$PDF" ]]; then
  echo "❌ PDF not found: $PDF"
  exit 1
fi

python3 - <<PY
from PyPDF2 import PdfReader
reader = PdfReader("$PDF")
text = "\n".join([page.extract_text() or "" for page in reader.pages])
with open("$TXT", "w") as f:
    f.write(text)
PY

echo "✅ Extracted text to $TXT"
