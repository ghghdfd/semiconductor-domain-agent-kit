# 문제 구조에 따른 Solver 선택

## 상황별 라우팅

| 문제 형태 | 대표 방법 | 흔한 함정 |
| --- | --- | --- |
| 연속량 + 선형 목적/제약 | LP (linprog, HiGHS) | 정수 단위가 필요한데 소수점 해 허용 |
| 0/1·정수량 + 선형 제약 | MILP (SciPy milp/HiGHS, OR-Tools MathOpt/MPSolver) | 단위와 빅-M, 목적부호 실수 |
| 스케줄·복잡한 논리·정수 제약 | CP-SAT (OR-Tools) | 실수값을 정수 스케일 없이 입력 |
| 여러 차량의 경로·용량·시간창 | VRP (OR-Tools Routing) | 이동시간 행렬·출발/복귀 조건 누락 |
| 소규모 순수 배정 | 완전탐색(검증용), Hungarian/정수계획 | 실제 규모에서 완전탐색 사용 |
| 데이터가 부족하거나 목적이 불명확 | 요구사항 재확인 | 'Solver 도입'이 목표 자체가 됨 |
| 대규모·시간 제한 엄격 | 휴리스틱·근사해 + 제약 검사 | 근사해를 최적해로 표시 |

OR-Tools CP-SAT는 **정수 기반**으로 모델링해야 한다. 복잡한 일정·인력 배치에 강점이 있으나, 부동소수점 제약을 그대로 입력하면 안 된다. SciPy `optimize.milp`는 HiGHS 기반의 혼합정수선형계획 모델을 제공한다.

## 실행 전 환경 확인

~~~bash
python --version
python -c "import importlib.util; print('ortools:', bool(importlib.util.find_spec('ortools'))); print('scipy:', bool(importlib.util.find_spec('scipy')))"
~~~

- **표준 라이브러리만 사용 가능:** 예제의 작은 모델로 문제 구조와 검증 로직을 시험한다. 완전탐색을 실제 대규모 데이터에 적용하지 않는다.
- **SciPy 사용 가능:** LP/MILP 형식으로 모델링 가능한지 확인.
- **OR-Tools 사용 가능:** CP-SAT·Routing·Assignment 예제를 검토.
- **패키지 설치가 금지되거나 네트워크 차단:** 허용된 내장 패키지와 의사코드·검증 가능한 간단한 해법만 선택; 허가 없이 설치하지 않는다.

모델 선택 전 데이터 크기, 제한시간, 사용 가능한 패키지, 해의 정확도/최적성 요구를 구분한다.

## 종료 상태를 혼동하지 말 것

| CP-SAT status | 뜻 |
| --- | --- |
| OPTIMAL | 설정된 모델의 최적해가 발견/입증됨 |
| FEASIBLE | 제약을 만족하는 해를 찾았지만 최적성은 미입증 |
| INFEASIBLE | 해당 모델이 불가능함을 입증 |
| MODEL_INVALID | 모델 명세/형식 오류 |
| UNKNOWN | 시간/메모리/기타 중단 등으로 결론 불명확 |

SciPy의 status 코드와 CP-SAT 상태 이름은 동일하지 않다. 라이브러리별 API를 기준으로 결과를 보고한다.

## 정확성과 가용성의 절충

- 제한시간 도달 시 `FEASIBLE`로 끝났다면 최적이 아닌 **잠정 실행 가능 해**라고 쓴다.
- 근사해도 강제 제약을 위반하면 업무상 유효하지 않다.
- 수치 오차가 있는 연속 최적화는 허용오차와 재평가 기준을 정한다.
- 최적성 격차(gap)는 제공될 때만 계산/표시한다.
- 목적함수 값이 좋더라도 **문제의 실제 성공 기준**에 부합하는지 별도 확인한다.

## 공개 원문
- [Google CP-SAT Solver](https://developers.google.com/optimization/cp/cp_solver)
- [Google Vehicle Routing](https://developers.google.com/optimization/routing/vrp)
- [Google Employee Scheduling](https://developers.google.com/optimization/scheduling/employee_scheduling)
- [SciPy MILP](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.milp.html)