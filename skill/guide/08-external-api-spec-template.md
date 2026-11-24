# 8장. 외부 연동 명세서 양식

밖으로 나가는 규격은 손으로 쓴 문서가 필요합니다. 6-3-6의 코드 생성은 우리 프론트가 쓰는 내부 API 얘기입니다. 아래를 복사해 채웁니다. 값은 예시입니다.

## 8-1 개정 이력

| 버전 | 일자       | 변경 내용                          | 작성자 |
|------|------------|------------------------------------|--------|
| 1.1  | 2026-09-06 | contracts\[\].status 에 ENDED 추가 | 홍길동 |
| 1.0  | 2026-08-20 | 최초 배포                          | 홍길동 |

## 8-2 접근 정보

| 항목          | 값                                               |
|---------------|--------------------------------------------------|
| 운영 주소     | <https://api.example.com>                        |
| 테스트 주소   | <https://api-test.example.com>                   |
| 인증 방식     | 헤더 x-api-key                                   |
| 자격증명 전달 | 담당자 메일로 개별 발급                          |
| 호출 제한     | 분당 60회, 초과 시 429                           |
| Content-Type  | application/json; charset=utf-8                  |
| 시각 표기     | ISO 8601 오프셋 포함 — 2026-09-06T14:22:10+09:00 |
| 오류 응답     | application/problem+json (RFC 9457)              |
| 담당자        | 홍길동 · <hong@example.com>                      |

## 8-3 암복호화

