#!/usr/bin/env python3
"""Typeset exact title lines onto a text-free cover background, locally."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import sys
import unicodedata

try:
    from fontTools.ttLib import TTFont, TTLibError
    from PIL import Image, ImageColor, ImageDraw, ImageFilter, ImageFont, ImageOps
except ImportError:
    raise SystemExit(
        "Rendering dependencies are missing. Install requirements-render.txt "
        "with the Python interpreter used to run this script."
    )


SIZES = {"16:9": (1536, 864), "3:4": (1152, 1536)}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_text(lines: list[str], badge: str, accent_word: str) -> None:
    if not 1 <= len(lines) <= 2:
        raise ValueError("Provide one or two semantic title lines; text is never truncated.")
    for text in [*lines, *([badge] if badge else [])]:
        if not text or not text.strip():
            raise ValueError("Title lines and badge must not be empty.")
        if any(unicodedata.category(char) in {"Cc", "Cf", "Cs"} for char in text):
            raise ValueError("Control characters and implicit line breaks are not supported.")
    if accent_word and not any(accent_word in line for line in lines):
        raise ValueError("The accent word must occur unchanged in a title line.")


def check_glyphs(font_path: Path, font_index: int, texts: list[str]) -> None:
    with TTFont(str(font_path), fontNumber=font_index, lazy=True) as face:
        cmap = face.getBestCmap() or {}
        missing = sorted({char for text in texts for char in text if not char.isspace() and ord(char) not in cmap})
    if missing:
        sample = " ".join(f"U+{ord(char):04X}" for char in missing[:12])
        raise ValueError(f"The selected font face lacks required glyphs: {sample}. Select a complete font.")


def make_plan(font_path: Path, font_index: int, lines: list[str], badge: str, ratio: str) -> dict:
    width, height = SIZES[ratio]
    vertical = ratio == "3:4"
    safe = [math.ceil(width * .10), math.ceil(height * .10), math.floor(width * .90),
            math.floor(height * (.90 if vertical else .84))]
    x = safe[0]
    y = safe[1] if vertical else math.ceil(height * .16)
    max_width = safe[2] - x if vertical else math.floor(width * .48)
    max_height = math.floor(height * (.28 if vertical else .42))
    min_size = 48 if vertical else 36
    max_size = math.floor(width * (.14 if vertical else .09))
    for size in range(max_size, min_size - 1, -1):
        font = ImageFont.truetype(str(font_path), size, index=font_index)
        small = ImageFont.truetype(str(font_path), max(22, round(size * .48)), index=font_index)
        boxes = [font.getbbox(line, anchor="ls") for line in lines]
        badge_box = small.getbbox(badge, anchor="ls") if badge else (0, 0, 0, 0)
        padding = max(10, round(size * .14))
        gap = max(8, round(size * .18))
        badge_gap = max(16, round(size * .22)) if badge else 0
        badge_width = badge_box[2] - badge_box[0] + padding * 2 if badge else 0
        badge_height = badge_box[3] - badge_box[1] + padding * 2 if badge else 0
        total_height = sum(box[3] - box[1] for box in boxes) + gap * (len(lines) - 1) + badge_gap + badge_height
        if (max(box[2] - box[0] for box in boxes) <= max_width
                and badge_width <= max_width and total_height <= max_height):
            break
    else:
        raise ValueError("Title does not fit at a readable size. Supply shorter, approved semantic lines.")

    positions = []
    cursor = y
    for line, box in zip(lines, boxes):
        baseline = cursor - box[1]
        positions.append({
            "text": line, "origin": [x - box[0], baseline],
            "bounds": [x, cursor, x + box[2] - box[0], cursor + box[3] - box[1]],
        })
        cursor += box[3] - box[1] + gap
    badge_y = cursor - gap + badge_gap
    badge_bounds = [x, badge_y, x + badge_width, badge_y + badge_height] if badge else None
    badge_origin = [x + padding - badge_box[0], badge_y + padding - badge_box[1]] if badge else None
    all_bounds = [item["bounds"] for item in positions] + ([badge_bounds] if badge else [])
    if any(not (safe[0] <= b[0] <= b[2] <= safe[2] and safe[1] <= b[1] <= b[3] <= safe[3]) for b in all_bounds):
        raise ValueError("Computed text or badge leaves the safe area.")
    return {
        "font": font, "badge_font": small, "font_size": size,
        "lines": positions, "badge_origin": badge_origin, "badge_bounds": badge_bounds,
        "safe_bounds": safe,
    }


def render_cover(*, output: Path, font_path: Path, lines: list[str], badge: str,
                 ratio: str, background: Path | None = None, solid: str = "#edf1f2",
                 font_index: int = 0, font_source: str, font_license: str,
                 accent_word: str = "", text_color: str = "#20282b", accent_color: str = "#087d88") -> dict:
    validate_text(lines, badge, accent_word)
    if ratio not in SIZES:
        raise ValueError("This renderer supports 16:9 and 3:4; other surfaces need their own layout.")
    if output.suffix.lower() != ".png":
        raise ValueError("Output must be a new .png file.")
    if not font_source.strip() or not font_license.strip():
        raise ValueError("Record the local font source and license; no fonts are bundled.")
    if not font_path.is_file() or font_index < 0:
        raise ValueError("Supply an existing font and a nonnegative collection index.")
    check_glyphs(font_path, font_index, [*lines, badge])
    for color in [solid, text_color, accent_color]:
        if len(ImageColor.getrgb(color)) != 3:
            raise ValueError("Use opaque RGB colors.")

    artifacts = {
        "image": output,
        "thumbnail": output.with_name(output.stem + ".thumb.png"),
        "report": output.with_name(output.stem + ".qa.json"),
    }
    if any(path.exists() for path in artifacts.values()):
        raise ValueError("An output already exists. Choose a new output name; files are never overwritten.")
    if background and any(path.resolve() == background.resolve() for path in artifacts.values()):
        raise ValueError("Source and output paths must be different.")

    size = SIZES[ratio]
    canvas = Image.new("RGBA", size, solid)
    source_info = None
    if background:
        with Image.open(background) as raw:
            oriented = ImageOps.exif_transpose(raw).convert("RGBA")
        contained = ImageOps.contain(oriented, size, Image.Resampling.LANCZOS)
        offset = ((size[0] - contained.width) // 2, (size[1] - contained.height) // 2)
        canvas.alpha_composite(contained, dest=offset)
        source_info = {
            "sha256": digest(background), "oriented_size": list(oriented.size),
            "fitted_size": list(contained.size), "offset": list(offset),
            "fit": "contain-no-crop",
        }

    plan = make_plan(font_path, font_index, lines, badge, ratio)
    draw = ImageDraw.Draw(canvas)
    for item in plan["lines"]:
        draw.text(tuple(item["origin"]), item["text"], font=plan["font"], fill=text_color, anchor="ls")
        if accent_word:
            start = 0
            while (index := item["text"].find(accent_word, start)) >= 0:
                advance = plan["font"].getlength(item["text"][:index])
                draw.text((item["origin"][0] + advance, item["origin"][1]),
                          accent_word, font=plan["font"], fill=accent_color, anchor="ls")
                start = index + len(accent_word)

    if badge:
        plate = tuple(plan["badge_bounds"])
        glass = canvas.crop(plate).filter(ImageFilter.GaussianBlur(12))
        glass = Image.alpha_composite(glass, Image.new("RGBA", glass.size, (240, 245, 246, 215)))
        mask = Image.new("L", glass.size, 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, glass.width - 1, glass.height - 1), radius=8, fill=255)
        canvas.paste(glass, plate[:2], mask)
        draw = ImageDraw.Draw(canvas)
        draw.rounded_rectangle(plate, radius=8, outline=(255, 255, 255, 235), width=2)
        draw.text(tuple(plan["badge_origin"]), badge, font=plan["badge_font"], fill=text_color, anchor="ls")

    final = canvas.convert("RGB")
    thumbnail = final.resize((size[0] // 4, size[1] // 4), Image.Resampling.LANCZOS)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("xb") as stream:
        final.save(stream, format="PNG")
    with artifacts["thumbnail"].open("xb") as stream:
        thumbnail.save(stream, format="PNG")
    with Image.open(output) as saved:
        saved.load()
        if saved.size != size:
            raise ValueError("Saved image dimensions differ from the declared canvas.")
    with Image.open(artifacts["thumbnail"]) as saved:
        saved.load()
        if saved.size != thumbnail.size:
            raise ValueError("Saved thumbnail dimensions differ.")
    report = {
        "schema_version": 1, "qa_status": "manual-review",
        "image": output.name, "thumbnail": artifacts["thumbnail"].name,
        "size": list(size), "ratio": ratio, "thumbnail_size": list(thumbnail.size),
        "image_sha256": digest(output), "source": source_info,
        "title_lines": lines, "badge": badge, "accent_word": accent_word,
        "text_mode": "hybrid" if background else "controlled-typeset",
        "artifact_kind": "cover" if background else "fixture",
        "font": {
            "file_name": font_path.name, "sha256": digest(font_path), "index": font_index,
            "family_and_style": list(plan["font"].getname()), "pixel_size": plan["font_size"],
            "source": font_source, "license": font_license,
        },
        "safe_bounds": plan["safe_bounds"],
        "text_bounds": [item["bounds"] for item in plan["lines"]],
        "badge_bounds": plan["badge_bounds"],
        "automatic_checks": {"exact_size": "pass", "font_glyphs": "pass", "text_bounds": "pass", "saved_files_read_back": "pass"},
        "manual_review": [
            "Read the exact title at full size and in the thumbnail.",
            "Check contrast, original subject, face/hands, and text-free background.",
            "Check platform cropping and asset permissions before publication.",
        ],
    }
    with artifacts["report"].open("x", encoding="utf-8") as stream:
        json.dump(report, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--background", type=Path, help="Text-free image with space reserved for the title.")
    source.add_argument("--solid-background", help="RGB color; use for offline typesetting fixtures, not generated-demo claims.")
    parser.add_argument("--ratio", choices=SIZES, required=True)
    parser.add_argument("--line", action="append", required=True, help="One approved semantic title line; repeat at most twice.")
    parser.add_argument("--badge", default="", help="Optional approved secondary text; never invented.")
    parser.add_argument("--font", type=Path, required=True)
    parser.add_argument("--font-index", type=int, default=0)
    parser.add_argument("--font-source", required=True)
    parser.add_argument("--font-license", required=True)
    parser.add_argument("--accent-word", default="")
    parser.add_argument("--text-color", default="#20282b")
    parser.add_argument("--accent-color", default="#087d88")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        report = render_cover(
            output=args.output, font_path=args.font, font_index=args.font_index,
            font_source=args.font_source, font_license=args.font_license,
            lines=args.line, badge=args.badge, ratio=args.ratio, background=args.background,
            solid=args.solid_background or "#edf1f2", accent_word=args.accent_word,
            text_color=args.text_color, accent_color=args.accent_color,
        )
    except (OSError, ValueError, KeyError, IndexError, TTLibError) as exc:
        parser.error(str(exc))
    print(json.dumps({"image": str(args.output), "size": report["size"], "qa_status": report["qa_status"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
