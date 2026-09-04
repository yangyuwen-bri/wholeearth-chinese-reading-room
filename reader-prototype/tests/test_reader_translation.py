import json
import sys
import unittest
from unittest.mock import patch
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
        payload = march.build_payload(march.load_rows(allow_pending_review=True))
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
        self.assertIn("## 通灵解读", body)
        self.assertNotIn("“读数”", body)
        self.assertNotIn("## 读数", body)
        self.assertIn("## 普通组", body)
        self.assertIn("没有白白停止刷牙", body)
        self.assertIn("67 岁", body)
        self.assertIn("大部分时间", body)
        self.assertIn("上课前", body)

    def test_reader_uses_established_name(self):
        template = (READER / "index.html").read_text()
        self.assertNotIn("中文精读室", template)
        self.assertIn('document.title = (data.display_title || data.title) + " · 中文阅读室"', template)

    def test_complete_release_stays_blocked_by_leaf_035(self):
        with self.assertRaisesRegex(ValueError, "all leaves to be accepted"):
            march.load_rows()
        self.assertTrue(any("035" in error for error in march.validate_issue()))
        self.assertEqual(march.validate_issue(allow_pending_review=True), [])

    def test_pending_page_requires_matching_visible_notice(self):
        rows = march.load_rows(allow_pending_review=True)
        self.assertEqual(rows[35]["status"], "needs_highres_scan")
        payload = march.build_payload(rows)
        section = next(s for c in payload["chapters"] for s in c["sections"] if s["leaf"] == 35)
        self.assertIn("尚不完整", section["review_notice"])
        self.assertEqual(march.validate_reader_payload(payload), [])
        section["review_notice"] = ""
        self.assertTrue(any("035" in error for error in march.validate_reader_payload(payload)))
        rows[35].pop("reader_notice")
        with patch.object(Path, "read_text", return_value="\n".join(json.dumps(row) for row in rows)):
            with self.assertRaisesRegex(ValueError, "requires a reader notice"):
                march.load_rows(allow_pending_review=True)
        template = (READER / "index.html").read_text()
        self.assertIn("escapeHtml(sec.review_notice)", template)
        self.assertIn("编者校订说明（非原文）", template)

    def test_leaf_035_corrections_and_withdrawn_passages(self):
        body = final_translation((march.LEAF_DIR / "leaf_035.md").read_text(), 35)
        for restored in ("银铃", "列宁诞生，1870", "花朵绽放", "弗洛伊德", "卡尔·马克思", "15 日至 30 日", "2:25 am", "6:01 pm", "12:10 am"):
            self.assertIn(restored, body)
        for withdrawn in ("地球日，1970", "15:30", "呼吸，进食，出汗", "科学不愿把神话接纳为自己的兄弟", "我们的母亲生出了你们"):
            self.assertNotIn(withdrawn, body)
        self.assertLess(body.index("**4 月 21 日**"), body.index("**俳句**"))
        self.assertLess(body.index("**俳句**"), body.index("**4 月 22 日**"))

    def test_leaf_038_sender_and_source_wording(self):
        body = final_translation((march.LEAF_DIR / "leaf_038.md").read_text(), 38)
        self.assertIn("查尔斯问，他能否寄些儿童书籍给我", body)
        self.assertIn("批判性的身体能力", body)
        self.assertIn("Everett Ireon", body)


if __name__ == "__main__":
    unittest.main()
