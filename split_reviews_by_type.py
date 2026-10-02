#!/usr/bin/env python3
"""가능한 사랑 평점+리뷰를 평론가 / 전문가(집계평점) / 일반 관객으로 분류해 CSV로 저장한다."""
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build_rating_review_csv import ROWS  # noqa: E402

OUT = os.path.join(HERE, "possible_love_ratings")

# (매체, 구분) -> 분류
CRITIC = {
    ("로튼토마토", "평론가 리뷰"),
    ("메타크리틱", "평론가 리뷰"),
    ("씨네21", "전문가 별점"),
}
AUDIENCE = {
    ("왓챠피디아", "사용자 코멘트"),
    ("키노라이츠", "사용자 리뷰"),
    ("Letterboxd", "사용자 리뷰"),
    ("IMDb", "사용자 리뷰"),
    ("씨네21", "관객 별점"),
}


def classify(row):
    key = (row[0], row[3])
    if key in CRITIC:
        return "평론가"
    if key in AUDIENCE:
        return "일반 관객"
    return "기타"


# 전문가(집계 평점)
EXPERT_ROWS = [
    ("씨네21", "전문가 별점", "8.13/10", "8명 참여", "국내 영화 전문가(평론가) 집계 평점", "https://cine21.com/movie/info/?movie_id=63333"),
    ("로튼토마토", "Tomatometer", "100%", "37 Reviews", "신선도 지수(평론가 긍정 비율), 팝콘지수(관객)는 아직 미집계", "https://www.rottentomatoes.com/m/possible_love"),
    ("메타크리틱", "Metascore", "93/100", "19 Critic Reviews", "Universal Acclaim(100% Positive)", "https://www.metacritic.com/movie/possible-love/"),
    ("IMDb", "Metascore(표기)", "93/100", "—", "IMDb 페이지에 표기된 메타스코어", "https://www.imdb.com/title/tt37803364/"),
    ("키노라이츠", "로튼토마토 지수(표기)", "100%", "—", "키노라이츠 상세 페이지 표기", "https://m.kinolights.com/season/144328"),
]

REVIEW_FIELDS = ["분류", "매체", "작성자", "평점", "리뷰요약", "URL"]
EXPERT_FIELDS = ["매체", "지표", "평점", "집계리뷰수", "비고", "URL"]


def write(path, fields, rows):
    with open(path, "w", encoding="utf-8-sig", newline="") as fp:
        w = csv.writer(fp)
        w.writerow(fields)
        w.writerows(rows)
    print(f"  {os.path.basename(path):<28} {len(rows):>3}행")


def main():
    critics, audience = [], []
    for r in ROWS:
        media, _agg, _n, _kind, author, score, summary, url = r
        cls = classify(r)
        out = [cls, media, author, score, summary, url]
        (critics if cls == "평론가" else audience).append(out)

    print("저장 완료:")
    write(os.path.join(OUT, "평점리뷰_평론가.csv"), REVIEW_FIELDS, critics)
    write(os.path.join(OUT, "평점리뷰_일반관객.csv"), REVIEW_FIELDS, audience)
    write(os.path.join(OUT, "평점리뷰_전문가_집계평점.csv"), EXPERT_FIELDS, EXPERT_ROWS)

    combined = []
    for r in ROWS:
        cls = classify(r)
        combined.append([cls] + list(r[:1]) + list(r[4:8]))
    combined.sort(key=lambda x: (["평론가", "전문가", "일반 관객"].index(x[0]), x[1]))
    write(os.path.join(OUT, "가능한_사랑_평점리뷰_분류.csv"),
          ["분류", "매체", "작성자", "평점", "리뷰요약", "URL"], combined)


if __name__ == "__main__":
    main()
