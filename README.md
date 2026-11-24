# web-app-design-guide

RDBMS 기반 웹 애플리케이션의 스키마·서버 코드·API 설계 규칙을 Claude Code 스킬로 만든 것. 원문은 [웹 애플리케이션 설계 가이드](https://mysticism.dev/posts/web-app-design-guide)다.

## 설치

```bash
git clone https://github.com/gidul0491/web-app-design-guide.git ~/git/web-app-design-guide
~/git/web-app-design-guide/install.sh
```

`~/.claude/skills/web-app-design-guide` 에 `skill` 폴더가 링크된다. 새 대화부터 Claude Code 가 테이블 설계, 서버 계층, API 규약, 테스트, 외부 연동 명세서를 다룰 때 이 스킬을 읽는다.

## 구성

- `skill/SKILL.md`: 스킬 본문. 언제 어느 장을 읽을지와 절·항 번호로 근거를 대는 법
- `skill/guide/`: 원문을 머리말과 1~8장으로 나눈 파일. 필요한 장만 읽어 한 번에 읽는 양을 줄인다

## 원문을 고쳤을 때

```bash
~/git/web-app-design-guide/sync-from-blog.sh
```

블로그 글을 받아 `skill/guide/` 를 새로 만들고 바뀐 파일을 보여 준다. [pandoc](https://pandoc.org) 이 필요하다. 장이 늘거나 장 제목이 바뀌면 `tools/split-guide.py` 의 파일 이름 표와 `skill/SKILL.md` 의 장 목록도 고친다.
