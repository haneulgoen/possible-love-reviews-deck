#!/usr/bin/env python3
"""평론가 / 전문가(집계평점) / 일반 관객 3분류를 하나의 CSV로 정리한다."""
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build_rating_review_csv import ROWS  # noqa: E402
from split_reviews_by_type import CRITIC, AUDIENCE, EXPERT_ROWS  # noqa: E402

OUT = os.path.join(HERE, "possible_love_ratings", "가능한_사랑_평점리뷰_3분류.csv")
FIELDS = ["분류", "매체", "작성자", "평점", "집계리뷰수", "리뷰요약", "URL"]
ORDER = ["평론가", "전문가", "일반 관객"]


def classify(media, kind):
    if (media, kind) in CRITIC:
        return "평론가"
    if (media, kind) in AUDIENCE:
        return "일반 관객"
    return "기타"


def main():
    rows = []
    # 평론가 / 일반 관객 (개별 리뷰)
    for media, agg, n, kind, author, score, summary, url in ROWS:
        cls = classify(media, kind)
        rows.append([cls, media, author, score, "", summary, url])
    # 전문가 (집계 평점)
    for media, metric, score, count, note, url in EXPERT_ROWS:
        rows.append(["전문가", media, metric, score, count, note, url])

    rows.sort(key=lambda r: (ORDER.index(r[0]), r[1], r[2]))

    with open(OUT, "w", encoding="utf-8-sig", newline="") as fp:
        w = csv.writer(fp)
        w.writerow(FIELDS)
        w.writerows(rows)

    counts = {c: sum(1 for r in rows if r[0] == c) for c in ORDER}
    print(f"총 {len(rows)}행 -> {OUT}")
    for c in ORDER:
        print(f"  {c}: {counts[c]}행")


if __name__ == "__main__":
    main()
