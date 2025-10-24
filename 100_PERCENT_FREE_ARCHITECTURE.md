# 100% 무료 아키텍처 가이드

## 🎯 목표: 영구적으로 비용 $0으로 운영

**모든 서비스를 무료 티어로만 구성하여 초기 사용자 1,000-5,000명까지 완전 무료 운영**

---

## 🏗️ 완전 무료 기술 스택

```
┌─────────────────────────────────────────┐
│         Frontend                        │
│   Next.js 14 + TypeScript               │
│   호스팅: Vercel (무료)                  │
│   - 무제한 배포                          │
│   - 100GB 대역폭/월                      │
│   - 자동 SSL                             │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│         Backend API                     │
│   FastAPI + Python 3.11                 │
│   호스팅: Render.com (무료)              │
│   - 750시간/월 (충분함)                  │
│   - 512MB RAM                            │
│   - 자동 배포                            │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│         Database                        │
│   PostgreSQL 15                         │
│   호스팅: Supabase (무료)                │
│   - 500MB 데이터베이스                   │
│   - 무제한 API 요청                      │
│   - 자동 백업                            │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│      Cache & Task Queue                 │
│   Redis                                 │
│   호스팅: Upstash (무료)                 │
│   - 10,000 commands/일                   │
│   - 256MB 메모리                         │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│      Background Jobs                    │
│   GitHub Actions (무료)                 │
│   - 2,000분/월 (CI/CD)                   │
│   - 크롤링 자동화                        │
│   - 데이터 수집                          │
└─────────────────────────────────────────┘
```

---

## 📊 무료 티어 상세 스펙

### 1. Vercel (Frontend 호스팅) ✅ 완전 무료
```yaml
플랜: Hobby (Free)
제공:
  - 배포: 무제한
  - 프로젝트: 무제한
  - 대역폭: 100GB/월
  - 빌드: 6,000분/월
  - 도메인: 커스텀 도메인 1개 무료
  - SSL: 자동 무료
  - CDN: 전 세계 무료

제한사항:
  - 팀 멤버: 1명
  - 동시 빌드: 1개

✅ 우리 서비스: 충분함 (사용자 5,000명까지 가능)
```

### 2. Render.com (Backend 호스팅) ✅ 무료
```yaml
플랜: Free
제공:
  - 인스턴스: 무료 Web Service
  - 시간: 750시간/월 (항상 켜짐 상태로 충분)
  - RAM: 512MB
  - CPU: 공유
  - 대역폭: 100GB/월
  - 자동 배포: GitHub 연동
  - SSL: 자동 무료

제한사항:
  - 15분 미사용 시 슬립 모드 (첫 요청 시 재시작 ~30초)
  - Cron jobs: 불가 (GitHub Actions 사용)

✅ 우리 서비스: 충분함
⚠️ 주의: 슬립 모드 방지 필요 (아래 해결책 참고)
```

**슬립 모드 방지 무료 해결책**:
```yaml
방법 1: UptimeRobot (무료)
  - URL: https://uptimerobot.com
  - 5분마다 자동 핑
  - 50개 모니터 무료
  → 서비스가 항상 깨어있음

방법 2: GitHub Actions (무료)
  - 5분마다 health check 요청
  - 완전 무료
```

### 3. Supabase (PostgreSQL 호스팅) ✅ 무료
```yaml
플랜: Free
제공:
  - 데이터베이스: 500MB
  - 자동 백업: 7일
  - API 요청: 무제한
  - 대역폭: 무제한
  - 동시 연결: 60개
  - Row Level Security 지원

제한사항:
  - 프로젝트: 2개
  - 7일간 미사용 시 일시정지 (쉽게 재개)

✅ 우리 서비스: 500MB면 초기 충분
  - 사용자 10,000명: ~50MB
  - 도서 정보 5,000권: ~100MB
  - 행사/문학상: ~50MB
  - 알림 기록: ~300MB
  → 총 500MB 내로 가능
```

