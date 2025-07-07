import unittest
from slang.rewriter import SlangRewriter

class TestDialectRewrites(unittest.TestCase):
    def setUp(self):
        self.rewriter = SlangRewriter()

    def test_egyptian(self):
        out = self.rewriter.rewrite("هذا الآن", dialect="egy")
        self.assertIn("ده", out)
        self.assertIn("دلوقتي", out)

    def test_gulf(self):
        out = self.rewriter.rewrite("هذا الآن", dialect="gulf")
        self.assertIn("هاذا", out)
        self.assertIn("الحين", out)

    def test_levant(self):
        out = self.rewriter.rewrite("هذا الآن", dialect="levant")
        self.assertIn("هاذا", out)
        self.assertIn("هلق", out)

if __name__ == "__main__":
    unittest.main()
