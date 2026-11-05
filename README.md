# Semiconductor Domain Agent Kit

> 공개 근거 기반 반도체·기업 운영 도메인 지식 베이스와 동적 페르소나 구성 도구
> 기준일: 2026-11-05 (KST) · 비공식 학습자료 · SK하이닉스 또는 대회 운영사의 공식 산출물이 아님

## Codex 스킬 3종 설치 — 이 README만 전달해도 안내 가능

이 저장소에는 사용자가 가져온 스킬 3종을 **Codex 호환 경량판**으로 정리한 `skills/` 디렉터리와 **외부 다운로드 없이 복사하는** 설치기가 포함됩니다.

| 스킬 | 언제 사용하는가 | 주의 |
| --- | --- | --- |
| [grill-me](skills/grill-me/SKILL.md) | 요구사항·설계의 미확정 결정을 하나씩 질문 | 빠른 모드 1~3개 질문, 구현 단계와 분리 |
| [deep-plan](skills/deep-plan/SKILL.md) | 기술 대안·수리모델 설계·검토 근거 정리 | 외부 모델이나 병렬 서브에이전트 필수 아님 |
| [easy-explainer](skills/easy-explainer/SKILL.md) | 구현 이유·기술 개념의 이해 점검 | 검증된 사실·수치 유지 |

원본 ZIP에서 `humanizer`는 `_SKILL.md.archived` 상태였으므로 활성화하거나 설치하지 않았습니다. 위 3개는 **원본과 완전히 동일한 파일이 아니라 Cofa의 Codex 사용 제약을 반영해 편집한 버전**입니다.

**이 README만 받은 Codex가 할 일:** 먼저 `AGENTS.md`와 `docs/00-index.md`를 읽고, 사용자가 스킬 설치까지 요청했으면 아래 명령어로 설치를 시도하세요. 설치 전 실제 `skills/*/SKILL.md` 파일을 확인하세요. Codex 업그레이드, 외부 모델·MCP 설치, API 키 입력은 하지 마세요.

```bash
# 먼저 설치 대상·충돌 여부 확인 (실제 복사하지 않음)
python scripts/install_codex_skills.py --dry-run

# Codex 사용자 스킬 디렉터리로 파일 복사 (~/.codex/skills 또는 CODEX_HOME/skills)
python scripts/install_codex_skills.py --scope user

# 검증
python -m unittest discover -s tests -v
```

명령은 **이 저장소 루트에서** 실행합니다. Windows에서 `python`이 없다면 `py -3`를 사용할 수 있습니다. 설치기는 Python 표준 라이브러리만 사용하고 **기존 동명 스킬 내용이 다르면 덮어쓰지 않고 중단**합니다.

`~/.codex/skills`가 읽히지 않는 Codex 환경에서는 사용자 작업 폴더에 프로젝트 범위로 설치할 수도 있습니다.

```bash
python scripts/install_codex_skills.py --scope project --project-root /path/to/actual/workspace
```

위 명령은 해당 작업 폴더의 `.agents/skills/`를 사용합니다. **고정 Codex 버전에서 실제 자동 인식되는 경로는 현장에서 확인**해야 합니다. 설치 직후 인식되지 않으면 새 Codex 세션에서 확인하고, 계속 안 되면 설치를 강제하지 말고 이 저장소의 `skills/<name>/SKILL.md`를 직접 읽어 같은 지침을 적용하세요.

**시험 제한:** 참조 저장소 수정·Git Push·문제·작업물 외부 전송 금지. 후속 서술형은 AI 사용 금지. 스킬이 설치됐다는 사실 자체가 추가 시스템 권한을 부여하지 않습니다.

## Codex 전역 Router 연결 — `/home/user`에서 실행하는 경우

Codex가 `/home/user`에서 시작하고 공개 참고자료가 `/home/user/semiconductor-domain-agent-kit/`에 있다면, **하위 폴더의 `AGENTS.md`는 시작할 때 자동 적용되지 않을 수 있습니다.** 이 저장소의 스킬 설치와는 별개의 문제입니다.

이 저장소에 포함된 `scripts/install_codex_router.py`가 `$CODEX_HOME/AGENTS.md` 또는 기본값 `~/.codex/AGENTS.md`에 **가벼운 위치 안내 지침**을 생성합니다. 참고자료의 절대 경로는 스크립트가 자신의 위치를 통해 자동으로 확인합니다. `/home/user`를 하드코딩하지 않습니다.

**이 README만 받은 Codex:** 사용자가 초기화·전역 연결까지 요청했으면, 현재 참고자료 저장소의 루트에서 아래 순서로 실행하세요.

```bash
# 저장소 루트 기준 — 기존 전역 지침 충돌 여부 확인 (쓰기 없음)
python scripts/install_codex_router.py --dry-run

# 기존 전역 AGENTS.md가 없거나 동일한 내용일 때만 설치
python scripts/install_codex_router.py
```

