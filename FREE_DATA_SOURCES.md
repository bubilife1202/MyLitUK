# 무료 데이터 소스 및 API 가이드

## 📚 도서 정보 (Books Data)

### 1. Open Library API ⭐ 추천
```
URL: https://openlibrary.org/developers/api
무료 여부: 완전 무료
제한: 없음 (Fair Use)
```

**제공 정보**:
- 도서 메타데이터 (제목, 작가, ISBN, 출판일)
- 표지 이미지
- 작가 정보
- 검색 API

**API 예시**:
```bash
# 도서 검색
GET https://openlibrary.org/search.json?q=booker+prize&author=hilary+mantel

# ISBN으로 도서 정보
GET https://openlibrary.org/api/books?bibkeys=ISBN:0385504209&format=json

# 작가 정보
GET https://openlibrary.org/authors/OL23919A.json

# 표지 이미지
GET https://covers.openlibrary.org/b/isbn/0385504209-L.jpg
```

### 2. Google Books API
```
URL: https://developers.google.com/books
무료 여부: 무료 (제한 있음)
제한: 1일 1,000 requests (무료 티어)
```

**제공 정보**:
- 도서 상세 정보
- 미리보기
- 판매 링크 (Google Play Books)

**API 예시**:
```bash
# 도서 검색
GET https://www.googleapis.com/books/v1/volumes?q=isbn:0385504209

# 작가로 검색
GET https://www.googleapis.com/books/v1/volumes?q=inauthor:hilary+mantel
```

### 3. ISBN DB API
```
URL: https://isbndb.com/
무료 여부: 제한적 무료
제한: 월 500 requests (무료 티어)
```

---

## 🎭 행사 정보 (Event Data)

### 실제 데이터 수집 방법

#### A. 공식 웹사이트 크롤링 (웹 스크래핑)
주요 문학 페스티벌의 공식 웹사이트에서 정보를 수집합니다.

**대상 웹사이트**:
```
1. Hay Festival
   - URL: https://www.hayfestival.com/
   - 정보: 행사 일정, 티켓 오픈 날짜

2. Edinburgh International Book Festival
   - URL: https://www.edbookfest.co.uk/
   - 정보: 프로그램, 티켓팅

3. Cheltenham Literature Festival
   - URL: https://www.cheltenhamfestivals.com/literature

4. London Literature Festival
   - URL: https://www.southbankcentre.co.uk/

5. Manchester Literature Festival
   - URL: https://manchesterliteraturefestival.co.uk/
```

**크롤링 도구**:
```python
# Python 라이브러리 (모두 무료)
- BeautifulSoup4: HTML 파싱
- Requests: HTTP 요청
- Scrapy: 고급 크롤링 프레임워크
- Playwright: 동적 페이지 크롤링

# 예시 코드
import requests
from bs4 import BeautifulSoup

def scrape_hay_festival():
    url = "https://www.hayfestival.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 행사 정보 추출 로직
    events = soup.find_all('div', class_='event-card')
    return events
```

#### B. RSS Feeds 활용
일부 사이트는 RSS 피드를 제공합니다.
```
- The Guardian Books RSS: https://www.theguardian.com/books/rss
- BBC Arts & Culture: https://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml
```

#### C. Eventbrite API (제한적)
```
URL: https://www.eventbrite.com/platform/api
무료 여부: 무료
제한: 상업적 사용 제한

# 영국 문학 행사 검색
GET https://www.eventbriteapi.com/v3/events/search/?q=literature&location.address=london
```

---

## 🏆 문학상 정보 (Literary Awards)

### 데이터 수집 방법

#### 1. 공식 웹사이트 크롤링 ⭐ 주요 방법

**주요 문학상 웹사이트**:
```
1. The Booker Prize
   - URL: https://thebookerprizes.com/
   - 정보: Longlist, Shortlist, Winner 발표 날짜

2. Women's Prize for Fiction
   - URL: https://www.womensprizeforfiction.co.uk/

3. Costa Book Awards
   - URL: https://costa.co.uk/behind-the-beans/costa-book-awards/

4. The Guardian First Book Award
   - URL: https://www.theguardian.com/books/guardianfirstbookaward

5. T.S. Eliot Prize
   - URL: https://tseliot.com/
```

