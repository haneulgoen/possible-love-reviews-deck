#!/usr/bin/env python3
"""가능한 사랑 리뷰 데이터를 분석해 슬라이드용 data.json을 만든다."""
import glob
import json
import os
import re
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
from build_rating_review_csv import ROWS  # noqa: E402
from build_review_summary_csv import ROWS as SUMMARY_ROWS  # noqa: E402
from split_reviews_by_type import CRITIC, AUDIENCE, EXPERT_ROWS  # noqa: E402


def classify(media, kind):
    if (media, kind) in CRITIC:
        return "평론가"
    if (media, kind) in AUDIENCE:
        return "일반 관객"
    return "기타"


def to100(media, kind, score):
    """개별 평점을 0~100으로 정규화(가능한 경우)."""
    s = str(score)
    try:
        if media == "씨네21" or media == "IMDb":
            return round(float(s) * 10, 1)
        if media == "왓챠피디아" or media == "키노라이츠" or media == "Letterboxd":
            return round(float(s) * 20, 1)
        if media == "메타크리틱":
            return round(float(s), 1)
        if media == "로튼토마토":
            if "/" in s:  # e.g. 4/4, 3.5/4, 9/10
                a, b = s.split("/")
                return round(float(a) / float(b) * 100, 1)
            if s == "Fresh":
                return 100.0
            if s == "B":
                return 85.0
    except (ValueError, ZeroDivisionError):
        pass
    return None


KEYWORDS = [
    "계급", "사랑", "욕망", "노동", "카메라", "시선", "연대", "이해", "거리",
    "달", "호루라기", "불편", "자본", "돈", "부부", "가족", "트라우마", "해고",
    "다큐", "예술", "윤리", "탐", "계명", "감정", "희망", "바다", "선의",
    "공감", "죄책감", "존엄", "권력", "이창동", "전도연", "설경구",
]


def analyze():
    by_cat = Counter()
    by_media = Counter()
    dist = {"평론가": [], "일반 관객": [], "전문가": []}
    quotes = {"평론가": [], "일반 관객": []}
    sentiment = Counter()

    for media, agg, n, kind, author, score, summary, url in ROWS:
        cat = classify(media, kind) if kind != "" else "기타"
        norm = to100(media, kind, score)
        by_media[media] += 1
        by_cat[cat] += 1
        if norm is not None:
            dist[cat].append({"media": media, "author": author, "score": score, "norm": norm})
        # 감성
        if norm is None:
            sentiment["긍정"] += 1
        elif norm >= 80:
            sentiment["긍정"] += 1
        elif norm >= 60:
            sentiment["혼합"] += 1
        else:
            sentiment["부정"] += 1
        if cat in quotes and len(quotes[cat]) < 4:
            quotes[cat].append({"media": media, "author": author, "score": score, "text": summary})

    # 키워드 빈도 (요약/리뷰 텍스트 코퍼스)
    corpus = []
    for r in ROWS:
        corpus.append(r[6])
    for r in SUMMARY_ROWS:
        corpus.append(r.get("요약", ""))
    text = " ".join(corpus)
    kw = {k: len(re.findall(re.escape(k), text)) for k in KEYWORDS}
    kw = dict(sorted(kw.items(), key=lambda x: -x[1]))

    # 매체 집계표 (정규화 0~100)
    media_agg = [
        {"media": "로튼토마토", "label": "Tomatometer", "score": "100%", "norm": 100, "n": "37 Reviews", "type": "평론가"},
        {"media": "메타크리틱", "label": "Metascore", "score": "93/100", "norm": 93, "n": "19 Critics", "type": "평론가"},
        {"media": "씨네21", "label": "전문가 별점", "score": "8.13/10", "norm": 81.3, "n": "8명", "type": "전문가"},
        {"media": "씨네21", "label": "관객 별점", "score": "9.13/10", "norm": 91.3, "n": "관객", "type": "일반 관객"},
        {"media": "키노라이츠", "label": "리뷰 평점", "score": "4.3/5", "norm": 86.0, "n": "107건", "type": "일반 관객"},
        {"media": "왓챠피디아", "label": "평균 별점", "score": "4.0/5", "norm": 80.0, "n": "68명", "type": "일반 관객"},
        {"media": "IMDb", "label": "IMDb Rating", "score": "8.2/10", "norm": 82.0, "n": "323 ratings", "type": "일반 관객"},
    ]

    data = {
        "movie": {
            "title": "가능한 사랑",
            "titleEn": "Possible Love",
            "director": "이창동",
            "runtime": "164분",
            "rating": "청소년 관람불가 (19+)",
            "release": "2026.09.23 (극장)",
            "netflix": "2026.11.06 (넷플릭스)",
            "cast": ["전도연", "설경구", "조인성", "조여정"],
            "award": "제83회 베네치아국제영화제 심사위원대상(은사자상) — 한국 영화 최초",
            "awardEn": "Silver Lion · Venice 2026",
        },
        "collection": {
            "total": len(ROWS),
            "media": len(by_media),
            "byCat": dict(by_cat),
            "byMedia": dict(by_media),
        },
        "mediaAgg": media_agg,
        "dist": dist,
        "sentiment": dict(sentiment),
        "keywords": list(kw.items()),
        "quotes": quotes,
        "expert": [{"media": m, "label": l, "score": s, "n": c} for m, l, s, c, _, _ in EXPERT_ROWS],
    }
    return data


if __name__ == "__main__":
    out = os.path.join(HERE, "data.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(analyze(), f, ensure_ascii=False, indent=2)
    print("saved", out)
