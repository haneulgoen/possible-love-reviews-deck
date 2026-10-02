#!/usr/bin/env python3
"""data.json을 template.html에 인라인해 docs/index.html 을 생성한다."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
docs = os.path.join(ROOT, "docs")
os.makedirs(docs, exist_ok=True)

tpl = open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
data = json.load(open(os.path.join(HERE, "data.json"), encoding="utf-8"))
data_js = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
html = tpl.replace("__DATA__", data_js)

out = os.path.join(docs, "index.html")
with open(out, "w", encoding="utf-8") as f:
    f.write(html)
print(f"built {out} ({len(html):,} bytes)")
