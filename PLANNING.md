# MyLitUK - 영국 문학 정보 플랫폼 기획서

## 📋 프로젝트 개요

**MyLitUK**는 영국 문학 애호가들을 위한 종합 정보 플랫폼입니다. 사용자들이 좋아하는 작가의 신간, 문학 행사, 문학상 소식을 한 곳에서 모두 받아볼 수 있는 맞춤형 **사이트 내 알림** 서비스를 제공합니다.

**핵심 전략**: 이메일 대신 사이트 내 알림으로 사용자가 자주 방문하도록 유도합니다.

### 핵심 가치 제안
- **경험 (Experience)**: 문학 행사 정보 및 티켓팅
- **구매 (Purchase)**: 신간 및 수상작 즉시 구매 연동
- **뉴스 (News)**: 문학상 실시간 업데이트

---

## 🎯 핵심 기능 (3대 알림 시스템)

### 1️⃣ 신간 알림 (New Book Alerts)
**목표**: 사용자가 좋아하는 작가의 신간을 놓치지 않도록

#### 기능
- **작가 팔로우**: 사용자가 관심 작가를 팔로우
- **자동 알림**: 팔로우한 작가의 신간 출시 시 알림
- **구매 연동**: 알림에 Amazon/Waterstones/Bookshop.org 등 구매 링크 포함

#### 사용자 플로우
```
작가 페이지 방문 → '팔로우' 버튼 클릭 →
신간 출시 → 사이트 내 알림 생성 (🔔 배지 표시) →
사이트 재방문 → 알림 확인 → 구매 링크 클릭 → 외부 서점 이동
```

---

### 2️⃣ 행사 알림 (Event Alerts) ⭐ NEW
**목표**: 사용자가 관심 있는 문학 행사를 놓치지 않도록

#### 2-A. 특정 연례 행사 팔로우
##### 대상 행사 예시
- **Hay Festival** (헤이 페스티벌)
- **Edinburgh International Book Festival** (에든버러 국제 도서 축제)
- **Cheltenham Literature Festival**
- **London Literature Festival**
- **Manchester Literature Festival**
- **Latitude Festival** (문학 섹션)

##### 기능
- 행사 상세 페이지에서 '팔로우' 버튼
- 내년도 일정 발표 알림
- **티켓 오픈 알림** (가장 중요!)
- 프로그램 발표 알림

#### 2-B. 키워드/지역 기반 알림 설정
##### 설정 항목
- **지역**: 런던, 맨체스터, 에든버러, 버밍엄, 브리스톨 등
- **키워드**:
  - 장르 (Poetry, Fiction, Non-fiction, Crime, SF, Fantasy 등)
  - 이벤트 유형 (Reading, Discussion, Workshop, Book Signing 등)
  - 특정 작가명

##### 알림 트리거
- 설정한 키워드/지역에 맞는 신규 행사 등록 시

#### 사용자 플로우
```
[타입 A]
행사 페이지 → '팔로우' 클릭 →
티켓 오픈 → 알림 수신 → 티켓 구매 사이트 이동

[타입 B]
마이페이지 → '행사 알림 설정' →
지역/키워드 입력 → 저장 →
매칭되는 신규 행사 등록 → 알림 수신
```

---

### 3️⃣ 문학상 알림 (Literary Award Alerts) ⭐ NEW
**목표**: 문학계 소식에 관심 많은 팬들을 위한 실시간 업데이트

#### 대상 문학상
##### 주요 문학상 리스트
- **The Booker Prize** (부커상)
- **Women's Prize for Fiction** (여성 소설상)
- **Costa Book Awards**
- **The Bailey's Prize**
- **National Book Critics Circle Award** (UK 후보)
- **The Guardian First Book Award**
- **T.S. Eliot Prize** (시 부문)
- **Samuel Johnson Prize** (논픽션)

#### 단계별 알림 시스템
```
1단계: Longlist (1차 후보) 발표 → 알림
2단계: Shortlist (최종 후보) 발표 → 알림
3단계: Winner (수상자) 발표 → 알림 + 구매 링크
```

#### 구매 연동 강화
- **즉시 구매**: 수상작 발표 알림에 구매 링크 포함
- **위시리스트 자동 추가**: Shortlist 도서 자동 저장 옵션
- **특가 알림**: 수상 후 할인 이벤트 시 추가 알림

