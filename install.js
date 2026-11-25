#!/usr/bin/env node
// Claude Code 가 이 스킬을 찾도록 ~/.claude/skills/db-api-design-guide 에 skill 폴더를 링크한다 (macOS·리눅스·윈도우).
// 윈도우는 관리자 권한 없이 만들 수 있는 폴더 링크(junction)를 쓴다. Git Bash 의 ln -s 는 링크 대신 폴더를 복사한다.
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const SKILL_NAME = 'db-api-design-guide';
const skillFolder = path.join(__dirname, 'skill');
const skillLink = path.join(os.homedir(), '.claude', 'skills', SKILL_NAME);

fs.mkdirSync(path.dirname(skillLink), { recursive: true });
removeExistingSkillLink();
fs.symlinkSync(skillFolder, skillLink, process.platform === 'win32' ? 'junction' : 'dir');
console.log(`스킬 링크: ${skillLink} → ${skillFolder}`);

// 예전 링크나, 링크 대신 복사된 이 스킬 폴더만 지운다. 다른 폴더가 있으면 멈춘다
function removeExistingSkillLink() {
  const existingEntry = fs.lstatSync(skillLink, { throwIfNoEntry: false });
  if (!existingEntry) return;
  if (existingEntry.isSymbolicLink()) return fs.unlinkSync(skillLink);
  const copiedSkillFile = path.join(skillLink, 'SKILL.md');
  const isCopiedSkill = fs.existsSync(copiedSkillFile) && new RegExp(`^name: ${SKILL_NAME}$`, 'm').test(fs.readFileSync(copiedSkillFile, 'utf8'));
  if (!isCopiedSkill) {
    console.error(`${skillLink} 에 이 스킬이 아닌 폴더가 있습니다. 확인 후 지우고 다시 실행하세요.`);
    process.exit(1);
  }
  fs.rmSync(skillLink, { recursive: true, force: true });
}
