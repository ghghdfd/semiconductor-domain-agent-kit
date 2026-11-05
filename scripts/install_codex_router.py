#!/usr/bin/env python3
"""현재 저장소의 지식 인덱스를 Codex 전역 AGENTS.md에 안전하게 연결한다.

외부 패키지, 네트워크, 모델 및 Codex 버전 변경이 필요하지 않다.
기존 전역 AGENTS.md는 덮어쓰지 않는다.
"""

import argparse
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def codex_home():
    configured = os.environ.get("CODEX_HOME")
    path = Path(configured).expanduser() if configured else Path.home() / ".codex"
    if not path.is_absolute():
        raise ValueError("CODEX_HOME은 절대 경로여야 합니다.")
    return path


def render_router(repo_root):
    root = Path(repo_root).resolve()
    for name in ("README.md", "AGENTS.md", "docs/00-index.md"):
        if not (root / name).is_file():
            raise ValueError("참고자료 파일이 없습니다: " + str(root / name))
    return f"""# Codex Workspace Router

이 파일은 공개 참고자료의 경로만 알려주는 전역 연결 지침입니다.

- 현재 작업 디렉터리와 실제 프로젝트의 README 및 AGENTS.md를 우선 확인합니다.
- 공개 참고자료 위치: `{root}` (읽기 전용으로 취급).
- 현재 업무가 관련될 때만 `{root / 'AGENTS.md'}`와 `{root / 'docs/00-index.md'}`를 직접 읽습니다.
- 인덱스를 바탕으로 필요한 문서만 선택해 읽고, 모든 문서를 한 번에 로딩하지 않습니다.
- 해당 저장소가 없거나 접근 불가능하면 추측하지 않고 사용자에게 알립니다.
- 실제 구현·테스트·제출 파일은 현재 작업 프로젝트에 보관합니다.
- 참고자료 저장소는 임의로 수정하지 않고, 설치된 스킬은 필요할 때만 사용합니다.
- 환경의 보안·응시 규정과 실제 프로젝트의 지침이 최우선입니다.
- 허가 없는 Git Push, 외부 AI 연결, 파일 반출, 모델·Codex 업데이트를 하지 않습니다.
- 수행 결과는 실행 테스트와 근거를 확인한 후 보고합니다.
"""


def install_router(repo_root, target, dry_run=False):
    target = Path(target)
    content = render_router(repo_root)
    if target.is_symlink():
        raise FileExistsError("심볼릭 링크 대상은 변경하지 않습니다: " + str(target))
    if target.exists():
        if not target.is_file():
            raise FileExistsError("기존 경로가 파일이 아닙니다: " + str(target))
        if target.read_text(encoding="utf-8") == content:
            return "ALREADY_INSTALLED"
        raise FileExistsError(
            "다른 전역 AGENTS.md가 이미 존재하므로 변경하지 않았습니다: "
            + str(target)
            + " (내용을 확인하고 수동 병합하거나 현재 세션에서 지침을 직접 읽으세요.)"
        )
    if not dry_run:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    return "DRY_RUN" if dry_run else "INSTALLED"


def main():
    parser = argparse.ArgumentParser(description="Codex 전역 AGENTS.md에 참고자료 연결 지침 설치")
    parser.add_argument("--dry-run", action="store_true", help="쓰기 없이 경로·충돌 여부만 확인")
    args = parser.parse_args()
    try:
        target = codex_home() / "AGENTS.md"
        status = install_router(ROOT, target, dry_run=args.dry_run)
    except (ValueError, FileExistsError, OSError) as exc:
        parser.error(str(exc))
    print("상태:", status)
    print("전역 지침:", target)
    print("참고자료:", ROOT)
    if status == "INSTALLED":
        print("이미 열린 Codex 세션에는 자동 재주입되지 않을 수 있습니다.")
        print("새 세션에서 적용 여부를 확인하거나 현재 세션에 이 AGENTS.md를 직접 읽히세요.")


if __name__ == "__main__":
    main()
