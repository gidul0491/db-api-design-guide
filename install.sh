#!/usr/bin/env bash
# Claude Code 가 이 스킬을 찾도록 ~/.claude/skills/web-app-design-guide 에 skill 폴더를 링크한다.
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_LINK="$HOME/.claude/skills/web-app-design-guide"

mkdir -p "$(dirname "$SKILL_LINK")"
if [ -e "$SKILL_LINK" ] && [ ! -L "$SKILL_LINK" ]; then
  echo "$SKILL_LINK 에 링크가 아닌 폴더가 있습니다. 확인 후 지우고 다시 실행하세요." >&2
  exit 1
fi
ln -sfn "$REPO_DIR/skill" "$SKILL_LINK"
echo "스킬 링크: $SKILL_LINK → $REPO_DIR/skill"
