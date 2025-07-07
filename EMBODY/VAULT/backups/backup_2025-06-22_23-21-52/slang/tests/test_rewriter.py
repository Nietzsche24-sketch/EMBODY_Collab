import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from rewriter import SlangRewriter

rewriter = SlangRewriter()

tests = {
    "That’s crazy!": "ده جنان",
    "Seriously, you did that?": "بجد",
    "No way.": "مستحيل",
    "Come on, man.": "يلا بقى"
}

for original, expected in tests.items():
    output = rewriter.rewrite(original)
    assert expected in output, f"❌ {original} → {output} (Expected: {expected})"

print("✅ All S.L.A.N.G. tests passed.")
print("🔊 Emotion Test:", rewriter.rewrite("That's crazy!", emotion="excited"))