**크롤링 전략**:
```python
# 정기적으로 체크 (Celery Task)
@celery.task
def check_booker_prize_updates():
    """
    매일 부커상 웹사이트를 체크하여
    새로운 발표가 있는지 확인
    """
    url = "https://thebookerprizes.com/the-booker-prize"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # "Longlist", "Shortlist", "Winner" 키워드 검색
    # 변경 감지 시 알림 발송
```

#### 2. Wikipedia API (보조 수단)
```
URL: https://www.mediawiki.org/wiki/API
무료 여부: 완전 무료

# 예시: 부커상 수상자 목록
GET https://en.wikipedia.org/api/rest_v1/page/html/Booker_Prize
```

#### 3. The Guardian API
```
URL: https://open-platform.theguardian.com/
무료 여부: 무료 (제한 있음)
제한: 1일 500 requests

# 문학상 뉴스 검색
GET https://content.guardianapis.com/search?q=booker%20prize&section=books
```

---

## 📧 이메일 발송 (무료 옵션)

### 1. SendGrid ⭐ 추천
```
무료 티어: 월 100 이메일/일 (영구 무료)
URL: https://sendgrid.com/
```

### 2. Mailgun
```
무료 티어: 월 5,000 이메일 (3개월)
URL: https://www.mailgun.com/
```

### 3. Gmail SMTP (개발/테스트용)
```
무료 티어: 1일 500 이메일
설정: SMTP (smtp.gmail.com:587)
```

### 4. Brevo (구 Sendinblue)
```
무료 티어: 월 300 이메일/일
URL: https://www.brevo.com/
```

---

## 💾 데이터베이스 (무료 호스팅)

### 1. PostgreSQL - Supabase ⭐ 추천
```
무료 티어:
- 500MB 데이터베이스
- 무제한 API 요청
- 50,000 MAU (월간 활성 사용자)
URL: https://supabase.com/
```

### 2. PostgreSQL - Neon
```
무료 티어:
- 3GB 스토리지
- 무제한 데이터베이스
URL: https://neon.tech/
```

### 3. PostgreSQL - Railway
```
무료 티어:
- $5 크레딧/월
- 1GB RAM
URL: https://railway.app/
```

---

## 🚀 호스팅 (무료 배포)

### Backend
```
1. Railway.app
   - 무료: $5 크레딧/월
   - FastAPI 지원

2. Render
   - 무료: 750시간/월
   - Python/Docker 지원
   - URL: https://render.com/

3. Fly.io
   - 무료: 3개 VM (256MB RAM)
   - URL: https://fly.io/
```

### Frontend
```
1. Vercel ⭐ 추천
   - 무료: 무제한 배포
   - Next.js 최적화
   - URL: https://vercel.com/

2. Netlify
   - 무료: 300 빌드 분/월
   - URL: https://www.netlify.com/

3. Cloudflare Pages
   - 무료: 무제한 요청
   - URL: https://pages.cloudflare.com/
```

---

## 🔄 작업 큐 & 캐시 (무료)

### Redis
```
1. Upstash Redis ⭐ 추천
   - 무료: 10,000 commands/일
   - URL: https://upstash.com/

2. Redis Cloud
   - 무료: 30MB
   - URL: https://redis.com/
```

---

## 🤖 크롤링 자동화 전략

### 방법 1: GitHub Actions (무료 CI/CD) ⭐ 추천
```yaml
# .github/workflows/scrape_data.yml
name: Daily Data Scraping

on:
  schedule:
    - cron: '0 9 * * *'  # 매일 오전 9시 (UTC)

jobs:
  scrape:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run scraping script
        run: python scripts/scrape_events.py
      - name: Update database
        run: python scripts/update_db.py
```

**장점**:
- 완전 무료
- 월 2,000분 무료 (일반 계정)
- 자동 스케줄링

### 방법 2: 로컬 Celery + 무료 서버
```python
# Celery Beat 스케줄
from celery import Celery
from celery.schedules import crontab

app = Celery('mylit')

app.conf.beat_schedule = {
    'scrape-events-daily': {
        'task': 'tasks.scrape_events',
        'schedule': crontab(hour=9, minute=0),
    },
    'check-awards-daily': {
        'task': 'tasks.check_awards',
        'schedule': crontab(hour=10, minute=0),
    },
}
```

