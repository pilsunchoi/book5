"""빌드한 HTML에서 수식 코드가 글자로 남는 자리만 고친다.

절 제목에 수식($R^2$, $p$값, $\\alpha$ …)이 있으면 페이지 안에서는 MathJax가 그려 주지만,
수식을 그릴 수 없는 자리에는 코드가 글자 그대로 남는다:
  - <title>            브라우저 탭, 즐겨찾기, 방문 기록
  - <meta … content>   링크 미리보기의 제목과 설명(og:title, og:description, description)
  - <link … title>     앞·뒤 페이지 제목(rel="prev", rel="next")
  - 인쇄용 머리 제목     <div id="jb-print-docs-body"> 안의 <h1>
이 네 자리의 글자만 바꾸고, 본문과 스크립트는 건드리지 않는다. 바꿀 것을 찾지 못하면 그대로 둔다.

쓰는 법: python tools/fix_head_math.py _build/html
새 기호가 절 제목에 나오면 SYMBOLS에 더한다.
"""
import re
import sys
from pathlib import Path

BS = chr(92)

# 수식 안의 내용 → 글자
SYMBOLS = {
    "R^2": "R²",
    "p": "p",
    "t": "t",
    "n": "n",
    "F": "F",
    BS + "alpha": "α",
    BS + "theta": "θ",
}
# 수식 표시 없이 맨 코드로 남는 것(인쇄용 제목, 미리보기 설명)
BARE = {
    BS + "alpha": "α",
    BS + "theta": "θ",
    "R^2": "R²",
}

INLINE = re.compile(re.escape(BS + "(") + r"\s*(.+?)\s*" + re.escape(BS + ")"))


def plain(text):
    """수식 코드를 글자로. 표에 없는 수식은 괄호 표시만 뗀다."""
    text = INLINE.sub(lambda m: SYMBOLS.get(m.group(1), m.group(1)), text)
    for code, ch in BARE.items():
        # 미리보기 설명은 "크론바흐\alpha 는", "R^2 과"처럼 앞 낱말에 붙고 뒤에 빈칸이 생긴 꼴로 남는다
        text = re.sub(r"(?<=[가-힣])" + re.escape(code), " " + ch, text)   # 앞 낱말과 띄운다
        text = text.replace(code, ch)
        text = re.sub(re.escape(ch) + r" (?=[가-힣])", ch, text)            # 뒤 조사와 붙인다
    return text


TITLE = re.compile(r"(<title>)(.*?)(</title>)", re.S)
META = re.compile(r'(<meta\b[^>]*?\bcontent=")([^"]*)(")')
LINK = re.compile(r'(<link\b[^>]*?\btitle=")([^"]*)(")')
PRINT = re.compile(r'(<div id="jb-print-docs-body"[^>]*>\s*<h1>)(.*?)(</h1>)', re.S)


def fix(html):
    for rx in (TITLE, META, LINK, PRINT):
        html = rx.sub(lambda m: m.group(1) + plain(m.group(2)) + m.group(3), html)
    return html


def main(root):
    changed = 0
    for path in sorted(Path(root).rglob("*.html")):
        old = path.read_text(encoding="utf-8")
        new = fix(old)
        if new != old:
            path.write_text(new, encoding="utf-8", newline="")
            changed += 1
            print("fixed", path.relative_to(root))
    print(f"fix_head_math: {changed} page(s) changed")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "_build/html")
