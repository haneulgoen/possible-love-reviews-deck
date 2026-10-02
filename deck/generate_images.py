#!/usr/bin/env python3
"""Nano Banana(Gemini 이미지 모델)로 슬라이드 이미지 에셋을 생성한다.

사용:
  GEMINI_API_KEY=... .venv/bin/python deck/generate_images.py [--force]

키가 없으면 아무것도 하지 않고 안내만 출력한다(폴백 SVG가 이미 배포되어 있음).
"""
import base64
import json
import os
import sys
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "docs", "assets")
os.makedirs(OUT, exist_ok=True)

MODELS = [
    "gemini-2.5-flash-image",
    "gemini-2.5-flash-image-preview",
    "gemini-2.0-flash-preview-image-generation",
]

PROMPTS = {
    "hero": (
        "Cinematic wide shot of a huge full moon over a dark calm sea at night, two tiny distant "
        "human silhouettes standing on the shore facing the water, muted teal and amber palette, "
        "social-realist Korean art film poster mood, heavy atmosphere, film grain, deep shadows. "
        "No text, no words, no letters, no watermark."
    ),
    "theme-class": (
        "Abstract conceptual image of a class divide: left half is a warm dim working-class interior "
        "with worn hands and old tools, right half is cold minimalist luxury with glass and steel, "
        "a hard vertical seam of light between them, cinematic, moody, no faces, no text, no letters."
    ),
    "theme-camera": (
        "Dramatic close-up of a documentary film camera lens emerging from shadows, one side lit warm "
        "amber, the other cold blue, metaphor of a voyeuristic gaze, cinematic shallow depth of field, "
        "no text, no words, no letters."
    ),
    "theme-moon": (
        "A full moon rising over a quiet Korean coastal village at night, soft reflection on wet ground, "
        "faint warm window lights, hopeful yet melancholic, painterly cinematic style, no text, no letters."
    ),
}


def load_key():
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if key:
        return key
    env = os.path.join(ROOT, ".env")
    if os.path.exists(env):
        for line in open(env, encoding="utf-8"):
            if line.startswith(("GEMINI_API_KEY=", "GOOGLE_API_KEY=")):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


def generate(key, model, prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseModalities": ["IMAGE"]},
    }
    req = urllib.request.Request(
        url, data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        data = json.load(resp)
    for cand in data.get("candidates", []):
        for part in cand.get("content", {}).get("parts", []):
            inline = part.get("inlineData") or part.get("inline_data")
            if inline and inline.get("data"):
                return base64.b64decode(inline["data"])
    raise RuntimeError(f"no image in response: {json.dumps(data)[:300]}")


def main():
    force = "--force" in sys.argv
    key = load_key()
    if not key:
        print("GEMINI_API_KEY가 없습니다. .env에 추가하거나 환경변수로 전달하세요.")
        print("폴백 SVG가 이미 docs/assets에 있으므로 배포는 정상 동작합니다.")
        return 1

    ok, fail = 0, 0
    for name, prompt in PROMPTS.items():
        target = os.path.join(OUT, f"{name}.png")
        if os.path.exists(target) and not force:
            print(f"skip {name} (exists)")
            continue
        last = None
        for model in MODELS:
            try:
                png = generate(key, model, prompt)
                open(target, "wb").write(png)
                print(f"ok   {name}.png  ({len(png):,} bytes, {model})")
                ok += 1
                break
            except urllib.error.HTTPError as e:
                last = f"{e.code} {e.read()[:160]}"
            except Exception as e:  # noqa: BLE001
                last = str(e)
        else:
            print(f"FAIL {name}: {last}")
            fail += 1
    print(f"\n완료: 성공 {ok}, 실패 {fail}")
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
