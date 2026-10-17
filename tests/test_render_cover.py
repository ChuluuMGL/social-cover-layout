"""Offline rendering and failure-path tests. No model/API calls."""

from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("render_cover", ROOT / "scripts/render_cover.py")
RENDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RENDER)


def font_path() -> Path:
    candidates = [
        os.environ.get("COVER_TEST_FONT", ""),
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/System/Library/Fonts/STHeiti Medium.ttc",
    ]
    for value in candidates:
        if value and Path(value).is_file():
            return Path(value)
    raise RuntimeError("Set COVER_TEST_FONT to a font covering Simplified Chinese and Latin; tests do not silently skip.")


class CoverTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.font = font_path()
        default_index = "2" if "NotoSansCJK" in self.font.name else "1" if "STHeiti" in self.font.name else "0"
        self.font_index = int(os.environ.get("COVER_TEST_FONT_INDEX", default_index))
        self.kwargs = dict(
            font_path=self.font, font_index=self.font_index, lines=["用AI搞定批量", "电商营销短视频"],
            badge="免费开源", font_source="local test font", font_license="not bundled",
            accent_word="批量",
        )

    def test_wide_and_vertical_dimensions_safe_bounds_and_exact_text(self):
        for ratio, size in RENDER.SIZES.items():
            with self.subTest(ratio=ratio):
                output = self.root / (ratio.replace(":", "-") + ".png")
                report = RENDER.render_cover(output=output, ratio=ratio, **self.kwargs)
                with Image.open(output) as image:
                    self.assertEqual(image.size, size)
                    self.assertGreater(len(image.getcolors(maxcolors=image.width * image.height)), 2)
                with Image.open(output.with_name(output.stem + ".thumb.png")) as thumb:
                    self.assertEqual(thumb.size, (size[0] // 4, size[1] // 4))
                saved = json.loads(output.with_name(output.stem + ".qa.json").read_text())
                self.assertEqual(saved["title_lines"], self.kwargs["lines"])
                self.assertEqual(saved["image_sha256"], RENDER.digest(output))
                self.assertEqual(saved["qa_status"], "manual-review")
                self.assertEqual(saved["text_mode"], "controlled-typeset")
                self.assertEqual(saved["artifact_kind"], "fixture")
                left, top, right, bottom = report["safe_bounds"]
                for box in report["text_bounds"] + [report["badge_bounds"]]:
                    self.assertTrue(left <= box[0] <= box[2] <= right)
                    self.assertTrue(top <= box[1] <= box[3] <= bottom)

    def test_background_is_contained_without_cropping_or_source_changes(self):
        source = self.root / "source.png"
        image = Image.new("RGB", (1672, 941), "white")
        ImageDraw.Draw(image).rectangle((1600, 0, 1671, 940), fill="red")
        image.save(source)
        before = source.read_bytes()
        output = self.root / "contained.png"
        report = RENDER.render_cover(output=output, ratio="16:9", background=source, **self.kwargs)
        self.assertEqual(source.read_bytes(), before)
        self.assertEqual(report["source"]["fit"], "contain-no-crop")
        self.assertEqual(report["text_mode"], "hybrid")
        self.assertEqual(report["artifact_kind"], "cover")
        with Image.open(output) as result:
            self.assertEqual(result.getpixel((1534, 430)), (255, 0, 0))

    def test_does_not_overwrite_existing_output_or_sidecar(self):
        output = self.root / "cover.png"
        sidecar = self.root / "cover.qa.json"
        sidecar.write_text("keep")
        with self.assertRaisesRegex(ValueError, "already exists"):
            RENDER.render_cover(output=output, ratio="3:4", **self.kwargs)
        self.assertFalse(output.exists())
        self.assertEqual(sidecar.read_text(), "keep")

    def test_rejects_missing_glyph_without_creating_output(self):
        options = dict(self.kwargs, lines=["Missing " + chr(0x10FFFF)], accent_word="")
        output = self.root / "invalid.png"
        with self.assertRaisesRegex(ValueError, "glyphs"):
            RENDER.render_cover(output=output, ratio="16:9", **options)
        self.assertFalse(output.exists())

    def test_refuses_unreadable_long_title_without_truncating(self):
        options = dict(self.kwargs, lines=["电商" * 100], accent_word="")
        with self.assertRaisesRegex(ValueError, "does not fit"):
            RENDER.render_cover(output=self.root / "long.png", ratio="3:4", **options)

    def test_rejects_invalid_lines_badge_and_accent(self):
        for changes in [
            {"lines": ["a", "b", "c"]}, {"lines": ["a\nb"]},
            {"badge": " "}, {"accent_word": "not in the title"},
        ]:
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                RENDER.render_cover(output=self.root / "bad.png", ratio="16:9", **dict(self.kwargs, **changes))

    def test_title_only_does_not_add_a_badge(self):
        report = RENDER.render_cover(
            output=self.root / "no-badge.png", ratio="3:4", **dict(self.kwargs, badge=""))
        self.assertEqual(report["badge"], "")
        self.assertIsNone(report["badge_bounds"])
        self.assertEqual(report["title_lines"], self.kwargs["lines"])

    def test_invalid_font_cli_returns_clear_error(self):
        invalid_font = self.root / "not-a-font.ttf"
        invalid_font.write_text("not a font")
        result = subprocess.run([
            sys.executable, str(ROOT / "scripts/render_cover.py"),
            "--solid-background", "white", "--ratio", "3:4", "--line", "标题",
            "--font", str(invalid_font), "--font-source", "test", "--font-license", "test",
            "--output", str(self.root / "invalid-font.png"),
        ], capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("Traceback", result.stderr)
        self.assertFalse((self.root / "invalid-font.png").exists())

    def test_cli_from_clean_installed_folder_and_unrelated_cwd(self):
        installed = self.root / ".codex/skills/social-cover-layout"
        shutil.copytree(ROOT, installed, ignore=shutil.ignore_patterns(".git", ".venv", "output", "__pycache__"))
        self.assertIn("name: social-cover-layout", (installed / "SKILL.md").read_text())
        output = self.root / "elsewhere/result.png"
        result = subprocess.run([
            sys.executable, str(installed / "scripts/render_cover.py"),
            "--solid-background", "#edf1f2", "--ratio", "16:9",
            "--line", self.kwargs["lines"][0], "--line", self.kwargs["lines"][1],
            "--badge", self.kwargs["badge"], "--font", str(self.font),
            "--font-index", str(self.font_index),
            "--font-source", "local test", "--font-license", "not bundled",
            "--output", str(output),
        ], cwd=self.root, capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["size"], [1536, 864])
        self.assertTrue(output.is_file())


if __name__ == "__main__":
    unittest.main()
