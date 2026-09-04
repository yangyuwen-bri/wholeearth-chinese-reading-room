import json
import sys
import unittest
from pathlib import Path


READER = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(READER))

import build_march_1971_last_supplement_reader_data as march
from build_translation_reader_data import final_translation, markdown_to_html, split_display_title


class FinalTranslationTests(unittest.TestCase):
    def test_preserves_internal_headings_and_repeated_content(self):
        body = "## 第一篇\n\n正文。\n\n## 第二篇\n\n正文。\n\n### 订购\n\n价格：$2。"
        source = f"## Final Translation\n\n{body}\n\n## Omitted Bibliographic/Order Info\n\n无。"
        self.assertEqual(final_translation(source, 39), body)

    def test_excludes_workflow_notes(self):
        for ending in ("Omitted Bibliographic/Order Info", "OCR / Uncertainty Notes", "Self Critique"):
            with self.subTest(ending=ending):
                source = f"## Final Translation\n正文。\n\n## {ending}\n内部记录。"
                self.assertEqual(final_translation(source, 0), "正文。")

    def test_eof_and_crlf(self):
        self.assertEqual(final_translation("## Final Translation\n正文。", 0), "正文。")
        self.assertEqual(final_translation("## Final Translation\r\n正文。\r\n## Self Critique\r\n内部", 0), "正文。")

    def test_missing_translation_raises(self):
        with self.assertRaises(ValueError):
            final_translation("## Source Pack\n证据", 0)


class MarchReaderTests(unittest.TestCase):
    def test_coverage_gate_rejects_dropped_page_and_truncated_body(self):
        payload = march.build_payload(march.load_rows())
        self.assertEqual(march.validate_reader_payload(payload), [])
        section = next(s for c in payload["chapters"] for s in c["sections"] if s["leaf"] == 39)
        section["html"] = "<p>只剩第一篇。</p>"
        self.assertTrue(any("039" in e for e in march.validate_reader_payload(payload)))
        payload["chapters"][-1]["sections"].pop()
        self.assertTrue(march.validate_reader_payload(payload))

    def test_all_132_published_pages_match_complete_translation(self):
        payload = json.loads(march.OUT.read_text())
        sections = [section for chapter in payload["chapters"] for section in chapter["sections"]]
        self.assertEqual([section["leaf"] for section in sections], list(range(132)))
        for section in sections:
            leaf = section["leaf"]
            source = (march.LEAF_DIR / f"leaf_{leaf:03d}.md").read_text()
            # Deliberately do not use the production section extractor as the oracle.
            complete = source.split("## Final Translation\n", 1)[1].split(
                "\n## Omitted Bibliographic/Order Info\n", 1
            )[0].strip()
            title, body = split_display_title(complete, section["title"])
            with self.subTest(leaf=leaf):
                self.assertEqual(section["title"], title)
                self.assertEqual(section["html"], markdown_to_html(body))

    def test_leaf_039_keeps_both_previously_dropped_sections(self):
        source = (march.LEAF_DIR / "leaf_039.md").read_text()
        body = final_translation(source, 39)
        self.assertIn("## 读数", body)
        self.assertIn("## 普通组", body)
        self.assertIn("没有白白停止刷牙", body)
        self.assertIn("67 岁", body)
        self.assertIn("大部分时间", body)
        self.assertIn("上课前", body)

    def test_reader_uses_established_name(self):
        template = (READER / "index.html").read_text()
        self.assertNotIn("中文精读室", template)
        self.assertIn('document.title = (data.display_title || data.title) + " · 中文阅读室"', template)


if __name__ == "__main__":
    unittest.main()
