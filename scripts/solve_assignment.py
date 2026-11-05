#!/usr/bin/env python3
"""작은 규모의 합성 배정문제. 표준라이브러리 완전탐색 + 독립 제약검사."""
import argparse
import itertools
import json
from pathlib import Path


def validate_input(data):
    workers, tasks = data["workers"], data["tasks"]
    costs = data["costs"]
    if not workers or not tasks or len(workers) < len(tasks):
        raise ValueError("유효한 작업자/업무 수가 아닙니다.")
    if len(set(workers)) != len(workers) or len(set(tasks)) != len(tasks):
        raise ValueError("중복 ID")
    if len(workers) > 9:
        raise ValueError("완전탐색 예제는 작업자 9명 이하로 제한합니다.")
    if len(costs) != len(workers) or any(len(row) != len(tasks) for row in costs):
        raise ValueError("비용행렬 크기 불일치")
    if any(type(c) not in (int, float) or c < 0 or c != c for row in costs for c in row):
        raise ValueError("비용은 0 이상의 유한한 숫자여야 합니다.")
    forbidden = {tuple(x) for x in data.get("forbidden", [])}
    if any(w not in workers or t not in tasks for w, t in forbidden):
        raise ValueError("알 수 없는 금지 배정 조합")
    return forbidden


def verify(data, assignment, claimed_cost):
    """독립적으로 모든 작업의 배정·작업자 중복·금지 조합·비용을 확인."""
    workers, tasks, costs = data["workers"], data["tasks"], data["costs"]
    forbidden = {tuple(x) for x in data.get("forbidden", [])}
    if len(assignment) != len(tasks):
        return False
    if set(assignment) != set(tasks) or len(set(assignment.values())) != len(tasks):
        return False
    if any(w not in workers or (w, t) in forbidden for t, w in assignment.items()):
        return False
    measured = sum(costs[workers.index(w)][tasks.index(t)] for t, w in assignment.items())
    return abs(measured - claimed_cost) <= 1e-8


def solve(data):
    forbidden = validate_input(data)
    workers, tasks, costs = data["workers"], data["tasks"], data["costs"]
    best = None
    for ordered_workers in itertools.permutations(workers, len(tasks)):
        assignment = dict(zip(tasks, ordered_workers))
        if any((w, t) in forbidden for t, w in assignment.items()):
            continue
        total = sum(costs[workers.index(w)][i] for i, w in enumerate(ordered_workers))
        if best is None or total < best["cost"]:
            best = {"cost": total, "assignment": assignment}
    if best is None:
        return {"status": "INFEASIBLE", "reason": "작은 합성 모델의 전수 탐색에서 실행 가능 해 없음"}
    if not verify(data, best["assignment"], best["cost"]):
        raise RuntimeError("독립 검증 실패")
    return {"status": "OPTIMAL", "objective": "minimize total cost", **best, "verified": True}


def main():
    ap = argparse.ArgumentParser(description="표준라이브러리로 가상 배정 문제를 완전탐색")
    ap.add_argument("path", type=Path)
    args = ap.parse_args()
    try:
        data = json.loads(args.path.read_text(encoding="utf-8"))
        output = solve(data)
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as ex:
        ap.error(str(ex))
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()