### 4. Upstash Redis (캐시) ✅ 무료
```yaml
플랜: Free
제공:
  - Commands: 10,000/일
  - 메모리: 256MB
  - 대역폭: 무제한
  - 동시 연결: 100개
  - TLS 암호화: 포함

제한사항:
  - 10,000 commands/일 초과 시 제한

✅ 우리 서비스: 충분함
  - 10,000 commands = 초당 0.1 commands 평균
  - 사용자 1,000명 기준 충분
```

### 5. GitHub Actions (자동화) ✅ 무료
```yaml
플랜: Free (Public Repo)
제공:
  - 빌드 시간: 2,000분/월
  - 저장 공간: 500MB
  - 스케줄 실행: Cron 지원

사용 계획:
  - 데이터 크롤링: 일 1회 (5분) = 150분/월
  - 알림 체크: 시간당 1회 (1분) = 720분/월
  - 백업: 주 1회 (5분) = 20분/월
  → 총 890분/월 (2,000분 내)

✅ 우리 서비스: 충분함
```

---

## 💾 데이터 소스 (완전 무료)

### 1. Open Library API ⭐ 추천
```yaml
URL: https://openlibrary.org
제한: 없음 (Fair Use)
제공:
  - 도서 검색
  - 작가 정보
  - ISBN 조회
  - 표지 이미지 (무료)

사용 예시:
  GET https://openlibrary.org/search.json?q=hilary+mantel
  GET https://openlibrary.org/authors/OL23919A.json
  GET https://covers.openlibrary.org/b/isbn/0385504209-L.jpg

✅ 무제한 무료!
```

### 2. Google Books API (보조)
```yaml
URL: https://developers.google.com/books
제한: 1,000 requests/일 (무료)
제공:
  - 도서 상세 정보
  - 미리보기

사용 계획:
  - Open Library에 없는 도서만 사용
  - 일 100-200 requests 예상
  → 1,000 requests 내 충분

✅ 무료 티어로 충분함
```

### 3. 웹 스크래핑 (완전 무료)
```python
# 필요한 무료 라이브러리
pip install requests beautifulsoup4 playwright

# 크롤링 대상
크롤링_대상 = [
    "Hay Festival 공식 사이트",
    "Edinburgh Book Festival 공식 사이트",
    "Booker Prize 공식 사이트",
    "Women's Prize 공식 사이트",
    # ... 등
]

# GitHub Actions로 일 1회 자동 실행
# → 완전 무료!
```

---

## 🔧 완전 무료 아키텍처 구현

### 디렉토리 구조
```
MyLitUK/
├── frontend/              # Next.js (Vercel 배포)
│   ├── app/
│   ├── components/
│   ├── lib/
│   └── public/
│
├── backend/               # FastAPI (Render 배포)
│   ├── app/
│   │   ├── api/
│   │   ├── models/
│   │   ├── services/
│   │   └── main.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── scripts/               # 크롤링 & 자동화
│   ├── scrape_events.py
│   ├── scrape_awards.py
│   └── check_new_books.py
│
├── .github/
│   └── workflows/
│       ├── scrape-daily.yml
│       ├── check-alerts.yml
│       └── keep-alive.yml
│
└── docs/
    ├── PLANNING.md
    ├── FREE_DATA_SOURCES.md
    └── 100_PERCENT_FREE_ARCHITECTURE.md
```

---

## 🤖 GitHub Actions 크롤링 자동화 (무료)

### 1. 일일 데이터 수집
```yaml
# .github/workflows/scrape-daily.yml
name: Daily Data Scraping

on:
  schedule:
    - cron: '0 9 * * *'  # 매일 오전 9시 UTC

jobs:
  scrape:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r scripts/requirements.txt

      - name: Scrape Events
        run: python scripts/scrape_events.py
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}

      - name: Scrape Awards
        run: python scripts/scrape_awards.py
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}

      - name: Check New Books
        run: python scripts/check_new_books.py
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}

# 완전 무료! (2,000분/월 제한 내)
```

### 2. 시간마다 알림 체크
```yaml
# .github/workflows/check-alerts.yml
name: Hourly Notification Check

on:
  schedule:
    - cron: '0 * * * *'  # 매시간

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Check Ticket Opening Alerts
        run: python scripts/check_ticket_alerts.py
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

### 3. 서버 슬립 방지 (Render용)
```yaml
# .github/workflows/keep-alive.yml
name: Keep Backend Alive

