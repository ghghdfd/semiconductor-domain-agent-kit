#!/usr/bin/env python3
"""저장소에 포함된 Codex 스킬을 설치한다. 외부 패키지·네트워크·Codex 업데이트 없음."""
import argparse
import os
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AVAILABLE = ("grill-me", "deep-plan", "easy-explainer")


def skill_path(name):
    if name not in AVAILABLE:
        raise ValueError("알 수 없는 스킬: " + name)
    path = ROOT / "skills" / name
    file = path / "SKILL.md"
    if not file.is_file() or file.is_symlink():
        raise ValueError("SKILL.md 없음: " + name)
    raw = file.read_text(encoding="utf-8")
    sections = raw.split("---", 2)
    if len(sections) < 3 or not raw.startswith("---"):
        raise ValueError("frontmatter 누락: " + name)
    if not re.search(r"(?m)^name:\s*" + re.escape(name) + r"\s*$", sections[1]):
        raise ValueError("frontmatter 이름 불일치: " + name)
    if not re.search(r"(?m)^description:", sections[1]):
        raise ValueError("frontmatter 설명 누락: " + name)
    if any(entry.is_symlink() for entry in path.rglob("*")):
        raise ValueError("심볼릭 링크를 포함한 스킬은 설치하지 않음: " + name)
    return path


def get_target(scope, project_root):
    if scope == "user":
        return Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))) / "skills"
    if scope == "project":
        return Path(project_root or Path.cwd()).resolve() / ".agents" / "skills"
    raise ValueError("지원되지 않는 scope")


def install(names, target, dry_run=False):
    added, identical = [], []
    for name in names:
        src = skill_path(name)
        dest = target / name
        if dest.exists() or dest.is_symlink():
            if not dest.is_dir() or dest.is_symlink():
                raise ValueError("기존 경로와 충돌: " + str(dest))
            src_files = {p.relative_to(src) for p in src.rglob("*") if p.is_file()}
            dst_files = {p.relative_to(dest) for p in dest.rglob("*") if p.is_file()}
            if src_files != dst_files or any((src / p).read_bytes() != (dest / p).read_bytes() for p in src_files):
                raise ValueError("동명 스킬이 다른 내용이므로 덮어쓰지 않음: " + str(dest))
            identical.append(name)
            continue
        if not dry_run:
            target.mkdir(parents=True, exist_ok=True)
            shutil.copytree(src, dest)
        added.append(name)
    return added, identical


def main():
    parser = argparse.ArgumentParser(description="Codex 호환 스킬을 로컬에서 안전하게 복사 설치")
    parser.add_argument("--scope", choices=("user", "project"), default="user")
    parser.add_argument("--project-root", type=Path, help="project 범위의 실제 작업 디렉터리")
    parser.add_argument("--skills", default=",".join(AVAILABLE))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    names = [name.strip() for name in args.skills.split(",") if name.strip()]
    if not names or len(names) != len(set(names)):
        parser.error("중복 없는 스킬 ID 1개 이상 지정")
    target = get_target(args.scope, args.project_root)
    try:
        added, identical = install(names, target, dry_run=args.dry_run)
    except ValueError as exc:
        parser.error(str(exc))
    print("대상:", target)
    print("모드:", "DRY_RUN" if args.dry_run else "INSTALLED")
    print("추가:", ", ".join(added) or "없음")
    print("이미 동일하게 설치:", ", ".join(identical) or "없음")
    print("인식되지 않으면 새 Codex 세션을 시작하고, 필요시 SKILL.md를 직접 읽도록 지시하세요.")


if __name__ == "__main__":
    main()
