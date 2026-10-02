#!/usr/bin/env python3
"""Firecrawl로 영화 '가능한 사랑' 리뷰 페이지를 검색·크롤링한다."""
import json
import os
import re
import sys
import time
import urllib.request

API = "https://api.firecrawl.dev/v1"
KEY = os.environ["FIRECRAWL_API_KEY"]
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "possible_love_reviews")
os.makedirs(OUT, exist_ok=True)


def post(path, payload):
    req = urllib.request.Request(
        f"{API}{path}",
        data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        return json.load(resp)


def slug(url):
    return re.sub(r"[^0-9A-Za-z가-힣]+", "_", url.replace("https://", "").replace("http://", ""))[:120]


def search(query, limit=10):
    result = post("/search", {"query": query, "limit": limit, "lang": "ko", "country": "kr"})
    return result.get("data", [])


def scrape(url):
    result = post("/scrape", {"url": url, "formats": ["markdown"], "onlyMainContent": True})
    return result.get("data", {})


def main():
    queries = [
        "영화 가능한 사랑 리뷰",
        "가능한 사랑 후기 결말",
        "이창동 가능한 사랑 리뷰 평론",
    ]
    seen, sources = set(), []
    for q in queries:
        for item in search(q):
            url = item.get("url", "")
            if url and url not in seen:
                seen.add(url)
                sources.append(item)
        time.sleep(1)

    search_file = os.path.join(OUT, "_search_results.json")
    with open(search_file, "w", encoding="utf-8") as f:
        json.dump(sources, f, ensure_ascii=False, indent=2)
    print(f"검색 결과 {len(sources)}건 저장: {search_file}", file=sys.stderr)

    index = []
    for i, item in enumerate(sources, 1):
        url = item["url"]
        try:
            data = scrape(url)
        except Exception as exc:  # noqa: BLE001
            print(f"[{i}/{len(sources)}] 실패 {url}: {exc}", file=sys.stderr)
            continue
        markdown = data.get("markdown", "")
        meta = data.get("metadata", {})
        name = slug(url)
        with open(os.path.join(OUT, f"{name}.md"), "w", encoding="utf-8") as f:
            f.write(f"# {meta.get('title', item.get('title', ''))}\n\n")
            f.write(f"- URL: {url}\n")
            f.write(f"- 설명: {item.get('description', '')}\n\n---\n\n{markdown}\n")
        index.append({"url": url, "title": meta.get("title") or item.get("title"), "file": f"{name}.md",
                      "chars": len(markdown)})
        print(f"[{i}/{len(sources)}] ok ({len(markdown)}자) {url}", file=sys.stderr)
        time.sleep(1)

    with open(os.path.join(OUT, "_index.json"), "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    print(f"완료: {len(index)}개 리뷰 저장 -> {OUT}", file=sys.stderr)


if __name__ == "__main__":
    main()
