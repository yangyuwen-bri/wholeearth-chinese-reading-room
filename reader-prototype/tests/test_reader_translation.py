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

    def test_display_title_never_moves_an_internal_heading(self):
        body = "承接上页的正文。\n\n## 第二篇文章\n\n第二篇正文。"
        self.assertEqual(split_display_title(body, "原书第 36 页"), ("原书第 36 页", body))
        self.assertEqual(split_display_title("\n\n## 页首标题\n正文。", "页码"), ("页首标题", "正文。"))


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

    def test_front_pages_retain_restored_source_units(self):
        required = {
            0: ("释放博比", "地上倒下的瓶身", "Southpaw"),
            2: ("梦结束了",),
            5: ("贝蒂·克罗克", "玛姬的农场", "Bob Hunter", "Robert Service", "Jerry Garcia"),
            6: ("让我惊讶的并不是奇迹本身", "二十五美分", "大麻脂", "只是来打个招呼"),
            7: ("口述予", "Stewart Brand Name", "两则寓言", "狗拉具"),
            8: ("剑桥大学生殖生理学教授", "制止犯罪教科书", "家长们，有烟就要查", "燃烧的蜡烛", "Dick Tracy"),
            9: ("Planetary People", "Ed Rosenfeld", "BARNES"),
            10: ("心理科学在消极方面", "精神病理学", "Rumi the Persian"),
            12: ("三吨粪肥", "吞下蜜蜂", "免费讲座", "Prof. Batty", "血浆养老金"),
            13: ("笨鸟", "宇宙之书", "不怎么好笑", "灌木"),
        }
        for leaf, phrases in required.items():
            body = final_translation((march.LEAF_DIR / f"leaf_{leaf:03d}.md").read_text(), leaf)
            for phrase in phrases:
                with self.subTest(leaf=leaf, phrase=phrase):
                    self.assertIn(phrase, body)

    def test_leaf_005_poems_and_leaf_012_cartoon_keep_boundaries(self):
        body = final_translation((march.LEAF_DIR / "leaf_005.md").read_text(), 5)
        self.assertEqual(body.count("我还曾<br>"), 4)
        self.assertGreaterEqual(markdown_to_html(body).count("<br>"), 34)
        self.assertLess(body.index("Bob Hunter"), body.index("**指针**"))
        self.assertLess(body.index("Robert Service"), body.index("Jerry Garcia"))
        body = final_translation((march.LEAF_DIR / "leaf_012.md").read_text(), 12)
        self.assertLess(body.index("踢人屁股的滑稽鬼屋"), body.index("**漫画**"))
        self.assertLess(body.index("**漫画**"), body.index("等他们回来时"))
        self.assertNotIn("等离子养老金", body)

    def test_reopened_small_print_has_visible_notices_and_blocks_release(self):
        rows = march.load_rows(allow_pending_review=True)
        payload = march.build_payload(rows)
        errors = march.validate_issue()
        for leaf in (8, 11):
            with self.subTest(leaf=leaf):
                self.assertEqual(rows[leaf]["status"], "needs_highres_scan")
                section = next(s for c in payload["chapters"] for s in c["sections"] if s["leaf"] == leaf)
                self.assertIn("尚不完整", section["review_notice"])
                self.assertTrue(any(f"{leaf:03d}" in error for error in errors))

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

    def test_leaf_034_caption_prose_and_repeated_lyrics(self):
        body = final_translation((march.LEAF_DIR / "leaf_034.md").read_text(), 34)
        for restored in ("Ron Boise", "Thunder Machine", "Peter & Helen Ready", "几乎真真切切的阴影", "Onward Christian Soldiers", "©"):
            self.assertIn(restored, body)
        self.assertNotIn("一字不差的阴影", body)
        self.assertIn("无论如何，<br>\n无论如何，<br>\n无论如何，<br>", body)

    def test_leaf_036_diagram_poetry_and_footnotes(self):
        body = final_translation((march.LEAF_DIR / "leaf_036.md").read_text(), 36)
        for restored in ("Hills of the Conscious", "Waters Below", "1：矿物", "2：植物", "3：动物", "4：人", "The Anima", "The Animus", "Terra Firma", "世界精神", "从自身分送到人类这棵树中", "自然、万物之母", "诸天、万物之父"):
            self.assertIn(restored, body)
        self.assertEqual(body.count("映照在"), 2)
        self.assertNotIn("衡量这种魔法", body)
        self.assertNotIn("卡文", body)
        html = markdown_to_html(body)
        self.assertIn("阴＊", html)
        self.assertIn("阳＊", html)
        self.assertIn("＊《易经》", html)
        self.assertGreaterEqual(html.count("<br>"), 29)

    def test_leaf_037_hitchhiking_fidelity(self):
        body = final_translation((march.LEAF_DIR / "leaf_037.md").read_text(), 37)
        for restored in ("水瓶座电能", "休班的美军士兵", "抽大麻", "竖拇指搭车", "最后一处还能搭便车", "R. Hunter", "Fidel Castro", "The Modesto Kid", "我们中的七个人"):
            self.assertIn(restored, body)
        for mistranslation in ("下班的警察", "最不可能搭便车", "按拇指"):
            self.assertNotIn(mistranslation, body)
        self.assertEqual(markdown_to_html(body).count("<br>"), 7)
        title, rendered_body = split_display_title(body, "原书第 36 页")
        self.assertEqual(title, "原书第 36 页")
        self.assertLess(rendered_body.index("R. Hunter"), rendered_body.index("## 致健康迷组织"))


if __name__ == "__main__":
    unittest.main()
