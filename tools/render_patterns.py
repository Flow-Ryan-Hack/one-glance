#!/usr/bin/env python3
"""Render every example in PATTERNS.md as a terminal screenshot (docs/patterns/*.png).

Usage: python3 tools/render_patterns.py   (needs Google Chrome)
"""
import html
import re
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "patterns"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
CHAR_W, LINE_H, PAD = 10.85, 24, 22  # JetBrains Mono at 18px

PAGE = """<!doctype html><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap">
<style>
html,body{{margin:0;background:transparent}}
.w{{background:#282c34;border-radius:10px;overflow:hidden;box-shadow:0 0 0 1px #3b4048;width:{w}px}}
.t{{height:32px;background:#21252b;position:relative;color:#9da5b4;font:600 13px -apple-system,sans-serif;display:flex;align-items:center;justify-content:center}}
.t i{{position:absolute;top:10px;width:12px;height:12px;border-radius:50%}}
pre{{margin:0;padding:{p}px;font:18px/{lh}px "JetBrains Mono",Menlo,monospace;color:#fff;white-space:pre}}
.g{{color:#3fb950}} .r{{color:#f85149}} .b{{color:#79c0ff}} .m{{color:#9198a1}}
</style>
<div class="w"><div class="t"><i style="left:12px;background:#ff5f57"></i><i style="left:30px;background:#febc2e"></i><i style="left:48px;background:#28c840"></i>{title}</div><pre>{body}</pre></div>"""


def colour(text):
    t = html.escape(text)
    t = t.replace("✓", '<span class="g">✓</span>').replace("✗", '<span class="r">✗</span>')
    t = re.sub(r"([█▓▒░▏▁▂▃▄▅▆▇]+)", r'<span class="b">\1</span>', t)
    return t


def main():
    md = (ROOT / "PATTERNS.md").read_text()
    OUT.mkdir(parents=True, exist_ok=True)
    for m in re.finditer(r"^## (\d+)\. (.+?)\n(.*?)(?=^## |\Z)", md, re.S | re.M):
        num, title, sec = m.group(1), m.group(2).strip(), m.group(3)
        block = re.search(r"```\n(.*?)\n```", sec, re.S)
        if not block:
            continue
        lines = block.group(1).splitlines()
        cols = max(len(l) for l in lines)
        w = int(cols * CHAR_W + 2 * PAD + 4)
        h = int(32 + len(lines) * LINE_H + 2 * PAD + 2)
        slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
        with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
            f.write(PAGE.format(w=w, p=PAD, lh=LINE_H, title=html.escape(title), body=colour(block.group(1))))
        png = OUT / f"{int(num):02d}-{slug}.png"
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        "--force-device-scale-factor=2", "--default-background-color=00000000",
                        f"--window-size={w},{h}", f"--screenshot={png}", "file://" + f.name],
                       capture_output=True, timeout=60)
        print(png.relative_to(ROOT), f"{w}x{h}")


if __name__ == "__main__":
    main()
