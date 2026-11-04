#!/usr/bin/env python3
"""공개 도메인 지식에 기반한 역할 지침을 생성하는 표준 라이브러리 스크립트."""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CATALOG = ROOT / "catalog" / "personas.json"
ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")


def load_roles(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("roles"), list):
        raise ValueError("카탈로그에는 roles 배열이 있어야 합니다.")
    roles = {}
    for role in data["roles"]:
        if not isinstance(role, dict):
            raise ValueError("roles 원소는 객체여야 합니다.")
        key = role.get("id")
        if not isinstance(key, str) or not ID_PATTERN.fullmatch(key):
            raise ValueError(f"잘못된 역할 ID: {key!r}")
        if key in roles:
            raise ValueError(f"중복 역할 ID: {key}")
        for field in ("name", "purpose"):
            if not isinstance(role.get(field), str) or not role[field].strip():
                raise ValueError(f"{key}: 필수 필드 {field} 누락")
        for field in ("knowledge", "checks", "deliverables"):
            value = role.get(field)
            if not isinstance(value, list) or not all(isinstance(v, str) and v.strip() for v in value):
                raise ValueError(f"{key}: {field}는 비어있지 않은 문자열 배열이어야 합니다.")
        for doc in role["knowledge"]:
            if Path(doc).is_absolute() or ".." in Path(doc).parts or not (ROOT / doc).is_file():
                raise ValueError(f"{key}: 유효하지 않은 지식 파일 경로: {doc}")
        roles[key] = role
    return roles


def render(role: dict) -> str:
    docs = "\n".join(f"- [{p}](../{p})" for p in role["knowledge"])
    checks = "\n".join(f"- {v}" for v in role["checks"])
    deliverables = "\n".join(f"- {v}" for v in role["deliverables"])
    return f"""# {role['name']}

> ID: `{role['id']}` · 공개자료 기반 일반 업무 역할 (특정 회사 내부자 아님)

## 목표
{role['purpose']}

## 우선 읽을 파일
{docs}

## 작업 규칙
1. 루트 AGENTS.md와 대상 도메인 문서를 읽고 실제 입력 데이터와 제한조건을 확인한다.
2. 확인한 사실·합리적 추론·미확인 정보를 구분한다.
3. 필요한 분야 전문성을 제공하되 권한이 있는 내부 직원인 척하지 않는다.
4. 민감정보는 외부 서비스에 제출하거나 공개 저장소로 전송하지 않는다.
5. 임의의 품질 임계값·내부 정책·평가 점수·시험 문제를 만들어내지 않는다.

## 주요 검증 항목
{checks}

## 기대 산출물
{deliverables}

## 최종 검토
실행 가능한 결과와 그 근거, 실제 테스트, 데이터 누락, 반증 가능성을 함께 보고한다.
"""


def main() -> None:
    p = argparse.ArgumentParser(description="필요한 n개 역할의 Markdown 파일을 생성합니다.")
    p.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    p.add_argument("--roles", help="쉼표로 구분한 역할 ID. --all과 동시 사용 불가")
    p.add_argument("--all", action="store_true", help="카탈로그의 모든 역할 선택")
    p.add_argument("--list", action="store_true", help="사용 가능한 역할 목록")
    p.add_argument("--out", type=Path, help="생성할 출력 디렉터리")
    a = p.parse_args()
    roles = load_roles(a.catalog)
    if a.list:
        for key, value in roles.items():
            print(f"{key}: {value['name']}")
        return
    if bool(a.roles) == bool(a.all):
        p.error("--roles 또는 --all 중 하나만 지정하세요.")
    ids = list(roles) if a.all else [s.strip() for s in a.roles.split(",")]
    if len(ids) != len(set(ids)):
        p.error("중복 역할 ID를 제거하세요.")
    unknown = [key for key in ids if key not in roles]
    if unknown:
        p.error("알 수 없는 역할 ID: " + ", ".join(unknown))
    if not ids:
        p.error("최소 1개 역할을 지정하세요.")
    if a.out:
        a.out.mkdir(parents=True, exist_ok=True)
        for key in ids:
            dest = a.out / f"{key}.md"
            dest.write_text(render(roles[key]), encoding="utf-8")
            print(dest)
    else:
        for key in ids:
            print(render(roles[key]))


if __name__ == "__main__":
    main()