#### 사용자 플로우
```
문학상 페이지 → '팔로우' 클릭 →
Longlist 발표 → 알림 (도서 목록 확인) →
Shortlist 발표 → 알림 (관심 도서 북마크) →
Winner 발표 → 알림 + 구매 링크 → 즉시 구매
```

---

## 🏗️ 시스템 아키텍처

### 기술 스택 제안

#### Backend
```
- Language: Python 3.11+
- Framework: FastAPI (고성능, 비동기 지원, 자동 API 문서화)
- ORM: SQLAlchemy 2.0 (async 지원)
- Database: PostgreSQL 15+
- Task Queue: Celery + Redis (알림 발송용)
- Cache: Redis
```

#### Frontend
```
- Framework: Next.js 14 (React)
- Language: TypeScript
- UI Library: Tailwind CSS + shadcn/ui
- State Management: Zustand or React Query
```

#### Infrastructure
```
- Web Server: Nginx
- Application Server: Uvicorn (ASGI)
- Container: Docker + Docker Compose
- Deployment: AWS / GCP / Vercel (Frontend)
```

#### External Services
```
- WebSocket/SSE: 실시간 알림 (자체 구현)
- Push Notification: (선택적) PWA 브라우저 푸시
- External APIs:
  - Open Library API (도서 정보) - 무료
  - Google Books API (보조) - 무료 티어
  - Web Scraping (행사/문학상 정보)
```

---

## 🗄️ 데이터베이스 스키마 설계

### 핵심 테이블

#### 1. Users (사용자)
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(200),
    notification_in_app BOOLEAN DEFAULT TRUE,  -- 사이트 내 알림
    notification_browser_push BOOLEAN DEFAULT FALSE,  -- 브라우저 푸시 (선택)
    last_visit TIMESTAMP,  -- 마지막 방문 시간
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 2. Authors (작가)
```sql
CREATE TABLE authors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    name_ko VARCHAR(200),  -- 한글 이름
    bio TEXT,
    birth_date DATE,
    nationality VARCHAR(100) DEFAULT 'UK',
    photo_url VARCHAR(500),
    website_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 3. Books (도서)
```sql
CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    title_ko VARCHAR(500),  -- 한글 제목
    author_id INTEGER REFERENCES authors(id),
    isbn VARCHAR(13) UNIQUE,
    publication_date DATE,
    publisher VARCHAR(200),
    genre VARCHAR(100),
    description TEXT,
    cover_image_url VARCHAR(500),
    amazon_url VARCHAR(500),
    waterstones_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 4. Events (행사)
