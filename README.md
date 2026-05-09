# Korea Stock App API (Backend)

## 1. Project Overview

`Korea Stock App API (Backend)`는 Python 기반의 경량 API 서버로, 한국 주식 데이터를 조회하고 클라이언트가 바로 사용할 수 있는 형태로 가공하여 제공합니다.

현재는 FastAPI 서버를 중심으로 최소 기능(MVP) 백엔드를 구성했으며, 삼성전자 단일 종목에 대해 실시간 시세와 등락률을 계산해 반환하는 API를 제공합니다.

## 2. Tech Stack

### Current

- `Python 3.13`
- `FastAPI`
- `yfinance`
- `Uvicorn`

### Planned

- `Supabase` (DB/캐싱 레이어)
- `Vercel Serverless Functions` (배포/서버리스 실행 환경)

## 3. Features

### 현재 구현

- **FastAPI 기본 서버 구성**
  - `GET /` 헬스체크성 루트 엔드포인트 제공
  - 서버 실행 시 JSON 메시지 반환으로 런타임 상태 확인
  - `main.py`는 앱 생성/미들웨어/라우터 등록 같은 설정 역할만 담당

- **종목 실시간 시세 API**
  - `GET /stock/{ticker}`
  - `yfinance.Ticker("<ticker>.KS")`를 통해 KRX 티커 데이터 조회
  - `fast_info.last_price`, `fast_info.previous_close` 기반으로 응답 데이터 구성

- **등락률 계산 로직**
  - 계산식:
    - `((current_price - previous_close) / previous_close) * 100`
  - `previous_close == 0`인 경우 분모 0 예외를 방지하기 위해 `change_percent = 0` 처리
  - 수치 필드는 `round(..., 2)`로 소수점 둘째 자리까지 정규화

- **예외 처리**
  - 데이터 조회/가공 과정 전체를 `try/except`로 보호
  - 예외 발생 시 에러 문자열과 사용자용 메시지를 포함한 JSON 반환

### 예정 기능

- 전체 종목 리스트 반환 API
- 종목 검색 API
- CORS 설정 적용

## 4. API Specification (Current)

### `GET /`

- **Description**: 서버 동작 여부 확인
- **Response Example**

```json
{
  "message": "Korea Stock App Backend is Running!"
}
```

### `GET /stock/{ticker}`

- **Description**: 요청한 티커의 실시간 시세 및 등락률 조회 (`005930` 입력 시 `005930.KS`로 정규화)
- **Success Response Example**

```json
{
  "name": "삼성전자",
  "current_price": 75400.12,
  "change_percent": 1.38
}
```

- **Error Response Example**

```json
{
  "error": "detailed error message",
  "message": "데이터 가공 중 오류가 발생했습니다."
}
```

## 5. Future Roadmap

- Supabase DB 연동을 통한 시세 데이터 캐싱 처리
- 실시간 시세 조회 성능 최적화를 위한 비동기 처리 도입
- Swagger UI 기반 API 문서 자동 생성 기능 적극 활용 (FastAPI 기본 OpenAPI 스키마 활용)

## 6. Environment Setup

### 1) 가상 환경 생성

#### Windows (PowerShell)

```powershell
python -m venv venv
```

#### macOS / Linux

```bash
python3 -m venv venv
```

### 2) 가상 환경 활성화

#### Windows (PowerShell)

```powershell
.\venv\Scripts\Activate.ps1
```

#### macOS / Linux

```bash
source venv/bin/activate
```

### 3) 의존성 설치

아래 명령으로 의존성을 설치합니다.

```bash
pip install -r requirements.txt
```

### 4) 개발 서버 실행

```bash
uvicorn main:app --reload
```

- 기본 접속 URL: `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## 7. Testing (TDD)

- 이 프로젝트는 **TDD(Test Driven Development)를 필수 원칙**으로 사용합니다.
- 기능 추가/변경 시 반드시 테스트를 먼저 작성하거나 동시에 보강해야 합니다.
- 외부 API(`yfinance`)에 의존하는 로직은 테스트에서 모킹하여 안정적으로 검증합니다.

### 테스트 실행

```bash
pytest
```
