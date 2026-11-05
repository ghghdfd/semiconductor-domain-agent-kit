# 도메인 인덱스: 목적별 문서 라우팅

**범위:** 공개 반도체 지식 + 일반 사내 운영 도메인. 개인·조직 고유의 비공개 업무 규칙이나 대회 문제를 포함하지 않는다.

## 분야별 문서

| 업무 신호 | 우선 파일 | 확인할 쟁점 |
| --- | --- | --- |
| DRAM, HBM, NAND, DDR5, SSD | 01-foundations/memory.md | 휘발성·인터페이스·대역폭·용량 |
| 포토, 증착, 식각, 세정, CMP, 수율 | 01-foundations/fabrication.md | 공정 단계·결함·계측·인과성 |
| 산업, IDM, Fabless, Foundry, OSAT | 01-foundations/value-chain.md | 공급망상의 역할과 의존도 |
| ASP, 매출, 영업이익률, 경쟁사 | 02-domains/market.md | 지표 정의·기간·환율·믹스 |
| 소재, 공급사, 변경심사, Lot | 02-domains/supplier-quality.md | 승인조건·품질 위험·추적성 |
| Overlay, 레이어 정렬, 포토장비 | 02-domains/overlay.md | 오차벡터·장비편차·SPC |
| 교육, 온보딩, 커리큘럼 | 02-domains/training.md | 대상수준·학습목표·오개념 |
| 통근버스, 배차, 교대시간 | 02-domains/commute.md | 수요·용량·시간창·공정성 |
| 식단, 영양, 알레르기, 원가 | 02-domains/cafeteria.md | 급식 안전·다양성·영양·제약 |
| 카메라, 사각지대, 프라이버시 | 02-domains/safety.md | 안전목적·위험도·접근권한 |
| 다영역 문제 해결 | 03-workflows/decision-playbook.md | 사실·가정·분석·검증 |
| 다중 역할 생성 | 04-agents/persona-factory.md | 역할 분담·증거공유·합성 |
| 웹앱 실행·Browser 미리보기·포트 오류 | 07-web-preview.md | 서버 실행·바인딩·실제 포트·경로·검증 |
| 공식 근거 추적 | 05-sources/registry.md | URL·날짜·검증 수준 |

## 사용 예시

- 'HBM 경쟁사 실적 비교': memory + market + decision-playbook
- '공급사 전환 검토': supplier-quality + fabrication + decision-playbook
- '특정 장비에서 Overlay 증가': overlay + fabrication + decision-playbook
- '이천 통근버스 노선 개선': commute + decision-playbook
- '식단 추천의 공정성과 알레르기 고려': cafeteria + safety(개인정보 부분만)

## 원칙

요청자가 제공한 데이터·규칙을 우선 읽되, 검증되지 않은 '조직 내부의 사실'로 일반화하지 않는다. 지역·사업장·장비별 임계값은 본 저장소에 없다. 실제 값이 없다면 필요한 데이터를 먼저 제시한다.

## 운영과학(OR)·대화형 문제해결 확장 (2026-11-05)
- 관계자 인터뷰·요구사항 수집: [06-or/01-intake-interview.md](06-or/01-intake-interview.md)
- 수리모델 정형화: [06-or/02-modeling.md](06-or/02-modeling.md)
- Solver 선택: [06-or/03-solver-selection.md](06-or/03-solver-selection.md)
- 독립 검증: [06-or/04-verification.md](06-or/04-verification.md)
- 에이전트 협업: [06-or/05-agent-workflow.md](06-or/05-agent-workflow.md)
- 합성 예제: [06-or/06-synthetic-cases.md](06-or/06-synthetic-cases.md)
- 2026 대회 공개 근거: [06-or/07-competition-evidence.md](06-or/07-competition-evidence.md)

**라우팅 기준:** 업무 요구가 모호하면 인터뷰 문서부터, 자원·일정·경로 선택이면 모델링/솔버 문서부터, 단순 정보 검색이면 OR을 억지로 적용하지 않는다.
