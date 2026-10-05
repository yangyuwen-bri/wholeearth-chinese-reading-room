import json
import subprocess
import sys
import unittest
from unittest.mock import patch
from pathlib import Path


READER = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(READER))

import build_march_1971_last_supplement_reader_data as march
from build_translation_reader_data import final_translation, markdown_to_html, split_display_title


class FinalTranslationTests(unittest.TestCase):
    def test_thematic_break_is_not_literal_text(self):
        self.assertEqual(markdown_to_html("前一则。\n\n---\n\n后一则。"), "<p>前一则。</p><hr><p>后一则。</p>")
        self.assertEqual(markdown_to_html("- 前项\n---\n> 后引文"), "<ul><li>前项</li></ul><hr><blockquote><p>后引文</p></blockquote>")

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
    def test_minor_exception_cannot_hide_notice_or_waive_calendar_prose(self):
        rows = march.load_rows(allow_pending_review=True)
        rows[62]["reader_notice"] = ""
        rows[34]["source_exception"] = "Unapproved prose waiver"
        original_read = Path.read_text
        def read_text(path, *args, **kwargs):
            if path == march.STATUS_PATH:
                return "\n".join(json.dumps(row) for row in rows)
            return original_read(path, *args, **kwargs)
        with patch.object(Path, "read_text", read_text):
            errors = march.validate_issue()
        self.assertIn("leaf 062: source exception requires accepted status and reader notice", errors)
        self.assertIn("leaf 034: no authorized minor source exception", errors)

    def test_hazlitt_quote_keeps_predicate(self):
        body = final_translation((march.LEAF_DIR / "leaf_062.md").read_text(), 62)
        self.assertIn("差异所触动", body)

    def test_current_preface_matches_authorized_exception_count(self):
        rows = march.load_rows()
        notice = next(s["html"] for s in march.PREFACE if s["title"] == "校订说明")
        exceptions = [row for row in rows if row.get("source_exception")]
        self.assertIn(f"{len(rows)} 页可供阅读", notice)
        self.assertIn(f"{len(exceptions)} 页按用户授权", notice)
        self.assertIn("第 34 页", notice)
        self.assertIn("不是另一位审校者的独立验收", notice)

    def test_kesey_translation_is_consistent_in_last_pages(self):
        for leaf in (127, 128, 130):
            body = final_translation((march.LEAF_DIR / f"leaf_{leaf:03d}.md").read_text(), leaf)
            self.assertIn("凯西", body)
            self.assertNotIn("克西", body)

    def test_restored_late_book_units_are_not_summarized(self):
        required = {
            104: ("麻醉药品成瘾", "Vintage"),
            105: ("1969年4月13日",),
            106: ("350 人", "5,000 美元"),
            107: ("CN 221", "SNOOPY", "SCHULZ"),
            108: ("TOMOLLY",),
            111: ("在楼上跳舞啊",),
            113: ("GUINDON",),
            114: ("第二次世界大战", "出价最高的人", "Michael Dreyfuss"),
            115: ("波多黎各", "维尔京群岛", "Lineaweaver", "Cairns"),
            116: ("Sudbury Inn", "K. S. Cotton", "Cynthia Nielson", "259½", "Jim Zerdan"),
            117: ("Richard Zander", "Joseph Kruszka", "James A. Stumm", "Carl Sagan", "3½", "11363"),
            118: ("2528 Q Street", "Robert S. Philleo", "Michael A. Eiss", "Tim Reitz<br>\nBox 145"),
            119: ("Carolyn Biggerstajj", "Carl Wimmer", "Loran V. Melnick"),
            120: ("Conrad", "Ina Haugen", "1475½", "James Miles"),
            121: ("Alan Luecke", "Apt. 2106", "824½", "81·1"),
            122: ("Tom Lauverman", "11651¾", "11219¾", "Fied Ler"),
            123: ("1103 Paloma No. 1", "San Diego, CA 62109", "Palo Alto, CA 04303"),
            124: ("Masae Namba", "Clairmont Heights Enterprizes", "2233½", "2943½", "512 I Street"),
            125: ("Jean Mollinson", "2770 Bellevue Avenue", "论沉默", "它不等待任何东西", "11664½"),
            126: ("梅赫·巴巴资料处", "Box 1101"),
            127: ("圣阿尔弗雷德", "FM 广播", "AM 广播", "记者证可免费索取", "PO Box 10121", "每年 4 美元"),
            128: ("——SB", "448 页", "十三周年", "肯尼迪那本书中被删去的部分"),
            129: ("6 月 11 日，星期五", "带点好吃的、好喝的，给别人享用", "你们一共多少人"),
            130: ("滑石粉", "帮助穿上", "也许还有点紧张"),
            131: ("目录", "而温顺的人", "许可证待批"),
        }
        for leaf, phrases in required.items():
            body = final_translation((march.LEAF_DIR / f"leaf_{leaf:03d}.md").read_text(), leaf)
            for phrase in phrases:
                with self.subTest(leaf=leaf, phrase=phrase):
                    self.assertIn(phrase, body)

    def test_checked_directory_records_survive_export(self):
        for leaf, count in ((115, 203), (116, 242), (117, 240), (118, 243),
                            (119, 230), (120, 239), (121, 235), (122, 238),
                            (123, 246), (124, 246), (125, 213)):
            body = final_translation((march.LEAF_DIR / f"leaf_{leaf:03d}.md").read_text(), leaf)
            with self.subTest(leaf=leaf):
                self.assertEqual(sum("<br>" in block for block in body.split("\n\n")), count)
                self.assertNotIn("```", body)
                self.assertNotIn("以下姓名、机构、邮寄地址", body)
        body = final_translation((march.LEAF_DIR / "leaf_118.md").read_text(), 118)
        self.assertEqual(body.count("L. M. Ledbetter"), 2)
        self.assertLess(body.index("2413 Maryland, Avenue"), body.index("Mr. T. Rawson"))
        body = final_translation((march.LEAF_DIR / "leaf_125.md").read_text(), 125)
        # 214 entries: 213 multi-line records and one printed name without an address.
        self.assertEqual(body.count("John Wilcox"), 2)
        self.assertIn("\n\nJohn Wilcox\n\nJohn Wilcox<br>", body)

    def test_retired_directory_copier_cannot_overwrite_checked_files(self):
        package = march.LEAF_DIR.parent
        paths = [package / "status.jsonl"] + list(march.LEAF_DIR.glob("leaf_1[12][0-9].md"))
        before = {path: path.read_bytes() for path in paths}
        result = subprocess.run(
            [sys.executable, str(package / "tools/build_directory_leaves.py")],
            capture_output=True, text=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Directory generation is disabled", result.stderr)
        self.assertEqual(before, {path: path.read_bytes() for path in paths})

    def test_late_music_and_report_pages_keep_restored_units(self):
        required = {
            79: ("北斗七星", "北极星"),
            83: ("Highway 1", "VAGABONDS", "D.C. al Coda", "我不会独自背负这份罪责"),
            84: ("不能推荐抑制剂", "DIXIE CUPS", "LORD BUCKLEY"),
            85: ("微型巴士", "免邮原样寄回", "尼尔心中的目标"),
            87: ("Monologue with Future Shock", "跑到乡村公社"),
            89: ("问一个选民", "政客本人不知道"),
            93: ("HERE I AM!", "——8 岁", "印第安人"),
            95: ("Ransom", "其实是送给那位朋友的"),
            97: ("Get The Lead Out", "全部乘客出行里程"),
            98: ("向人民开战", "把它还给印第安人", "THE MILITARY", "巴基斯坦地震"),
            99: ("Nancy Mann", "第 179 页"),
        }
        for leaf, phrases in required.items():
            body = final_translation((march.LEAF_DIR / f"leaf_{leaf:03d}.md").read_text(), leaf)
            for phrase in phrases:
                with self.subTest(leaf=leaf, phrase=phrase):
                    self.assertIn(phrase, body)
        lyrics = final_translation((march.LEAF_DIR / "leaf_083.md").read_text(), 83)
        self.assertEqual(lyrics.count("我是你们的诗人。"), 2)
        self.assertEqual(lyrics.count("原谅我们吧，啊，最后的孤独与困苦者。"), 2)

    def test_historical_medical_and_gas_notices_stay_outside_source(self):
        rows = march.load_rows(allow_pending_review=True)
        for leaf in (73, 74, 94, 96, 97, 98, 100, 101, 102, 103, 111, 127, 130):
            with self.subTest(leaf=leaf):
                notice = rows[leaf]["reader_notice"]
                self.assertIn("非原文", notice)
                body = final_translation((march.LEAF_DIR / f"leaf_{leaf:03d}.md").read_text(), leaf)
                self.assertNotIn(notice, body)
        self.assertIn("切勿模仿", rows[96]["reader_notice"])

    def test_corrected_food_pages_keep_units_and_steps(self):
        body = final_translation((march.LEAF_DIR / "leaf_059.md").read_text(), 59)
        for phrase in ("Shambala", "6 杯温水", "2 汤匙酵母（2 包）", "2 杯奶粉", "2 杯大麦面粉", "1-1/2 茶匙盐", "耳垂", "涂过油", "350°F 烤 1-1/2 小时"):
            self.assertIn(phrase, body)
        self.assertNotIn("燕麦", body)
        self.assertLess(body.index("莎拉说"), body.index("### 藏式大麦面包"))
        self.assertLess(body.index("涂过油"), body.index("### 关于埃德"))

    def test_resolved_signature_and_separate_historical_safety_notices(self):
        rows = march.load_rows(allow_pending_review=True)
        self.assertEqual(rows[8]["status"], "accepted")
        self.assertIn("Cieciorka", final_translation((march.LEAF_DIR / "leaf_008.md").read_text(), 8))
        for leaf in (50, 51):
            self.assertIn("非原文", rows[leaf]["reader_notice"])
            self.assertNotIn("美国国家癌症研究所的资料", final_translation((march.LEAF_DIR / f"leaf_{leaf:03d}.md").read_text(), leaf))

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
            title, body = march.split_page_title(complete, section["title"], leaf)
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

    def test_interview_and_inserted_pages_retain_source_boundaries(self):
        bodies = {leaf: final_translation((march.LEAF_DIR / f"leaf_{leaf:03d}.md").read_text(), leaf)
                  for leaf in range(14, 22)}
        self.assertIn("GOSLOW", bodies[14])
        self.assertIn("印第安人", bodies[14])
        self.assertNotIn("SNS", bodies[16])
        self.assertIn("它超出了联邦调查局全部技术所能触及的范围", bodies[16])
        self.assertIn("《每日新闻》", bodies[16])
        self.assertIn("目的就不能使手段正当化", bodies[16])
        self.assertIn("## 枪", bodies[17])
        self.assertIn("13:11", bodies[17])
        self.assertEqual(markdown_to_html(bodies[17]).count("<br>"), 5)
        self.assertIn("金钱战", bodies[18])
        self.assertNotIn("猴子战术", bodies[18])
        self.assertEqual(bodies[18].count("偷这本书。（"), 9)
        self.assertIn("否”（Negative）", bodies[19])
        self.assertIn("PATSALOS", bodies[20])
        self.assertIn("被打乱顺序征召", bodies[20])
        self.assertIn("4-F", bodies[21])
        self.assertIn("Ramparts of Clay", bodies[21])
        self.assertLess(bodies[21].index("**罗宾：**"), bodies[21].index("## 蓝幽灵"))
        self.assertLess(bodies[21].index("## 蓝幽灵"), bodies[21].index("## 来自气象局"))

    def test_authorized_source_exceptions_have_visible_notices(self):
        rows = march.load_rows(allow_pending_review=True)
        payload = march.build_payload(rows)
        errors = march.validate_issue()
        for leaf in (35,):
            with self.subTest(leaf=leaf):
                self.assertEqual(rows[leaf]["status"], "accepted")
                section = next(s for c in payload["chapters"] for s in c["sections"] if s["leaf"] == leaf)
                self.assertIn("用户授权", section["review_notice"])
                self.assertIn("不作猜补", section["review_notice"])
                self.assertFalse(any(f"leaf {leaf:03d}:" in error for error in errors))
        for leaf in (11, 62, 84, 86):
            with self.subTest(authorized_minor_exception=leaf):
                self.assertEqual(rows[leaf]["status"], "accepted")
                self.assertIn("用户允许", rows[leaf]["source_exception"])
                self.assertIn("不作猜补", rows[leaf]["reader_notice"])
                self.assertFalse(any(f"leaf {leaf:03d}:" in error for error in errors))
        self.assertIn("source_exception", rows[35])
        self.assertEqual(len(errors), 0)
        # The matching color painting resolves leaf 082's suspected inscription
        # as architecture and seated figures, not omitted source text.
        self.assertEqual(rows[82]["status"], "accepted")
        section = next(s for c in payload["chapters"] for s in c["sections"] if s["leaf"] == 82)
        self.assertFalse(section.get("review_notice"))

    def test_law_and_computer_pages_restore_omitted_units(self):
        bodies = {leaf: final_translation((march.LEAF_DIR / f"leaf_{leaf:03d}.md").read_text(), leaf)
                  for leaf in range(22, 26)}
        for phrase in ("Weather Underground", "武元甲", "州议会大厦", "L. Clark Stevens"):
            self.assertIn(phrase, bodies[22])
        self.assertIn("引导那只握着铅笔的手", bodies[23])
        self.assertIn("吞噬自身", bodies[23])
        self.assertLess(bodies[23].index("John Manos"), bodies[23].index("## 法律"))
        for phrase in ("Jab", "KK", "Yabe Yablonsky", "天翻地覆的震撼"):
            self.assertIn(phrase, bodies[24])
        self.assertEqual(markdown_to_html(bodies[24]).count("<br>"), 7)
        for phrase in ("1984", "13 年", "军方情报机构", "南非市场", "137 West 14th Street"):
            self.assertIn(phrase, bodies[25])
        self.assertNotIn("中情局", bodies[25])
        self.assertNotIn("南亚的活动", bodies[25])
        self.assertEqual(markdown_to_html(bodies[25]).count("<li>"), 5)
        self.assertIn("第 14 期", bodies[25])

    def test_mantras_sufism_yoga_and_lyrics_restore_source_units(self):
        bodies = {leaf: final_translation((march.LEAF_DIR / f"leaf_{leaf:03d}.md").read_text(), leaf)
                  for leaf in range(26, 34)}
        for phrase in ("这咒语不卖钱", "要有信心", "六十个世纪", "审计者", "皮套"):
            self.assertIn(phrase, bodies[27])
        self.assertIn("## 苏菲主义", bodies[28])
        self.assertIn("2.45 美元", bodies[28])
        self.assertLess(bodies[29].index("在水上行走的人"), bodies[29].index("从 Bindu 到 Ojas"))
        self.assertIn("重新上船", bodies[29])
        for phrase in ("ॐ 15", "ॐ CVII", "悖论　悖论　悖论　悖论"):
            self.assertIn(phrase, bodies[30])
        self.assertNotIn("15 美元", bodies[30])
        self.assertIn("把潜在的视为永恒的", bodies[31])
        self.assertIn("7. 执着", bodies[31])
        self.assertIn("FRISCO", bodies[32])
        for phrase in ("诸神的黄昏", "二十英里", "伍德斯托克", "头盔", "斯库拉"):
            self.assertIn(phrase, bodies[33])
        self.assertGreaterEqual(markdown_to_html(bodies[33]).count("<br>"), 33)

    def test_reader_uses_established_name(self):
        template = (READER / "index.html").read_text()
        self.assertNotIn("中文精读室", template)
        self.assertIn('document.title = (data.display_title || data.title) + " · 中文阅读室"', template)

    def test_complete_release_allows_authorized_leaf_035(self):
        rows = march.load_rows()
        self.assertEqual(rows[35]["status"], "accepted")
        self.assertIn("source_exception", rows[35])
        self.assertEqual(march.validate_issue(), [])

    def test_authorized_page_requires_matching_visible_notice(self):
        rows = march.load_rows()
        self.assertEqual(rows[35]["status"], "accepted")
        payload = march.build_payload(rows)
        section = next(s for c in payload["chapters"] for s in c["sections"] if s["leaf"] == 35)
        self.assertIn("次要的年历插页", section["review_notice"])
        self.assertEqual(march.validate_reader_payload(payload), [])
        section["review_notice"] = ""
        self.assertTrue(any("035" in error for error in march.validate_reader_payload(payload)))
        rows[35].pop("reader_notice")
        with patch.object(Path, "read_text", return_value="\n".join(json.dumps(row) for row in rows)):
            errors = march.validate_issue()
        self.assertIn("leaf 035: source exception requires accepted status and reader notice", errors)
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