on:
  schedule:
    - cron: '*/10 * * * *'  # 10분마다

jobs:
  ping:
    runs-on: ubuntu-latest
    steps:
      - name: Ping Backend
        run: curl https://mylituk-api.onrender.com/health
```

---

## 🚀 배포 가이드 (완전 무료)

### Step 1: Supabase 데이터베이스 설정

```bash
# 1. https://supabase.com 회원가입 (무료)
# 2. New Project 생성
# 3. Database URL 복사:
#    postgresql://postgres:[PASSWORD]@db.[PROJECT].supabase.co:5432/postgres

# 4. SQL Editor에서 스키마 생성
# PLANNING.md의 CREATE TABLE 문 실행
```

### Step 2: Backend (Render) 배포

```bash
# 1. GitHub에 코드 푸시
git push origin main

# 2. https://render.com 회원가입 (무료)

# 3. New Web Service 생성
Name: mylituk-api
Runtime: Python 3.11
Build Command: pip install -r requirements.txt
Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT

# 4. Environment Variables 설정
DATABASE_URL=postgresql://[SUPABASE_URL]
REDIS_URL=redis://[UPSTASH_URL]

# 5. 자동 배포 완료!
```

### Step 3: Frontend (Vercel) 배포

```bash
# 1. https://vercel.com 회원가입 (무료)

# 2. GitHub 저장소 연동

# 3. 프로젝트 Import
Framework Preset: Next.js
Root Directory: ./frontend

# 4. Environment Variables 설정
NEXT_PUBLIC_API_URL=https://mylituk-api.onrender.com

# 5. Deploy 클릭 → 완료!
# 자동으로 mylituk.vercel.app 도메인 생성
```

### Step 4: Redis (Upstash) 설정

```bash
# 1. https://upstash.com 회원가입 (무료)

# 2. Create Database
Name: mylituk-redis
Region: 가장 가까운 지역 선택

# 3. Redis URL 복사
# Render 환경변수에 추가
```

### Step 5: GitHub Actions 활성화

```bash
# 1. GitHub Secrets 설정
Settings → Secrets → Actions

# 2. Secrets 추가
DATABASE_URL: [Supabase PostgreSQL URL]
API_URL: [Render Backend URL]

# 3. Actions 자동 실행 확인
# .github/workflows/ 파일들이 자동 실행됨
```

---

## 💰 비용 분석: 완전 $0

### 초기 단계 (사용자 0~1,000명)
```
Vercel:          $0/월 ✅
Render:          $0/월 ✅
Supabase:        $0/월 ✅
Upstash Redis:   $0/월 ✅
GitHub Actions:  $0/월 ✅
도메인:          $0/월 (vercel.app 사용)
SSL:             $0/월 (자동 포함)
모니터링:        $0/월 (UptimeRobot 무료)
───────────────────────
총합:            $0/월 🎉
```

### 성장 단계 (사용자 1,000~5,000명)
```
Vercel:          $0/월 ✅ (100GB 대역폭 내)
Render:          $0/월 ✅ (750시간 충분)
Supabase:        $0/월 ✅ (500MB 내)
Upstash Redis:   $0/월 ✅ (10,000 commands/일 내)
GitHub Actions:  $0/월 ✅ (2,000분/월 내)
───────────────────────
총합:            $0/월 🎉
```

### 무료 한계점 (업그레이드 필요 시점)
```
사용자 5,000명 초과 시:
- Vercel: 대역폭 100GB 초과 가능 → $20/월
- Supabase: 500MB 초과 → $25/월
- Render: 슬립 모드 불편 → $7/월

하지만 5,000명까지는 완전 무료! 🚀
```

---

## ⚠️ 무료 티어 제한사항 & 해결책

### 1. Render 슬립 모드 (15분 미사용 시)
```
문제: 첫 요청 시 30초 지연

해결책 1: UptimeRobot 무료 서비스
  - 5분마다 자동 핑
  - https://uptimerobot.com

해결책 2: GitHub Actions keep-alive
  - 10분마다 health check
  - 완전 무료

