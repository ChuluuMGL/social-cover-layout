#!/usr/bin/env python3
"""Small deterministic package check for social-cover-layout."""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "SKILL.md",
    "README.md",
    "README.zh-CN.md",
    "LICENSE",
    "NOTICE",
    "skill.json",
    "agents/openai.yaml",
    "references/color-system.md",
    "references/visual-routes.md",
    "references/quality-gate.md",
    "TESTING.md",
    "PUBLISHING.md",
]


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def main() -> int:
    for relative in REQUIRED:
        if not (ROOT / relative).is_file():
            fail(f"missing required file: {relative}")

    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    if not skill.startswith("---\n") or "name: social-cover-layout" not in skill:
        fail("SKILL.md frontmatter is missing or has the wrong name")
    for marker in ("adaptive-composite", "generation_mode", "quality-gate"):
        if marker not in skill:
            fail(f"SKILL.md is missing marker: {marker}")

    metadata = json.loads((ROOT / "skill.json").read_text(encoding="utf-8"))
    if metadata.get("name") != "social-cover-layout":
        fail("skill.json name mismatch")
    if metadata.get("license") != "MIT":
        fail("skill.json must declare MIT")
    if metadata.get("repository") != "https://github.com/ChuluuMGL/social-cover-layout":
        fail("skill.json repository mismatch")

    for readme in (ROOT / "README.md", ROOT / "README.zh-CN.md"):
        text = readme.read_text(encoding="utf-8")
        markers = (
            ("Quick Start", "Quality", "MIT")
            if readme.name == "README.md"
            else ("3 分钟开始使用", "质量门", "MIT")
        )
        for marker in markers:
            if marker not in text:
                fail(f"{readme.name} is missing: {marker}")

    print(json.dumps({"pass": True, "files": len(REQUIRED), "version": metadata["version"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
