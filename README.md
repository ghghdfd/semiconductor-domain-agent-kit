# Semiconductor Domain Agent Kit

> 공개 근거 기반 반도체·기업 운영 도메인 지식 베이스와 동적 페르소나 구성 도구
> 기준일: 2026-11-05 (KST) · 비공식 학습자료 · SK하이닉스 또는 대회 운영사의 공식 산출물이 아님

## 무엇을 할 수 있나

- 메모리 제품, 반도체 제조, 소재 품질, 시장전략, 밸류체인, 사내 운영 분야의 **섹션별 Markdown 문서** 조회
- 주어진 업무에 맞는 전문 페르소나를 **0개가 아닌 원하는 n개만큼** 선택하거나 직접 추가
- **Codex/CLI**에서 프로젝트 지침(AGENTS.md)으로 지식 탐색·검증 규칙 적용
- 파이썬 표준 라이브러리만으로 선택한 페르소나의 개별 프롬프트 생성
- 출처·확인일·주장의 근거 수준을 분리하여 환각과 과도한 단정을 줄임

## 빠른 시작

~~~bash
git clone --depth 1 https://github.com/ghghdfd/semiconductor-domain-agent-kit.git
cd semiconductor-domain-agent-kit
python scripts/compose_personas.py --list
python scripts/compose_personas.py --roles memory-market,photo-overlay --out generated_agents
python -m unittest discover -s tests -v
~~~

Codex CLI를 사용할 수 있는 환경이라면 **저장소 루트에서** codex를 실행하세요. 루트의 AGENTS.md는 자동으로 읽힐 수 있지만 지식 문서 전체가 자동으로 컨텍스트에 들어가는 것은 아닙니다. 에이전트에게 해당 문서를 읽도록 지시하세요.

~~~bash
command -v codex || echo "Codex CLI 없음"
codex --version
codex
~~~

시험·사내 보안 정책이 우선입니다. 인터넷·외부 Git 저장소 접근, 패키지 설치, 외부 AI 호출 또는 파일 반출이 허용되는지는 **해당 실행 환경의 최신 공식 규칙**으로 확인해야 합니다. 본 저장소는 공개 자료만 포함하며 비공개 대회 과제, 내부 사이트 스크립트 또는 문제 풀이를 포함하지 않습니다.

## 문서 지도

| 경로 | 담당 영역 |
| --- | --- |
| docs/00-index.md | 업무와 문서 사이의 빠른 라우팅 |
| docs/01-foundations/ | DRAM/HBM/NAND, 전공정, 밸류체인 |
| docs/02-domains/ | 시장, 소재, Overlay, 교육, 통근, 식단, 안전 |
| docs/03-workflows/ | 수치·근거·결정·검증 프레임워크 |
| docs/04-agents/ | 페르소나 설계 원칙, 모델 독립적 실행 가이드 |
| docs/05-sources/ | 원문 출처, 주장·출처 매핑 및 갱신 정책 |
| catalog/personas.json | 기본 역할 카탈로그 |
| scripts/compose_personas.py | n개 페르소나 프롬프트 생성 |
| examples/custom-personas.json | 사용자 정의 역할 추가 예시 |

## 어떤 일을 시킬 때

1. 업무 요구사항에서 **목표 / 입력 데이터 / 제약 / 검증 기준 / 제출물**을 추출합니다.
2. docs/00-index.md를 참고해 관련 문서를 찾습니다.
3. catalog/personas.json에서 필요한 역할만 고르거나, 새 역할을 JSON으로 정의합니다.
4. scripts/compose_personas.py로 역할별 지침을 생성합니다.
5. 실제 제공된 데이터만 가지고 분석·구현하며, 가설과 사실을 엄격히 구분합니다.
6. 제출 전 데이터·품질 검증과 설명서 작성 시간을 확보합니다.

## 주의

- 설명된 업무 역할은 **일반화한 예시**이며 공식 채점기준·실제 문제·시험 페르소나가 아닙니다.
- 근거가 부족한 수치는 만들지 않습니다. 2026-11-05 이후의 최신 실적·규정은 새로 확인하세요.
- 외부 문서의 원문·표·도면을 복제하지 않고, 짧은 자체 설명과 출처 링크만 담았습니다.
- 코드·문서의 원본 작성 부분은 LICENSE의 MIT 조건을 적용합니다. 링크된 제3자 문서의 권리는 원저작자에게 있습니다.

## 새 기능: 업무 최적화 및 대화형 AI 에이전트 (2026-11-05)
반도체 섹션은 유지하면서 [OR 확장 문서](docs/06-or/00-overview.md)를 추가했습니다. 업무가 최적화 문제인지 먼저 확인하고, 관계자 인터뷰 → 요구 명세 → 결정변수·목적함수·제약조건 → Solver → 독립 검증 순서로 해결합니다.

```bash
python scripts/check_or_contract.py examples/or/model-contract.json
python scripts/solve_assignment.py examples/or/assignment.json
python scripts/compose_personas.py --roles or-interviewer,or-modeler,or-solver,or-verifier --out generated_agents
python -m unittest discover -s tests -v
```

**표준 라이브러리 예제는 소형 합성 배정(완전탐색) 전용**입니다. 대규모 실무에서는 CP-SAT/LP/MILP/VRP 등 환경에 맞는 솔버를 사용하세요. 현재 기본 예제에는 외부 패키지 설치가 필요하지 않습니다. 본 자료에는 실제 평가문항이나 비공개 데이터가 없습니다.
