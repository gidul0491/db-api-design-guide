#!/usr/bin/env bash
# 블로그 원문을 다시 받아 skill/guide/ 를 새로 만든다. pandoc 이 필요하다.
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
POST_URL="https://mysticism.dev/posts/web-app-design-guide"
WORK_DIR="$(mktemp -d)"
trap 'rm -rf "$WORK_DIR"' EXIT

curl -fsSL "$POST_URL" -o "$WORK_DIR/post.html"
python3 "$REPO_DIR/tools/extract-article.py" "$WORK_DIR/post.html" "$WORK_DIR/article.html"
pandoc -f html -t gfm --wrap=none "$WORK_DIR/article.html" -o "$WORK_DIR/article.md"
rm -rf "$REPO_DIR/skill/guide"
python3 "$REPO_DIR/tools/split-guide.py" "$WORK_DIR/article.md" "$REPO_DIR/skill/guide"
git -C "$REPO_DIR" status --short skill/guide
