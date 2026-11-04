# AGENTS.md — Semiconductor Domain Agent Kit

한국어로 답하고, 요청 범위에 해당하는 파일만 읽는다. 이 저장소는 공식 SK하이닉스 정보시스템도 공식 대회 문제 은행도 아니다.

## 라우팅
- 메모리/제품/시장: docs/01-foundations/memory.md → docs/02-domains/market.md
- 제조/수율/Overlay: docs/01-foundations/fabrication.md → docs/02-domains/overlay.md
- 소재/공급사: docs/02-domains/supplier-quality.md
- 밸류체인/사업전략: docs/01-foundations/value-chain.md → docs/02-domains/market.md
- 교육/설명: docs/02-domains/training.md
- 통근/식단/CCTV: 각 운영 문서(docs/02-domains/)
- 사용자 업무가 복합적이면 docs/04-agents/persona-factory.md에서 필요한 역할 여러 개만 선택한다.

## 필수 행동
1. 업무 목표, 제공 데이터의 범위, 단위·기간·기준, 제한조건, 성공기준, 제출물을 먼저 추출한다.
2. 역할을 정할 때 역할명보다 **실제 업무 범위**를 먼저 판단한다. 요구받지 않은 페르소나를 늘리지 않는다.
3. 공개 자료에서 확인되는 일반 상식과 사용자 파일에서 검증할 사안, 추론을 반드시 구분한다.
4. 수치 계산의 분모·분자·단위·비교 시점, 결측·중복·이상치를 명시한다.
5. 원인·상관관계 혼동을 피하고 반례와 검증 한계를 제시한다.
6. 필요한 경우에만 docs/05-sources/registry.md의 출처를 참고한다. 불확실하면 미확인이라고 쓴다.
7. 명시적으로 허용된 도구·데이터만 사용한다. 작업물이나 응시 환경의 비공개 정보를 외부로 올리지 않는다.
8. 결과물을 검증하기 전 성공을 선언하지 않는다.

## 최종 산출물 기본 형식
- 요구사항 및 가정
- 수행한 작업과 사용한 데이터
- 핵심 결과와 검증 수치
- 의사결정의 이유·대안·리스크
- 남은 문제와 다음 확인사항

## 환경
- 특정 모델이나 에이전트 기능을 전제하지 않는다. Codex 존재 여부·버전·가용 모델·도구 사용 권한은 실행 시 확인한다.
- AGENTS.md만으로 전 문서를 자동 로딩하지 않는다. 필요 지식 파일을 명시적으로 읽는다.