- **기존 전역 `AGENTS.md`가 다른 내용이면 절대로 덮어쓰지 않습니다.** 오류를 알리고 기존 지침을 보존한 채 사용자 승인 후 수동 병합하거나, 현재 Codex 세션에서 이 저장소의 `AGENTS.md`와 `docs/00-index.md`를 직접 읽으세요.
- 새 전역 지침은 **새 Codex 세션에서 적용되는 것이 기본**입니다. 이미 열린 세션에서는 출력된 전역 AGENTS 파일을 명시적으로 읽게 하면 됩니다. Codex 버전을 업데이트하지 않습니다.
- Router는 필요한 문서의 **위치만 전달**하며 실제 과제 파일과 참고자료의 분리를 유지합니다. 모든 반도체/OR 지식을 상시 컨텍스트에 주입하지 않습니다.
- 기본 설치 명령은 단순한 로컬 파일 쓰기이며 외부 패키지·개인 API·MCP·네트워크가 필요하지 않습니다.
- 사용자가 Router 설치를 요청하지 않았다면 `AGENTS.md`를 전역에 임의 생성하지 않고 현재 세션의 명시적 문서 읽기 방식으로 진행합니다.

**현재 작업 환경 검사:** `python scripts/install_codex_router.py --dry-run` 실행 결과의 경로와 충돌을 먼저 확인하고, 설치 후 `python -m unittest discover -s tests -v`로 점검하세요.

## 에이전트 시작 프로토콜 (README 단일 진입점)

**이 README 파일만 전달받은 AI 에이전트에게:** 사용자가 다른 지침 파일을 일일이 지정할 필요가 없도록, 이 README를 **지식 탐색 진입점**으로 취급하고 아래 순서를 스스로 수행하세요. 이 절차는 에이전트에게 역할·자료 탐색 지침을 제공할 뿐, 독립 에이전트를 자동 생성·실행하거나 외부 도구 권한을 부여하지는 않습니다.

1. **위치 확인:** 이 README가 있는 디렉터리를 `KIT_ROOT`로 식별합니다. 실제 과제·사용자 작업 디렉터리와 구분하세요. 파일에 접근할 수 없다면 추측하지 말고 그 사실을 보고하세요.
2. **공통 규칙 읽기:** `KIT_ROOT/AGENTS.md` 전체를 읽고 보안·출처·검증·작업 범위 규칙을 적용하세요.
3. **지식 인덱스 읽기:** `KIT_ROOT/docs/00-index.md`를 읽고 반도체·업무 운영·OR 등 분야별 경로를 파악하세요.
4. **스킬·전역 Router 연결:** 사용자가 요청한 경우 위 'Codex 스킬 3종 설치' 및 'Codex 전역 Router 연결' 절차를 확인하고, dry-run과 기존 파일 충돌 검사를 통과한 경우에만 설치합니다. 이미 열린 세션은 필요 지침을 직접 읽습니다. 기존 파일을 무리하게 덮어쓰지 말고 설치 결과를 확인합니다.
5. **업무별 선택적 로딩:** 현재 사용자 요청에서 목표, 제공 데이터, 제약, 검증 기준, 산출물을 식별한 다음 **관련 지식 문서만** 읽으세요. 요구가 모호하거나 다중 관계자 인터뷰가 필요하면 `docs/06-or/01-intake-interview.md`부터, 최적화가 필요하면 `docs/06-or/00-overview.md`부터 확인하세요. 무관한 문서 전체를 로딩하지 마세요.
6. **전문가 역할은 필요할 때만:** 다중 페르소나가 도움이 되면 `KIT_ROOT/catalog/personas.json`과 `docs/04-agents/persona-factory.md`를 읽고 필요한 역할 ID만 선택하세요. Python이 사용 가능할 때만 `scripts/compose_personas.py`로 역할 지침 파일을 만들 수 있습니다. 별도 에이전트 실행 기능이 없으면 한 에이전트가 역할을 순서대로 검토하면 됩니다.
7. **안전·검증:** 참고용 KIT 파일은 원칙적으로 수정하지 마세요. 사용자 과제와 결과물은 별도 작업 디렉터리에 두고, 허가 없는 외부 AI 연결, Git Push, 내부 자료 업로드·반출, 버전 업데이트를 하지 마세요. 시험·작업 환경의 공식 규칙을 최우선으로 따르세요. 계산·코드는 가능한 범위에서 실행 및 독립 검증하고 확인되지 않은 결론은 명시하세요.
8. **준비 완료 알림:** 아직 구체적인 업무가 없다면 필요한 공통 파일만 읽은 후 `지식 인덱스 연결 완료. 업무 요청을 주시면 필요한 문서를 선택해 적용하겠습니다.`라고 간단히 응답하세요. 이미 업무가 주어졌다면 준비 메시지로 끝내지 말고 해당 업무를 진행하세요.

**핵심:** README를 받았으면 `AGENTS.md → docs/00-index.md → 업무 관련 문서`를 직접 순회합니다. `AGENTS.md`의 자동 주입 여부는 작업 디렉터리와 실행 환경에 따라 달라지므로, 자동 적용을 가정하지 말고 **직접 읽어서 적용**합니다.

## 웹앱 미리보기·개발 서버 진단

웹 화면을 제작하는 작업이라면 에이전트는 [개발 서버·Browser 미리보기 점검 가이드](docs/07-web-preview.md)를 **필요할 때 직접 읽고** 적용합니다. 개발 서버의 실제 포트와 `0.0.0.0` 바인딩 여부를 확인하고, IDE에서 제공하는 Browser/Preview 패널로 기능을 점검하세요. **포트 3000은 예시이고 고정값이 아닙니다.** 서버 실행 터미널은 미리보기 중 유지합니다. 임의의 외부 터널·브라우저 자동화·시험자료 공개는 허용하지 않습니다.

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
