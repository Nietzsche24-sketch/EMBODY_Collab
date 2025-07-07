import unittest
from slang.rewriter import SlangRewriter
from slang.emotion_templates import templates
from slang.style_templates import styles

class TestEmotionStyleTemplates(unittest.TestCase):
    def setUp(self):
        self.rewriter = SlangRewriter()
        self.text = "هذا جنوني"

    def test_excited_emotion(self):
        output = self.rewriter.rewrite(self.text, emotion="excited")
        found = any(template.replace("{text}", "") in output for template in templates["excited"])
        self.assertTrue(found)

    def test_angry_emotion(self):
        output = self.rewriter.rewrite(self.text, emotion="angry")
        found = any(template.replace("{text}", "") in output for template in templates["angry"])
        self.assertTrue(found)

    def test_funny_style(self):
        output = self.rewriter.rewrite(self.text, style="funny")
        found = any(template.replace("{text}", "") in output for template in styles["funny"])
        self.assertTrue(found)

    def test_gentle_style(self):
        output = self.rewriter.rewrite(self.text, style="gentle")
        found = any(template.replace("{text}", "") in output for template in styles["gentle"])
        self.assertTrue(found)

if __name__ == "__main__":
    unittest.main()
