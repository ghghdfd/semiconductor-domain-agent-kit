#!/usr/bin/env python3
"""요구사항 모델 계약의 필수 필드 점검. 수리적 타당성 자체는 판단하지 않는다."""
import argparse
import json
from pathlib import Path

FIELDS = {
    "schema_version": str,
    "title": str,
    "purpose": str,
    "source_type": str,
    "decision_variables": list,
    "input_data": list,
    "hard_constraints": list,
    "soft_preferences": list,
    "objective": dict,
    "acceptance_tests": list,
    "open_questions": list,
    "assumptions": list,
}


def check(data: dict) -> list[str]:
    errors = []
    if not isinstance(data, dict):
        return ["최상위 구조는 JSON 객체여야 합니다."]
    for key, typ in FIELDS.items():
        if key not in data or not isinstance(data[key], typ):
            errors.append(f"{key}: {typ.__name__} 타입의 필수 필드")
    if isinstance(data.get("decision_variables"), list) and not data["decision_variables"]:
        errors.append("decision_variables: 비어 있을 수 없음")
    if isinstance(data.get("acceptance_tests"), list) and not data["acceptance_tests"]:
        errors.append("acceptance_tests: 비어 있을 수 없음")
    if isinstance(data.get("objective"), dict):
        obj = data["objective"]
        if obj.get("sense") not in ("minimize", "maximize", "feasibility"):
            errors.append("objective.sense: minimize / maximize / feasibility 중 선택")
        if not isinstance(obj.get("metric"), str) or not obj["metric"].strip():
            errors.append("objective.metric: 비어 있지 않은 문자열")
    return errors


def main():
    ap = argparse.ArgumentParser(description="OR 요구사항 모델 계약 검증")
    ap.add_argument("path", type=Path)
    args = ap.parse_args()
    try:
        data = json.loads(args.path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as ex:
        ap.error(str(ex))
    errors = check(data)
    if errors:
        print("CONTRACT_INVALID")
        for e in errors:
            print(" -", e)
        raise SystemExit(1)
    print("CONTRACT_VALID (형식만 통과; 수학·업무 타당성은 별도 검증 필요)")


if __name__ == "__main__":
    main()