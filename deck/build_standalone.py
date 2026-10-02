#!/usr/bin/env python3
"""docs/index.html 을 이미지·CSS·JS까지 모두 내장한 단일 HTML 파일로 만든다."""
import base64
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DOCS = os.path.join(ROOT, "docs")
SRC = os.path.join(DOCS, "index.html")
OUT = os.path.join(ROOT, "가능한_사랑_리뷰분석_발표자료.html")


def data_uri(path, mime):
    with open(path, "rb") as f:
        return f"data:{mime};base64," + base64.b64encode(f.read()).decode()


def main():
    html = open(SRC, encoding="utf-8").read()

    # 1) vendor CSS/JS 인라인
    css = open(os.path.join(DOCS, "vendor", "reveal.css"), encoding="utf-8").read()
    html = html.replace(
        '<link rel="stylesheet" href="vendor/reveal.css" />',
        f"<style>{css}</style>",
    )
    for name in ("reveal.js", "chart.umd.min.js"):
        js = open(os.path.join(DOCS, "vendor", name), encoding="utf-8").read()
        html = html.replace(
            f'<script src="vendor/{name}"></script>',
            f"<script>{js}</script>",
        )

    # 2) 이미지(assets/*.png|jpg|svg) → data URI (jpg 우선)
    def repl(match):
        block = match.group(0)
        for ext, mime in (("jpg", "image/jpeg"), ("png", "image/png"), ("svg", "image/svg+xml")):
            m = re.search(rf"assets/([\w-]+)\.{ext}", block)
            if m:
                path = os.path.join(DOCS, "assets", f"{m.group(1)}.{ext}")
                if os.path.exists(path):
                    return f"url('{data_uri(path, mime)}')"
        return block

    html = re.sub(r"url\('assets/[\w-]+\.(?:png|jpg|svg)'\)(?:,url\('assets/[\w-]+\.(?:png|jpg|svg)'\))*", repl, html)

    with open(OUT, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"built {os.path.basename(OUT)}  ({os.path.getsize(OUT):,} bytes)")
    print("remaining external refs:",
          sorted(set(re.findall(r'(?:src|href)="(https?://[^"]+)"', html))) or "none")


if __name__ == "__main__":
    main()
