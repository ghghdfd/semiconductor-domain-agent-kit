# Persona Factory — n개 전문가 역할의 재사용 가능한 구성

## 개념

**페르소나**는 '모델의 새로운 지식'이 아니다. 주어진 작업에서 무엇을 검토하고 어떤 산출물을 작성할지 정하는 **역할 지침**이다. 필요한 공개 지식 파일을 실제로 읽지 않으면 단순 역할 설정만으로 정확도가 높아지지 않는다.

- catalog/personas.json: 미리 정의한 전문 분야
- examples/custom-personas.json: 작업별 추가 역할 예제
- scripts/compose_personas.py: 선택한 ID들의 Markdown 역할 지침을 생성
- AGENTS.md: 전체 작업에 공통으로 적용할 핵심 원칙
- docs/00-index.md: 실제 업무 주제에 따라 필요한 문서를 찾는 지도

## 'n개'의 정확한 의미

n은 고정값이 아니다. JSON에 정의된 역할을 직접 지정한 만큼 n개 생성한다. 신규 역할 추가도 제한하지 않는다. 단, 역할별 지침 파일이 n개 생기는 것이지 n개의 **독립적으로 실행 중인 AI 프로세스**가 생기는 것은 아니다. 도구의 멀티에이전트 기능이 없다면 하나의 Codex에게 순차 검토를 시킬 수 있다.

## 생성기

~~~bash
python scripts/compose_personas.py --list
python scripts/compose_personas.py --roles memory-market,materials-quality,photo-overlay --out generated_agents
python scripts/compose_personas.py --roles custom-sustainability --catalog examples/custom-personas.json --out generated_agents
~~~

기본 모드는 **단일 입력 카탈로그**다. 복수 카탈로그 병합 기능은 제공하지 않는다. 필요하다면 사용자가 두 JSON의 roles 항목을 직접 하나로 통합한다. --out 경로를 생략하면 표준 출력으로 합쳐 출력한다.

## 생성되는 프롬프트의 공통 내용

1. **당신의 역할**: 필요한 전문 관점을 제공하지만 독점적인 전문 지식이나 권한이 있는 것으로 가장하지 않는다.
2. **현재 업무**: 목표, 데이터, 제한조건, 성공 기준 확인.
3. **사용할 지식 파일**: 존재하는 파일만 읽고 출처를 확인한다.
4. **산출물/검증**: 역할별 분석 항목, 검증조건, 불확실성과 반례를 기록한다.
5. **주의**: 자료에 없는 기업 내부 데이터·출제 정보·합격 기준·임계치를 만들지 않는다.

## 실행 패턴

**패턴 A — 단일 Codex, 순차 역할 검토(호환성 높음):**

~~~text
이 저장소의 AGENTS.md와 docs/00-index.md를 읽어라.
요청: [업무 설명]
선택할 역할: memory-market,materials-quality
해당 역할의 지식 문서를 읽고 역할별 검토를 순서대로 수행하라.
마지막에 충돌하는 판단을 설명하고 검증된 결론만 통합하라.
~~~

**패턴 B — 외부 멀티에이전트 실행기가 있을 때:** 생성된 Markdown을 각각의 에이전트 system/developer instruction에 연결하고, 결과를 별도의 종합 단계에서 다시 검증한다. 이 저장소는 외부 실행기의 API 호출이나 오케스트레이션을 포함하지 않는다.

## 결합 예시

- 시장: memory-market + value-chain-strategy + evidence-reviewer
- 공정: photo-overlay + process-yield + evidence-reviewer
- 소재: materials-quality + value-chain-strategy + evidence-reviewer
- 종합: 다른 역할 2~3개 + evidence-reviewer

## 복잡도 관리

역할은 필요할 때만 추가한다. 전 영역을 한 번에 읽히는 것보다 문서 2~3개로 관련성을 유지하는 편이 비용·컨텍스트·검증에 유리할 수 있다. '검토자' 역할도 독립된 사실 확인을 보장하지 않는다.

## 모델·Cofa 관련 주의

이 저장소는 어떤 GPT/Codex 모델 버전도 하드코딩하지 않는다. 실제 실행 환경에서 `codex --version`, `codex --help`로 사용 가능한 인터페이스와 제한을 확인한다. 별도 사용 권한이 없는 네트워크/외부 API/민감 파일 접근은 실행하지 않는다. 사용자 말로 외부 공개 Git 활용이 허용되더라도 **이 저장소를 내려받는 행위**와 **외부 모델 호출·데이터 업로드**는 서로 다른 정책 적용 대상일 수 있다.