---

## 📊 무료 기술 스택 최종 구성

```
┌─────────────────────────────────────────┐
│         Frontend (Vercel)               │
│   Next.js + TypeScript + Tailwind       │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│        Backend (Render/Fly.io)          │
│    FastAPI + SQLAlchemy + Celery        │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│      Database (Supabase/Neon)           │
│          PostgreSQL 15+                 │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│       Cache/Queue (Upstash)             │
│              Redis                      │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│     Email Service (SendGrid)            │
│        100 emails/day FREE              │
└─────────────────────────────────────────┘
```

---

## 🎯 데이터 수집 계획

### Phase 1: 초기 데이터베이스 구축

#### 1. 도서 데이터
```python
# Open Library API로 영국 작가 도서 수집
def fetch_uk_literature():
    authors = [
        "Hilary Mantel",
        "Kazuo Ishiguro",
        "Ian McEwan",
        "Zadie Smith",
        "Ali Smith",
        # ... 100+ 영국 작가
    ]

    for author in authors:
        books = fetch_from_openlibrary(author)
        save_to_database(books)
```

#### 2. 행사 데이터 (수동 + 크롤링)
```python
# 주요 연례 행사는 수동으로 먼저 등록
initial_events = [
    {
        "name": "Hay Festival",
        "is_annual": True,
        "city": "Hay-on-Wye",
        "website": "https://www.hayfestival.com/"
    },
    # ... 주요 행사 10-20개
]

# 이후 크롤링으로 업데이트
```

#### 3. 문학상 데이터 (수동)
```python
# 주요 문학상 목록은 직접 등록
literary_awards = [
    {
        "name": "The Booker Prize",
        "category": "Fiction",
        "website": "https://thebookerprizes.com/"
    },
    # ... 10-15개 주요 문학상
]
```

### Phase 2: 자동 업데이트

```python
# 매일 실행되는 스크립트
@daily_task
def update_all_data():
    # 1. 신간 체크
    check_new_books_from_openlibrary()

    # 2. 행사 웹사이트 크롤링
    scrape_hay_festival()
    scrape_edinburgh_festival()

    # 3. 문학상 발표 체크
    check_booker_prize_website()
    check_womens_prize_website()

    # 4. Guardian API로 뉴스 수집
    fetch_literary_news_from_guardian()
```

---

## ⚠️ 주의사항

### 1. 웹 스크래핑 법적 이슈
```
✅ 허용:
- robots.txt를 준수하는 크롤링
- 공개된 정보 수집
- 개인 정보 미수집

❌ 금지:
- 과도한 요청 (DDoS)
- 개인정보 수집
- 저작권 침해
```

### 2. API Rate Limiting 관리
```python
# 요청 제한 준수
import time
from ratelimit import limits, sleep_and_retry

@sleep_and_retry
@limits(calls=100, period=60)  # 1분에 100회
def call_api(url):
    return requests.get(url)
```

### 3. 캐싱 활용
```python
# 동일한 데이터를 반복 요청하지 않기
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_book_info(isbn):
    return call_openlibrary_api(isbn)
```

---

## 🎉 결론

### ✅ 완전 무료로 가능한 것:
1. **도서 정보**: Open Library API (무제한)
2. **행사 정보**: 웹 크롤링 (합법적 범위 내)
3. **문학상 정보**: 공식 사이트 크롤링 + Guardian API
4. **이메일 알림**: SendGrid (100통/일)
5. **호스팅**: Vercel + Render + Supabase
6. **자동화**: GitHub Actions

### ⚠️ 제한사항:
- 이메일 발송량 제한 (일 100-300통)
- API 요청 제한 (대부분 충분함)
- 서버 리소스 제한 (소규모 서비스는 충분)

### 💡 확장 시 고려사항:
- 사용자 1,000명 이상: 유료 이메일 플랜 필요
- 트래픽 증가: 서버 업그레이드 필요
- 고급 기능: 유료 API 사용 고려

**현재 계획으로는 초기 서비스 완전 무료 운영 가능!** 🚀
