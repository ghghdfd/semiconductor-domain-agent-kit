# 운영과학(Operations Research) 확장 가이드

기준일: 2026-11-05 KST. 기존 반도체 도메인 문서는 변경 없이 유지한다.

## 이 섹션의 목적

다양한 업무에서 자연어 요구를 **목표·결정변수·데이터·제약조건·검증 가능한 해**로 변환한다. OR(수리최적화) 도구는 필요한 상황에만 사용한다. 모든 AI 에이전트 구축 문제가 OR은 아니다.

- **요구사항이 숨겨졌을 때:** [01-intake-interview.md](01-intake-interview.md)로 증거와 확인 질문 정리
- **모델로 표현할 때:** [02-modeling.md](02-modeling.md)로 집합·변수·제약·목적함수 명시
- **솔버를 선택할 때:** [03-solver-selection.md](03-solver-selection.md)로 문제 구조·설치 여부 확인
- **실제 결과를 확인할 때:** [04-verification.md](04-verification.md)로 독립 제약검사·최적성 상태 확인
- **복수 역할 분담할 때:** [05-agent-workflow.md](05-agent-workflow.md)로 역할·공유 증거 기록
- **연습 문제:** [06-synthetic-cases.md](06-synthetic-cases.md)
- **공개 대회 방식과의 비교:** [07-competition-evidence.md](07-competition-evidence.md)

## 5단계 문제해결 파이프라인

요구사항 확보 → 수리 모델 사양 확정 → 알고리즘/솔버 적용 → 독립 검증 → 의사결정 설명.

각 단계에서 **확인된 정보/잠정 가정/미확인 질문**을 구분한다. '더 많은 에이전트'는 목표가 아니라 필요 지식을 빠짐없이 확인하기 위한 수단이다.

## OR이 맞는지 결정

| 업무 질문 | 적합한 접근 |
| --- | --- |
| '예산과 조건 내에서 무엇을 얼마나 배정할까?' | LP, MILP, CP-SAT 등 고려 |
| '작업자를 시간표에 어떻게 넣을까?' | CP-SAT 또는 정수계획 |
| '차량을 어느 경로로 운행할까?' | VRP·시간창 모델 |
| '문서의 정책을 찾아 답변할까?' | 검색·규칙 검증·RAG 등 (OR 필수 아님) |
| '관계자 요구를 아직 모른다' | 인터뷰·증거 수집 먼저 |
| '정답을 설명하는 교육자료를 만들어라' | 도메인 검색과 구성, OR은 선택적 |

## 반드시 구분할 개념

- **Feasible(실행 가능):** 모든 강제 제약을 지킨 해. '최적'이라는 뜻이 아니다.
- **Optimal(최적성 입증):** 정의된 모델·허용오차에서 최적성이 입증된 해.
- **Infeasible:** 제약을 동시에 만족하는 해가 없다고 입증된 경우.
- **Unknown/시간 초과:** 문제에 해가 없다는 뜻이 아니다. 솔버의 종료 상태 확인.
- **모델의 정답과 업무의 정답:** 수리모델이 잘못됐으면 Solver가 정확히 최적화해도 업무에는 틀린 답이 된다.

## 공식 원문
- [Google OR-Tools 개요](https://developers.google.com/optimization/introduction)
- [Google 제약조건 최적화](https://developers.google.com/optimization/cp)
- [Google CP-SAT 종료 상태](https://developers.google.com/optimization/cp/cp_solver)