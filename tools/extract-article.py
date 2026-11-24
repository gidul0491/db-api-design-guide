"""블로그 글 HTML 에서 본문(article)만 꺼낸다. 머리글(제목·날짜), 댓글 입력, 코드 복사 버튼은 뺀다.
    python3 tools/extract-article.py <글 HTML> <본문 HTML>
"""
import pathlib
import re
import sys

post_html = pathlib.Path(sys.argv[1]).read_text()
article_html = re.search(r'<article.*?</article>', post_html, flags=re.S).group(0)
for removed_part in [r'<header.*?</header>', r'<form.*?</form>', r'<button.*?</button>']:
    article_html = re.sub(removed_part, '', article_html, flags=re.S)
pathlib.Path(sys.argv[2]).write_text(article_html)
