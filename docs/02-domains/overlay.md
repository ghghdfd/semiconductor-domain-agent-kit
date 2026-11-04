# 도메인: 포토 Overlay·장비 상태·계측 품질

**페르소나 유형:** 포토 기술 엔지니어, 장비 데이터 분석가, 계측·공정 품질 담당자.

## 한 문장 설명

Overlay는 **칩의 서로 다른 층(layer)이 웨이퍼 상에서 얼마나 정확하게 겹치는지**를 보는 위치 정렬 성능이다. ASML은 Overlay와 Focus를 노광 품질의 핵심 계측 파라미터로 설명한다.

## 함께 쓰이는 용어
| 용어 | 무엇을 뜻하나 |
| --- | --- |
| Overlay X/Y | 층 사이의 X·Y 방향 위치 오차 |
| CD(Critical Dimension) | 패턴의 중요 선폭/치수; Overlay와 다른 지표 |
| Focus | 노광 상의 초점 품질 |
| Wafer map | 웨이퍼 위치에 따라 측정값을 시각화한 것 |
| Scanner | 노광 장비. 장비/레시피별로 구분 분석 |
| Metrology | 측정·계측 활동. 측정기 편향과 반복성 확인 필요 |
| Control chart | 정상 공정 변동과 이상 신호를 분리하는 관리도 |
| Excursion | 공정 이상 상태를 나타내는 범주적 표현; 내부 정의 필요 |

## 분석 순서
1. 목표 확인: 사양 초과의 원인 파악인지, 장비별 차이 분석인지, 품질 추세 예측인지 구별.
2. 데이터 검증: timestamp, lot_id, wafer_id, exposure_tool, layer, site_x, site_y, overlay_x, overlay_y, unit, measurement_tool.
3. 측정단위(nm 등), 결측·중복·위치 좌표계, 동일 레시피/동일 제품 여부 확인.
4. 시계열·웨이퍼 위치·층별·장비별 분포 비교. 장비/Layer 믹스 혼동 주의.
5. 이상 탐지: 제공된 기준의 초과 여부 + 통계 관리도. 규격 한계와 관리 한계는 절대 혼용하지 않는다.
6. 가설 생성: 장비 이동/정렬, 웨이퍼 패턴, 계측기 상태, 후속 공정 영향 등 **가능성**만 분리.
7. 가설 검증: 대조군과 시간 순서, 계측 재현성, 변경 이력 확인.
8. 권고: 추가 측정, 장비 상태 점검, 재현시험, 사람 검토. 임의 레시피 변경 제안 금지.

## 예시 계산(개념)
- 방향별 평균 오차: mean(x), mean(y).
- 벡터 오차 크기: sqrt(x² + y²). 이 값은 별도 정의된 관리지표의 대용으로 자동 사용하지 않는다.
- 표준편차와 사분위 분포: 장비/제품/층·측정 위치가 동질적인 집단에서 해석.
- 경보: 실제 제공된 spec/관리기준 없이는 임의의 '합격/불합격' 임계값을 설정하지 않는다.

## 예상 오개념
- Overlay와 CD는 둘 다 '선폭 오차'가 아님.
- 평균이 0에 가까워도 분산과 국소적 이상이 클 수 있다.
- 장비 A의 평균이 더 낮아도 제품 믹스/층이 다르면 우열을 단정할 수 없다.
- 상관계수가 높다고 장비 결함의 근본 원인이 확정되지는 않는다.
- 모니터링 모델은 근거 없이 자동 장비 변경을 수행해서는 안 된다.

## 결과물 형식
장비·기간별 통계표 / wafer-map 개요 / 이상 후보 / 원인 가설의 근거·반증 / 추가 데이터 요청 / 권고조치 순서.

## 출처
- [ASML Measuring Accuracy](https://www.asml.com/en/technology/lithography-principles/measuring-accuracy) (공식)
- [ASML Lithography Principles](https://www.asml.com/en/technology/lithography-principles)
- [NIST Lithography Process: 관리도 사례](https://www.itl.nist.gov/div898/handbook/pmc/section6/pmc61.htm)
- [NIST Process Control](https://www.itl.nist.gov/div898/handbook/pmc/section1/pmc13.htm)