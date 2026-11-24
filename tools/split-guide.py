"""블로그 글을 pandoc 으로 바꾼 마크다운을 받아, 머리말과 장마다 나눠 skill/guide/ 에 쓴다.
    python3 tools/split-guide.py <바꾼 마크다운> <guide 폴더>
"""
import pathlib
import re
import sys

converted_markdown_file, guide_folder = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
CHAPTER_FILE_NAMES = {
    '01': '01-source-of-truth.md',
    '02': '02-database-design.md',
    '03': '03-sensitive-data.md',
    '04': '04-code-structure.md',
    '05': '05-backend-layers.md',
    '06': '06-api-conventions.md',
    '07': '07-testing.md',
    '08': '08-external-api-spec-template.md',
}

markdown_text = converted_markdown_file.read_text()
markdown_text = markdown_text[:markdown_text.index('## 댓글')]
markdown_text = re.sub(r'^\s*</?div[^>]*>\s*$\n?', '', markdown_text, flags=re.M)
markdown_text = re.sub(r'^(\s*)``` shiki$', r'\1```', markdown_text, flags=re.M)
markdown_text = re.sub(r'\n{3,}', '\n\n', markdown_text)

chapter_starts = list(re.finditer(r'^## (0\d)\. (.+)$', markdown_text, flags=re.M))
introduction_text = markdown_text[:chapter_starts[0].start()].strip()
guide_folder.mkdir(parents=True, exist_ok=True)
(guide_folder / '00-introduction.md').write_text(f'# 웹 애플리케이션 설계 가이드\n\n{introduction_text}\n')
for chapter_index, chapter_start in enumerate(chapter_starts):
    chapter_end = chapter_starts[chapter_index + 1].start() if chapter_index + 1 < len(chapter_starts) else len(markdown_text)
    chapter_number, chapter_title = chapter_start.group(1), chapter_start.group(2)
    chapter_body = markdown_text[chapter_start.end():chapter_end].strip()
    chapter_body = re.sub(r'^###', '##', chapter_body, flags=re.M)
    (guide_folder / CHAPTER_FILE_NAMES[chapter_number]).write_text(f'# {int(chapter_number)}장. {chapter_title}\n\n{chapter_body}\n')
    print(CHAPTER_FILE_NAMES[chapter_number], len(chapter_body))
