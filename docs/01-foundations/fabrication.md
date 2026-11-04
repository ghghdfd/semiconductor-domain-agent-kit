# 반도체 제조공정과 품질: 큰 그림

## 핵심 흐름

반도체 생산은 단방향 직선이 아니라 **박막 형성·포토·식각·세정·계측 등이 여러 차례 반복**되는 복합 공정이다.

| 단계 | 목적 | 품질 관점 |
| --- | --- | --- |
| 웨이퍼·산화 | 기반 및 절연막 형성 | 두께·균일성·결함 |
| 증착(CVD/PVD 등) | 절연막·도전막 등 박막 형성 | 막 두께, 균일도, 단차 피복 |
| 포토(Lithography) | 회로 패턴 위치와 형태 정의 | CD(선폭), Overlay, Focus |
| 식각(Etch) | 선택되지 않은 부분 제거·패턴 전사 | 식각 깊이, 선택비, 잔류물 |
| 이온주입/열처리 | 불순물 도핑과 활성화 | 프로파일, 균일도 |
| 세정(Clean) | 입자·잔류 화학물 제거 | 오염도, 결함, 손상 |
| CMP | 표면 평탄화 | 평탄도, 스크래치, 두께 |
| 계측/검사 | 상태 측정 및 이상 검출 | 측정 신뢰성, 샘플링 |
| 후공정 | 다이 분리·패키징·시험 | 연결 품질, 신뢰성, 불량률 |

## 수율/불량 분석

- **수율**은 정의된 검사/집계 단계에서 양품 비율이다. 웨이퍼 수율·다이 수율·최종테스트 수율은 서로 다르다.
- **Lot**은 생산 추적 단위다. 장비, 레시피, 시간, 자재 배치에 따라 계층화 분석한다.
- **SPC**는 측정값이 공정이 안정된 상태에서 예상되는 변동 범위를 벗어나는지 추적한다. 관리한계는 규격 상한/하한과 다르다.
- 상관이 있다고 즉시 장비 원인이라고 결론내리지 않는다. 제품·레시피·기간·샘플링 조건 등을 통제한다.
- 데이터가 없는 실제 공정의 레시피·관리한계·경보 임계치는 만들지 않는다.

## 기본 데이터 컬럼 예

timestamp, wafer_id, lot_id, tool_id, chamber_id, process_step, recipe_id, measurement_name, value, unit, spec_lower, spec_upper, sampling_flag, inspection_status

위는 실습용 **예시 스키마**이지 특정 사업장의 실제 테이블 구조가 아니다.

## 공개 원문
- [SK하이닉스 전공정 6부작](https://news.skhynix.com/en/series/frond-end-process/) (2022–2023)
- [SK하이닉스 세정·CMP 설명](https://news.skhynix.com/en/creating-defectless-wafers-a-look-at-clean-cmp-technology/) (2022)
- [ASML 반도체 제조 여섯 단계](https://www.asml.com/en/company/stories/2021/semiconductor-manufacturing-process-steps)
- [NIST 공정관리 핸드북](https://www.itl.nist.gov/div898/handbook/pmc/pmc.htm)