✅ 해결 완료!
```

### 2. Supabase 500MB 제한
```
문제: 데이터베이스 500MB 초과 우려

해결책:
  - 알림 데이터 90일 후 자동 삭제
  - 이미지는 외부 CDN 사용 (Open Library)
  - 불필요한 인덱스 최소화

예상 사용량:
  - 사용자 5,000명: 250KB = 1.25GB
  - 도서 10,000권: 200KB = 2GB
  - 알림 3개월분: ~300MB

  총: 500MB 내 유지 가능 ✅
```

### 3. GitHub Actions 2,000분/월 제한
```
문제: 크롤링 + CI/CD 시간 제한

해결책:
  - 효율적인 스크립트 (5분 내 완료)
  - 불필요한 빌드 최소화
  - 캐싱 활용

예상 사용:
  - 크롤링: 일 5분 × 30 = 150분
  - 알림 체크: 시간당 1분 × 24 × 30 = 720분
  - CI/CD: 100분

  총: 970분/월 (2,000분 내) ✅
```

### 4. API Rate Limiting
```
Open Library: 제한 없음 ✅
Google Books: 1,000 requests/일
  → 보조용으로만 사용 (100 requests/일)

✅ 문제 없음!
```

---

## 🎯 완전 무료 운영 체크리스트

### 필수 설정
```
✅ Vercel 배포 (Frontend)
✅ Render 배포 (Backend)
✅ Supabase 데이터베이스
✅ Upstash Redis
✅ GitHub Actions 자동화
✅ UptimeRobot 슬립 방지
✅ Open Library API 연동
```

### 비용 모니터링
```
✅ Vercel 대역폭 확인 (100GB 한도)
✅ Supabase 용량 확인 (500MB 한도)
✅ Upstash commands 확인 (10,000/일 한도)
✅ GitHub Actions 시간 확인 (2,000분/월 한도)
```

### 최적화
```
✅ 이미지는 외부 URL 사용 (데이터베이스 절약)
✅ API 응답 캐싱 (Redis)
✅ 오래된 알림 정리 (90일 후 삭제)
✅ 효율적인 크롤링 스크립트
```

---

## 🚀 무료로 시작하는 3단계

### Step 1: 개발 (로컬, 무료)
```bash
# 1. PostgreSQL 로컬 설치
docker run --name postgres -e POSTGRES_PASSWORD=dev -p 5432:5432 -d postgres:15

# 2. Redis 로컬 설치
docker run --name redis -p 6379:6379 -d redis:7

# 3. 개발 서버 실행
cd backend && uvicorn app.main:app --reload
cd frontend && npm run dev
```

### Step 2: 무료 호스팅 배포
```bash
# 1. Supabase 데이터베이스 생성
# 2. Render에 Backend 배포
# 3. Vercel에 Frontend 배포
# 4. GitHub Actions 활성화
```

### Step 3: 모니터링 (무료)
```bash
# 1. UptimeRobot 설정
# 2. Supabase Dashboard 확인
# 3. Render Logs 확인
# 4. Vercel Analytics 확인 (무료)
```

---

## 🎉 결론

### ✅ 완전 무료 운영 가능!
```
사용자 5,000명까지 영구 무료로 운영 가능합니다.

비용: $0/월
- 호스팅
- 데이터베이스
- 캐시
- 자동화
- SSL
- 도메인 (vercel.app)
- 모니터링

모두 무료! 🎉
```

### 💡 확장 시 고려사항
```
5,000명 초과 시:
Option 1: 유료 플랜 전환 (~$50/월)
Option 2: 추가 최적화로 무료 유지
Option 3: 후원/광고 수익으로 비용 충당
```

### 🚀 지금 바로 시작 가능!
```
1. GitHub 저장소 생성 (무료)
2. Vercel + Render + Supabase 가입 (모두 무료)
3. 배포 (자동, 무료)
4. 완성! 💪

총 소요 시간: 30분
총 비용: $0
```

---

**작성일**: 2025-10-24
**버전**: 1.0
**목표**: 100% 무료 운영 아키텍처
**결과**: ✅ 달성 가능!