| 항목 | 값 |
|----|----|
| 알고리즘 | AES-256 |
| 모드 | GCM |
| 패딩 | 해당 없음. CBC·ECB 등 블록 모드일 때만 적는다 (예: PKCS#7) |
| 초기화 벡터 | 12바이트 난수, 매 건 새로 뽑아 값 안에 포함 |
| 인증 태그 | 128비트, 암호문 뒤에 이어 붙여 마지막 조각에 함께 담는다 (GCM일 때) |
| 추가 인증 데이터 | 사용하지 않음 |
| 값 형식 | {알고리즘}.{모드}.{키}.{IV}.{암호문} |
| 키 이름 | pii-k1. 교체 시 사전 통보 후 양쪽 병행 기간을 둔다 |
| 인코딩 | base64url, 패딩(=) 제거 |
| 키 | 32바이트, Base64로 전달 |
| 대상 필드 | employee.socialNumber · employee.phone. 하이픈·공백을 지운 값을 암호화한다 |
| 키 전달 | 별도 경로로 전달. 이 문서에 적지 않음 |

## 8-4 공통 응답 형태

성공 여부는 HTTP 상태 코드가 알립니다. 본문에 따로 표시하지 않습니다.
```
성공 — 200 · 201
{ "receiptNo": "R2026-000481", "employeeId": 3391,
  "receivedAt": "2026-09-06T14:22:10+09:00" }

목록 — 200
{ "data": [ … ],
  "pagination": { "page": 1, "size": 20, "total": 137 } }

실패 — 4xx · 5xx        Content-Type: application/problem+json
{ "type": "https://api.example.com/problems/employee-not-found",
  "title": "직원을 찾을 수 없음",
  "status": 404,
  "detail": "직원 번호 3391 에 해당하는 직원이 없습니다",
  "instance": "/api/external/employees/3391/cancel",
  "code": "EMPLOYEE_NOT_FOUND" }
```
## 8-5 공통 에러 코드

| HTTP | code | title | 발생 조건 |
|----|----|----|----|
| 400 | INVALID_PARAMETER | 요청 값이 올바르지 않음 | 필수 누락, 형식 오류 |
| 401 | API_KEY_MISSING | 인증 정보가 없습니다 | 헤더 누락 |
| 401 | INVALID_API_KEY | 인증 정보가 올바르지 않습니다 | 키 불일치·만료 |
| 403 | FORBIDDEN | 권한이 없습니다 | 다른 회사의 자원 |
| 404 | NOT_FOUND | 대상을 찾을 수 없습니다 | 존재하지 않는 식별자 |
| 409 | DUPLICATED | 이미 처리된 요청입니다 | 중복 접수 |
| 429 | RATE_LIMITED | 호출이 너무 잦습니다 | 호출 제한 초과 |
| 500 | INTERNAL_SERVER_ERROR | 처리 중 오류가 발생했습니다 | 그 밖의 실패 |

## 8-6 API 목차

| 번호 | 이름           | 메서드 | 경로                                        |
|------|----------------|--------|---------------------------------------------|
| 1    | 직원 등록      | POST   | /api/external/employees                     |
| 2    | 직원 목록 조회 | GET    | /api/external/employees                     |
| 3    | 직원 등록 해지 | POST   | /api/external/employees/{employeeId}/cancel |

## 8-7 API 상세

### 1. 직원 등록

| 항목 | 값 |
|----|----|
| 메서드 | POST |
| 경로 | /api/external/employees |
| 설명 | 직원을 등록하고 접수 번호를 돌려줍니다. 접수 시점에 검증은 하지 않으며, 결과는 2번에 receiptNo 를 조건으로 넣어 조회합니다 |

### 요청

| 필드명 | 타입 | 길이 | 필수 | 예시 | 설명 |
|----|----|----|----|----|----|
| companyId | number | \- | Y | 12 | 회사 번호 |
| employee | object | \- | Y |  | 직원 정보 |
| employee.name | string | 20 | Y | 홍길동 | 직원 이름 |
| employee.phone | string | 200 | Y | aes256.gcm.… | 암호화 대상. 하이픈을 지운 뒤 암호화한다 |
| employee.socialNumber | string | 200 | Y | aes256.gcm.… | 암호화 대상. 하이픈을 지운 뒤 암호화한다 |
| employee.birthday | string | 10 | Y | 1990-01-01 | YYYY-MM-DD |
| contracts | array | \- | N |  | 계약 목록. 없으면 빈 배열 |
| contracts\[\].no | string | 20 | Y | C2026-0001 | 계약 번호 |
| contracts\[\].startAt | string | 25 | Y | 2026-09-06T00:00:00+09:00 | 계약 시작. 시작일 포함 |
| contracts\[\].status | string | 20 | Y | ACTIVE | ACTIVE · ENDED |
| memo | string | 500 | N |  | 비고 |
```
{
  "companyId": 12,
  "employee": {
    "name": "홍길동",
    "phone": "aes256.gcm.pii-k1.7AOkv9uITst8dabB.60jHw3PJo6bKEO7GppfPSBuCmfsXlD3AhEq5",
    "socialNumber": "aes256.gcm.pii-k1.8tlH7J3tYj6ukBOl.Lq5-BJ_Ih1y5BxryVeVfKomDLADzXnKZ0FHm_tM",
    "birthday": "1990-01-01"
  },
  "contracts": [
    { "no": "C2026-0001", "startAt": "2026-09-06T00:00:00+09:00", "status": "ACTIVE" }
  ]
}
```
### 응답

| 필드명 | 타입 | 길이 | 필수 | 예시 | 설명 |
|----|----|----|----|----|----|
| receiptNo | string | 20 | Y | R2026-000481 | 접수 번호. 2번 조회의 receiptNo 조건에 쓴다 |
| employeeId | number | \- | Y | 3391 | 직원 번호 |
| receivedAt | string | 25 | Y | 2026-09-06T14:22:10+09:00 | 접수 시각 |
```
201 Created
{
  "receiptNo": "R2026-000481",
  "employeeId": 3391,
  "receivedAt": "2026-09-06T14:22:10+09:00"
}
```
```
409 Conflict        Content-Type: application/problem+json
{
  "type": "https://api.example.com/problems/duplicated-employee",
  "title": "이미 등록된 직원",
  "status": 409,
  "detail": "같은 회사에 같은 주민등록번호가 이미 등록되어 있습니다",
  "instance": "/api/external/employees",
  "code": "DUPLICATED_EMPLOYEE"
}
```
### 에러 코드

| HTTP | 코드                  | 발생 조건                                   |
|------|-----------------------|---------------------------------------------|
| 409  | DUPLICATED_EMPLOYEE   | 같은 회사에 같은 주민등록번호가 이미 등록됨 |
| 422  | CONTRACT_DATE_INVALID | startAt 이 오늘보다 이전                    |
| 422  | AGE_NOT_ALLOWED       | 나이가 고용 가능 기준을 벗어남              |

> **참고** — 필드명은 중첩을 `parent.child`, 배열 안을 `list[].item`으로 적습니다. 들여쓰기로 표현하면 복사해 붙일 때 깨지고 검색으로 필드를 찾을 수 없습니다. 길이는 문자열에만 적고, 숫자는 범위를, 날짜·시각은 형식을 설명 칸에 적습니다. 값이 정해진 필드는 가능한 값 전체를 적습니다. 필수 여부가 다른 필드에 따라 갈리면 `Y`·`N` 대신 조건을 설명 칸에 적습니다.