```sql
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    name VARCHAR(300) NOT NULL,
    name_ko VARCHAR(300),  -- 한글 이름
    type VARCHAR(50),  -- 'festival', 'reading', 'discussion', 'workshop'
    is_annual BOOLEAN DEFAULT FALSE,  -- 연례 행사 여부
    description TEXT,
    venue VARCHAR(300),
    city VARCHAR(100),
    region VARCHAR(100),  -- 'London', 'Manchester', 'Edinburgh' etc.
    start_date DATE,
    end_date DATE,
    ticket_url VARCHAR(500),
    ticket_open_date TIMESTAMP,  -- 티켓 오픈 시간
    website_url VARCHAR(500),
    image_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 5. Event Keywords (행사 키워드)
```sql
CREATE TABLE event_keywords (
    id SERIAL PRIMARY KEY,
    event_id INTEGER REFERENCES events(id) ON DELETE CASCADE,
    keyword VARCHAR(100) NOT NULL,  -- 'Poetry', 'Fiction', 'Crime' etc.
    UNIQUE(event_id, keyword)
);
```

#### 6. Literary Awards (문학상)
```sql
CREATE TABLE literary_awards (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    name_ko VARCHAR(200),  -- 한글 이름
    description TEXT,
    category VARCHAR(100),  -- 'Fiction', 'Poetry', 'Non-fiction'
    annual_cycle INTEGER DEFAULT 1,  -- 연례 주기
    website_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 7. Award Announcements (문학상 발표)
```sql
CREATE TABLE award_announcements (
    id SERIAL PRIMARY KEY,
    award_id INTEGER REFERENCES literary_awards(id),
    year INTEGER NOT NULL,
    stage VARCHAR(20) NOT NULL,  -- 'longlist', 'shortlist', 'winner'
    announcement_date TIMESTAMP,
    announced BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(award_id, year, stage)
);
```

#### 8. Award Nominees (후보작)
```sql
CREATE TABLE award_nominees (
    id SERIAL PRIMARY KEY,
    announcement_id INTEGER REFERENCES award_announcements(id),
    book_id INTEGER REFERENCES books(id),
    is_winner BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 알림 관련 테이블

#### 9. User Author Follows (작가 팔로우)
```sql
CREATE TABLE user_author_follows (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    author_id INTEGER REFERENCES authors(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, author_id)
);
```

#### 10. User Event Follows (행사 팔로우)
```sql
CREATE TABLE user_event_follows (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    event_id INTEGER REFERENCES events(id) ON DELETE CASCADE,
    notify_on_ticket_open BOOLEAN DEFAULT TRUE,
    notify_on_program_update BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, event_id)
);
```

#### 11. User Event Alert Preferences (행사 알림 설정)
```sql
CREATE TABLE user_event_alert_preferences (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    region VARCHAR(100),  -- 'London', 'Manchester' etc.
    keywords TEXT[],  -- PostgreSQL array: ['Poetry', 'Fiction']
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 12. User Award Follows (문학상 팔로우)
```sql
CREATE TABLE user_award_follows (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    award_id INTEGER REFERENCES literary_awards(id) ON DELETE CASCADE,
    notify_longlist BOOLEAN DEFAULT TRUE,
    notify_shortlist BOOLEAN DEFAULT TRUE,
    notify_winner BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, award_id)
);
```

#### 13. Notifications (알림 기록)
```sql
CREATE TABLE notifications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL,  -- 'new_book', 'event_ticket', 'award_longlist' etc.
    title VARCHAR(300) NOT NULL,
    message TEXT NOT NULL,
    related_id INTEGER,  -- book_id, event_id, or announcement_id
    related_type VARCHAR(50),  -- 'book', 'event', 'award'
    action_url VARCHAR(500),  -- 구매/티켓 링크
    priority VARCHAR(20) DEFAULT 'medium',  -- 'high', 'medium', 'low'
    is_read BOOLEAN DEFAULT FALSE,
    read_at TIMESTAMP,  -- 읽은 시간
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 빠른 조회를 위한 인덱스
CREATE INDEX idx_notifications_user_unread
    ON notifications(user_id, is_read, created_at DESC);
```

#### 14. User Visit Streaks (방문 연속 기록) ⭐ NEW
```sql
CREATE TABLE user_visit_streaks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    visit_date DATE NOT NULL,
    streak_count INTEGER DEFAULT 1,
    UNIQUE(user_id, visit_date)
);
```

---

## 🔗 API 엔드포인트 설계

### 인증 (Authentication)
```
POST   /api/auth/register          # 회원가입
POST   /api/auth/login             # 로그인
POST   /api/auth/logout            # 로그아웃
POST   /api/auth/refresh           # 토큰 갱신
GET    /api/auth/me                # 내 정보 조회
```

### 작가 (Authors)
```
GET    /api/authors                # 작가 목록
GET    /api/authors/:id            # 작가 상세
POST   /api/authors/:id/follow     # 작가 팔로우
DELETE /api/authors/:id/follow     # 작가 언팔로우
GET    /api/authors/:id/books      # 작가의 도서 목록
```

### 도서 (Books)
```
GET    /api/books                  # 도서 목록
GET    /api/books/:id              # 도서 상세
GET    /api/books/new              # 신간 목록
GET    /api/books/award-winners    # 수상작 목록
```

### 행사 (Events)
```
GET    /api/events                 # 행사 목록
GET    /api/events/:id             # 행사 상세
POST   /api/events/:id/follow      # 행사 팔로우
DELETE /api/events/:id/follow      # 행사 언팔로우
GET    /api/events/upcoming        # 다가오는 행사
GET    /api/events/festivals       # 연례 페스티벌 목록
```

### 행사 알림 설정 (Event Alert Preferences)
```
GET    /api/me/event-alerts        # 내 알림 설정 조회
POST   /api/me/event-alerts        # 알림 설정 추가
PUT    /api/me/event-alerts/:id    # 알림 설정 수정
DELETE /api/me/event-alerts/:id    # 알림 설정 삭제
```

### 문학상 (Literary Awards)
```
GET    /api/awards                 # 문학상 목록
GET    /api/awards/:id             # 문학상 상세
POST   /api/awards/:id/follow      # 문학상 팔로우
DELETE /api/awards/:id/follow      # 문학상 언팔로우
GET    /api/awards/:id/nominees    # 후보작 목록 (연도별)
GET    /api/awards/:id/winners     # 역대 수상작
```

### 알림 (Notifications)
```
GET    /api/notifications              # 내 알림 목록
GET    /api/notifications/unread       # 안 읽은 알림
GET    /api/notifications/count        # 안 읽은 개수만 (배지용)
PUT    /api/notifications/:id/read     # 알림 읽음 처리
PUT    /api/notifications/mark-all-read # 모두 읽음
DELETE /api/notifications/:id          # 알림 삭제
GET    /api/notifications/stream       # 실시간 SSE (선택)
```

### 대시보드 (Dashboard) ⭐ NEW
```
GET    /api/dashboard/today            # 오늘의 업데이트
GET    /api/dashboard/timeline         # 개인화 타임라인
GET    /api/dashboard/recommendations  # 맞춤 추천
GET    /api/dashboard/weekly-report    # 주간 리포트
```

### 사용자 (User Profile)
```
GET    /api/me/follows/authors     # 팔로우 중인 작가
GET    /api/me/follows/events      # 팔로우 중인 행사
GET    /api/me/follows/awards      # 팔로우 중인 문학상
GET    /api/me/preferences         # 알림 설정
PUT    /api/me/preferences         # 알림 설정 수정
```

---

## 🔔 알림 생성 시스템 설계

### Celery Task 구조

#### Task 1: 신간 알림 생성 (Daily)
```python
@celery.task
def check_new_books():
    """
    1. 최근 24시간 내 등록된 신간 조회
    2. 해당 작가를 팔로우하는 사용자 목록 조회
    3. 각 사용자의 알림 테이블에 레코드 생성
    4. (선택) WebSocket으로 실시간 푸시
    """
```

#### Task 2: 행사 티켓 오픈 알림 생성 (Hourly)
```python
@celery.task
def check_event_ticket_opening():
    """
    1. 향후 24시간 내 티켓 오픈 예정 행사 조회
    2. 해당 행사를 팔로우하는 사용자 목록 조회
    3. 사전 알림 생성 (1일 전, 1시간 전)
    4. 우선순위 'high'로 설정
    """
```

#### Task 3: 신규 행사 매칭 알림 생성 (Daily)
```python
@celery.task
def match_new_events_to_preferences():
    """
    1. 최근 24시간 내 등록된 신규 행사 조회
    2. 각 행사의 region + keywords와 사용자 설정 매칭
    3. 매칭되는 사용자에게 알림 생성
    """
```

#### Task 4: 문학상 발표 알림 생성 (Daily)
```python
@celery.task
def check_award_announcements():
    """
    1. 오늘 발표 예정인 문학상 단계(longlist/shortlist/winner) 조회
    2. 해당 문학상을 팔로우하는 사용자 목록 조회
    3. 단계별 알림 생성
    4. Winner 발표 시: 우선순위 'high', 수상작 구매 링크 포함
    """
```

### 알림 우선순위
```
[High Priority] priority='high'
- 문학상 Winner 발표
- 행사 티켓 오픈 1시간 전
→ 빨간 배지, 시각적 강조

[Medium Priority] priority='medium'
- 신간 출시
- 문학상 Longlist/Shortlist
→ 파란 배지

[Low Priority] priority='low'
- 신규 행사 매칭
→ 회색 배지
```

### 실시간 알림 전송 (선택적)
```python
# Redis Pub/Sub로 실시간 알림
async def send_realtime_notification(user_id: int, notification: dict):
    """
    WebSocket 연결된 클라이언트에게 즉시 푸시
    """
    await redis.publish(f"user:{user_id}:notifications", json.dumps(notification))
```

---

## 👤 사용자 플로우 시나리오

### 시나리오 1: 신규 사용자 온보딩
```
1. 회원가입 (이메일 + 비밀번호)
2. 관심 장르 선택 (Fiction, Poetry, Crime 등)
3. 관심 지역 선택 (London, Manchester 등)
4. 추천 작가 목록 표시 → 3-5명 팔로우 유도
5. 추천 문학상 목록 표시 → 2-3개 팔로우 유도
6. 알림 설정 완료 → 대시보드로 이동
```

### 시나리오 2: 행사 티켓팅 성공 케이스
```
사용자: Sarah (런던 거주, 시(Poetry) 애호가)

1. [3개월 전] Edinburgh International Book Festival 팔로우
2. [1개월 전] "내년도 일정 발표" 알림 수신
3. [2주 전] "티켓 오픈 1주일 전" 사전 알림 수신
4. [티켓 오픈 1시간 전] "1시간 후 티켓 오픈!" 긴급 알림 수신
5. [정각] 알림 속 링크 클릭 → 공식 티켓 사이트 이동 → 구매 완료
```

### 시나리오 3: 문학상 수상작 즉시 구매
```
사용자: John (부커상 팔로워)

1. [8월] Booker Prize Longlist 발표 알림 수신
   → 13권 리스트 확인, 관심 도서 3권 북마크
2. [9월] Shortlist 발표 알림 수신
   → 6권 확인, 2권 추가 북마크
3. [10월] Winner 발표 알림 수신
   → 알림에 포함된 Amazon 링크 클릭 → 즉시 구매
```

---

## 🎨 UI/UX 주요 화면

### 0. 헤더 (모든 페이지 공통) ⭐ 핵심
```
┌─────────────────────────────────────────┐
│ MyLitUK  홈  행사  문학상   [🔔 3]  👤  │
│                            ↑             │
│                      읽지 않은 알림      │
└─────────────────────────────────────────┘
```

### 1. 홈 대시보드 (개인화)
```
안녕하세요, [사용자명]님! 👋
오늘 새로운 소식이 3건 있습니다.

[오늘의 업데이트]
📚 팔로우 중인 작가 신간 2건
🎭 다가오는 행사 1건
[상세보기]

[이번 주 놓치면 안 될 일정]
⏰ 2일 후: Hay Festival 티켓 오픈
📖 4일 후: Ian McEwan 신간 출시

[맞춤 추천]
당신이 좋아할 만한 행사
- Poetry Reading in London
```

### 2. 알림 페이지 (전용)
```
[알림]  [전체] [신간] [행사] [문학상]

오늘
─────────────────────────────
🎉 Booker Prize 수상작 발표!     ●
   "Prophet Song" 구매하기   5분 전

🎫 Hay Festival 티켓 오픈
   [지금 구매하기]        2시간 전

어제
─────────────────────────────
📚 Ian McEwan 신간 출시
   [상세보기]              어제
```

### 3. 마이페이지
```
[탭 구조]
- 팔로우 관리 (작가/행사/문학상)
- 알림 설정 (키워드/지역)
- 활동 통계 (연속 방문: 7일 🔥)
- 북마크/위시리스트
```

### 3. 행사 상세 페이지
```
- 행사 기본 정보
- [팔로우 버튼] ← 핵심
- 티켓 정보 & 링크
- 프로그램 (작가 라인업)
- 과거 행사 아카이브 (연례 행사일 경우)
```

### 4. 문학상 상세 페이지
```
- 문학상 소개
- [팔로우 버튼] ← 핵심
- 올해 일정 타임라인
- 현재 후보작 리스트 (Longlist/Shortlist)
- 역대 수상작
```

---

## 📊 관리자 기능

### Admin Dashboard
```
- 도서 등록/수정/삭제
- 행사 등록/수정/삭제
- 문학상 관리
- 문학상 발표 일정 등록
- 후보작 등록
- 알림 발송 로그
- 사용자 통계
```

### 크롤링 & 자동화
```
- Google Books API 연동 (신간 자동 수집)
- 주요 페스티벌 웹사이트 크롤링 (티켓 오픈 일정)
- 문학상 공식 사이트 크롤링 (발표 일정)
```

---

## 🚀 개발 로드맵

### Phase 1: MVP (4-6주)
```
✅ 백엔드
  - FastAPI 프로젝트 구조 설정
  - PostgreSQL 스키마 구축
  - 인증 시스템 (JWT)
  - 작가/도서 CRUD API
  - 신간 알림 기능

✅ 프론트엔드
  - Next.js 프로젝트 구조
  - 회원가입/로그인 페이지
  - 작가 목록/상세 페이지
  - 팔로우 기능 UI
```

### Phase 2: 행사 알림 (3-4주)
```
✅ 백엔드
  - 행사 테이블 & API
  - 행사 팔로우 로직
  - 키워드/지역 알림 설정 API
  - 티켓 오픈 알림 Celery Task

✅ 프론트엔드
  - 행사 목록/상세 페이지
  - 행사 검색 & 필터
  - 알림 설정 페이지
```

### Phase 3: 문학상 알림 (3-4주)
```
✅ 백엔드
  - 문학상 테이블 & API
  - 후보작 관리 시스템
  - 단계별 알림 로직
  - 구매 링크 자동 생성

✅ 프론트엔드
  - 문학상 목록/상세 페이지
  - 후보작 타임라인 UI
  - 알림 히스토리 페이지
```

### Phase 4: 고도화 (4-6주)
```
- 알림 다이제스트 (주간/월간)
- 추천 시스템 (AI 기반)
- 모바일 앱 (React Native)
- 관리자 대시보드
- 크롤링 자동화
```

---

## 📈 성공 지표 (KPI)

### 사용자 참여도 지표 (핵심!)
```
- 일일 활성 사용자 (DAU) ⭐
- 주간 활성 사용자 (WAU)
- 평균 세션 시간
- 재방문율 (Return Rate)
- 연속 방문 일수 (Streak)
```

### 알림 지표
```
- 알림 읽음률 (Read Rate)
- 알림 클릭률 (CTR)
- 평균 알림 확인 시간
- 안 읽은 알림 → 방문 전환율
```

### 팔로우 지표
```
- 평균 팔로우 수 (작가/행사/문학상)
- 팔로우 후 활성도
- 알림당 팔로우 전환율
```

### 비즈니스 지표
```
- 구매 링크 클릭 수
- 티켓 링크 클릭 수
- 제휴 수익 (Affiliate)
- 알림 → 구매 전환율
```

---

## 💡 향후 확장 아이디어

### 1. 소셜 기능
- 다른 사용자 팔로우
- 독서 모임 기능
- 행사 참석 인증
- 리뷰 & 평점

### 2. 프리미엄 기능
- 조기 티켓 정보 (얼리버드)
- 한정판 도서 사전 예약
- VIP 행사 초대
- 광고 제거

### 3. 커뮤니티
- 도서 토론 포럼
- 행사 후기 공유
- 작가 Q&A
- 독서 챌린지

---

## 📚 참고 자료

### 벤치마킹 사이트
- **Goodreads**: 도서 추천 & 리뷰
- **Eventbrite**: 행사 검색 & 알림
- **Literary Hub**: 문학 뉴스 큐레이션
- **The Guardian Books**: 문학상 뉴스

### 주요 데이터 소스
- Google Books API
- Open Library API
- Eventbrite API
- 각 문학상 공식 웹사이트

---

## ✅ 다음 단계

1. **기술 스택 최종 확정**
2. **프로젝트 구조 세팅**
   - Backend (FastAPI + PostgreSQL)
   - Frontend (Next.js)
   - Docker Compose
3. **데이터베이스 마이그레이션 생성**
4. **MVP 개발 시작**

---

## 🔄 버전 히스토리

### v2.0 (2025-10-24) - 사이트 내 알림으로 전면 변경
**주요 변경사항**:
- ❌ 이메일 알림 제거
- ✅ 사이트 내 알림으로 전환
- ✅ 읽지 않은 알림 배지 (🔔) 추가
- ✅ 개인화된 대시보드 추가
- ✅ 연속 방문 스트릭 추가
- ✅ 실시간 알림 (WebSocket/SSE) 옵션 추가

**전략 변경**:
- 이메일로 알림 → 사이트 방문 유도 전략으로 변경
- 사용자가 사이트를 자주 방문하도록 유도하는 것이 목표

### v1.0 (2025-10-24) - 초기 기획
- 3대 알림 시스템 설계
- 이메일 기반 알림

---

**작성일**: 2025-10-24
**버전**: 2.0 (In-App Notifications)
**작성자**: Claude (AI Assistant)
