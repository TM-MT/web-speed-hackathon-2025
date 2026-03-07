#!/usr/bin/env python3
"""
Extract base64-embedded fonts from SVG files and save them to public/fonts/.
Font files are named after the font-family name.
SVG src attributes are updated to reference the external font files.
"""
import re
import base64
import sys
from pathlib import Path

repo_root = Path(__file__).parent.parent
logos_dir = repo_root / "public" / "logos"
fonts_dir = repo_root / "public" / "fonts"
fonts_dir.mkdir(parents=True, exist_ok=True)

# Pattern matches:
#   @font-face {
#     font-family: 'NAME';
#     src: url('data:font/TYPE[;params];base64,DATA') format('FORMAT');
#   }
# The [;params] part is optional (e.g., ;charset=utf-8)
FONT_FACE_PATTERN = re.compile(
    r"@font-face\s*\{\s*"
    r"font-family:\s*['\"]([^'\"]+)['\"];\s*"
    r"src:\s*url\(['\"]data:([^;]+)(?:;[^;,]+)*;base64,([^'\"]+)['\"]\)\s*"
    r"format\(['\"]([^'\"]+)['\"]\);\s*"
    r"\}",
    re.DOTALL,
)

EXT_MAP = {
    "opentype": ".otf",
    "truetype": ".ttf",
    "woff2": ".woff2",
    "woff": ".woff",
    "font/opentype": ".otf",
    "font/truetype": ".ttf",
}

svg_files = sorted(logos_dir.glob("*.svg"))
if not svg_files:
    print("No SVG files found.", file=sys.stderr)
    sys.exit(1)

total_extracted = 0
total_updated = 0

for svg_path in svg_files:
    content = svg_path.read_text(encoding="utf-8")
    if "data:font" not in content and "data:application/font" not in content:
        continue

    def replace_font_face(match: re.Match) -> str:
        font_family = match.group(1)
        data_type = match.group(2)
        base64_data = match.group(3).replace("\n", "").replace(" ", "")
        format_name = match.group(4)

        ext = EXT_MAP.get(format_name) or EXT_MAP.get(data_type, ".otf")
        font_filename = font_family + ext
        font_path = fonts_dir / font_filename

        if not font_path.exists():
            font_bytes = base64.b64decode(base64_data)
            font_path.write_bytes(font_bytes)
            size_kb = len(font_bytes) / 1024
            print(f"  Extracted: {font_filename} ({size_kb:.1f} KB)")
            global total_extracted
            total_extracted += 1

        return (
            f"@font-face{{"
            f"font-family:\"{font_family}\";"
            f"src:url('/fonts/{font_filename}') format('{format_name}')"
            f"}}"
        )

    new_content = FONT_FACE_PATTERN.sub(replace_font_face, content)

    if new_content != content:
        svg_path.write_text(new_content, encoding="utf-8")
        print(f"  Updated:   {svg_path.name}")
        total_updated += 1

print(f"\nDone: {total_extracted} font(s) extracted, {total_updated} SVG(s) updated.")
