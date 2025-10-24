# 다국어 지원 (영어/한국어)

## 🌍 언어 지원

MyLitUK는 **영어**와 **한국어** 2개 언어를 지원합니다.

---

## 🎯 언어 선택 방식

### 1. 사용자 인터페이스
```
헤더 우측에 언어 선택:
┌─────────────────────────────────────────┐
│ MyLitUK  Home  Events  Awards  🔔  [EN ▼] │
└─────────────────────────────────────────┘
                                    ↑
                            클릭하면 드롭다운:
                            - English (EN)
                            - 한국어 (KO)
```

### 2. 자동 감지 (초기 방문 시)
```
1순위: 사용자 설정 (로그인 사용자)
2순위: 브라우저 언어 설정
3순위: 기본값 (영어)
```

---

## 🗄️ 데이터베이스 다국어 필드

### 기존 테이블에 다국어 필드 추가

#### Authors (작가)
```sql
CREATE TABLE authors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,           -- 영어 이름 (기본)
    name_ko VARCHAR(200),                 -- 한국어 이름
    bio TEXT,                             -- 영어 소개
    bio_ko TEXT,                          -- 한국어 소개
    birth_date DATE,
    nationality VARCHAR(100) DEFAULT 'UK',
    photo_url VARCHAR(500),
    website_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 예시 데이터
INSERT INTO authors (name, name_ko, bio, bio_ko) VALUES
('Hilary Mantel', '힐러리 맨텔',
 'British author, best known for her historical novels',
 '영국 작가, 역사 소설로 유명함');
```

#### Books (도서)
```sql
CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,          -- 영어 제목
    title_ko VARCHAR(500),                -- 한국어 제목
    author_id INTEGER REFERENCES authors(id),
    isbn VARCHAR(13) UNIQUE,
    publication_date DATE,
    publisher VARCHAR(200),
    genre VARCHAR(100),
    description TEXT,                     -- 영어 설명
    description_ko TEXT,                  -- 한국어 설명
    cover_image_url VARCHAR(500),
    amazon_url VARCHAR(500),
    waterstones_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 예시 데이터
INSERT INTO books (title, title_ko, description, description_ko) VALUES
('Wolf Hall', '울프 홀',
 'A historical novel about Thomas Cromwell',
 '토마스 크롬웰에 관한 역사 소설');
```

#### Events (행사)
```sql
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    name VARCHAR(300) NOT NULL,           -- 영어 이름
    name_ko VARCHAR(300),                 -- 한국어 이름
    type VARCHAR(50),
    is_annual BOOLEAN DEFAULT FALSE,
    description TEXT,                     -- 영어 설명
    description_ko TEXT,                  -- 한국어 설명
    venue VARCHAR(300),
    venue_ko VARCHAR(300),                -- 한국어 장소명
    city VARCHAR(100),
    region VARCHAR(100),
    start_date DATE,
    end_date DATE,
    ticket_url VARCHAR(500),
    ticket_open_date TIMESTAMP,
    website_url VARCHAR(500),
    image_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 예시 데이터
INSERT INTO events (name, name_ko, description, description_ko, venue, venue_ko) VALUES
('Hay Festival', '헤이 페스티벌',
 'Annual literature and arts festival in Wales',
 '웨일스에서 열리는 연례 문학 및 예술 축제',
 'Hay-on-Wye, Wales', '웨일스 헤이온와이');
```

#### Literary Awards (문학상)
```sql
CREATE TABLE literary_awards (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,           -- 영어 이름
    name_ko VARCHAR(200),                 -- 한국어 이름
    description TEXT,                     -- 영어 설명
    description_ko TEXT,                  -- 한국어 설명
    category VARCHAR(100),
    annual_cycle INTEGER DEFAULT 1,
    website_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 예시 데이터
INSERT INTO literary_awards (name, name_ko, description, description_ko) VALUES
('The Booker Prize', '부커상',
 'Leading literary award in the English-speaking world',
 '영어권 최고의 문학상');
```

#### Users (사용자 언어 설정)
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(200),
    preferred_language VARCHAR(2) DEFAULT 'en',  -- 'en' or 'ko' ⭐ NEW
    notification_in_app BOOLEAN DEFAULT TRUE,
    notification_browser_push BOOLEAN DEFAULT FALSE,
    last_visit TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🔧 API 다국어 처리

### 방법 1: Accept-Language 헤더 (권장)
```http
GET /api/authors/1
Accept-Language: ko

Response:
{
  "id": 1,
  "name": "힐러리 맨텔",
  "bio": "영국 작가, 역사 소설로 유명함",
  ...
}
```

### 방법 2: 쿼리 파라미터
```http
GET /api/authors/1?lang=ko

Response:
{
  "id": 1,
  "name": "힐러리 맨텔",
  "bio": "영국 작가, 역사 소설로 유명함",
  ...
}
```

### FastAPI 구현 예시
```python
from fastapi import Header, Query
from typing import Optional

def get_localized_field(obj, field: str, lang: str):
    """
    언어에 맞는 필드 반환
    예: get_localized_field(author, 'name', 'ko') → author.name_ko or author.name
    """
    if lang == 'ko':
        ko_field = getattr(obj, f"{field}_ko", None)
        if ko_field:
            return ko_field
    return getattr(obj, field)

@app.get("/api/authors/{author_id}")
async def get_author(
    author_id: int,
    accept_language: Optional[str] = Header(None),
    lang: Optional[str] = Query(None)
):
    # 언어 결정 (우선순위: lang 파라미터 > Accept-Language 헤더 > 기본값)
    language = lang or (accept_language.split(',')[0][:2] if accept_language else 'en')

    author = db.query(Author).filter(Author.id == author_id).first()

    return {
        "id": author.id,
        "name": get_localized_field(author, 'name', language),
        "bio": get_localized_field(author, 'bio', language),
        ...
    }
```

---

## 🎨 프론트엔드 다국어 (Next.js)

### 1. next-intl 라이브러리 사용 (권장)
```bash
npm install next-intl
```

### 2. 번역 파일 구조
```
frontend/
├── messages/
│   ├── en.json          # 영어 번역
│   └── ko.json          # 한국어 번역
├── app/
│   └── [locale]/
│       ├── layout.tsx
│       └── page.tsx
```

### 3. 번역 파일 예시

#### messages/en.json
```json
{
  "header": {
    "home": "Home",
    "events": "Events",
    "awards": "Awards",
    "login": "Login",
    "signup": "Sign Up"
  },
  "dashboard": {
    "greeting": "Hello, {name}!",
    "todayUpdates": "Today's Updates ({count})",
    "newBooks": "New books from authors you follow",
    "upcomingEvents": "Upcoming events",
    "awardNews": "Literary award news"
  },
  "notifications": {
    "newBook": "{author} has released a new book: {title}",
    "ticketOpen": "{event} tickets are now on sale!",
    "awardAnnounced": "{award} {stage} announced"
  }
}
```

#### messages/ko.json
```json
{
  "header": {
    "home": "홈",
    "events": "행사",
    "awards": "문학상",
    "login": "로그인",
    "signup": "회원가입"
  },
  "dashboard": {
    "greeting": "안녕하세요, {name}님!",
    "todayUpdates": "오늘 업데이트 ({count}건)",
    "newBooks": "팔로우 중인 작가의 신간",
    "upcomingEvents": "다가오는 행사",
    "awardNews": "문학상 소식"
  },
  "notifications": {
    "newBook": "{author} 작가의 신간 출시: {title}",
    "ticketOpen": "{event} 티켓이 오픈되었습니다!",
    "awardAnnounced": "{award} {stage} 발표"
  }
}
```

### 4. 컴포넌트에서 사용
```tsx
// app/[locale]/page.tsx
import { useTranslations } from 'next-intl';

export default function Dashboard() {
  const t = useTranslations('dashboard');

  return (
    <div>
      <h1>{t('greeting', { name: 'Sarah' })}</h1>
      <h2>{t('todayUpdates', { count: 3 })}</h2>

      <section>
        <h3>{t('newBooks')}</h3>
        {/* ... */}
      </section>
    </div>
  );
}
```

### 5. 언어 선택 컴포넌트
```tsx
// components/LanguageSwitcher.tsx
'use client';

import { useRouter, usePathname } from 'next/navigation';
import { useState } from 'react';

export function LanguageSwitcher() {
  const router = useRouter();
  const pathname = usePathname();
  const [isOpen, setIsOpen] = useState(false);

  const currentLocale = pathname.split('/')[1]; // 'en' or 'ko'

  const switchLanguage = (locale: string) => {
    // pathname에서 현재 locale을 새 locale로 변경
    const newPath = pathname.replace(/^\/(en|ko)/, `/${locale}`);
    router.push(newPath);
    setIsOpen(false);
  };

  return (
    <div className="relative">
      <button onClick={() => setIsOpen(!isOpen)}>
        {currentLocale === 'ko' ? '한국어' : 'English'} ▼
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 bg-white shadow-lg">
          <button onClick={() => switchLanguage('en')}>
            English (EN)
          </button>
          <button onClick={() => switchLanguage('ko')}>
            한국어 (KO)
          </button>
        </div>
      )}
    </div>
  );
}
```

---

## 📝 UI 텍스트 번역 전략

### 번역 필요한 부분
```
✅ 고정 텍스트 (UI 라벨, 버튼, 메시지)
  → messages/en.json, ko.json

✅ 데이터베이스 콘텐츠 (작가명, 도서 제목, 행사명)
  → 테이블의 _ko 필드

❌ 번역 불필요 (공통)
  → ISBN, URL, 날짜, 숫자
```

### 번역 우선순위

#### 1순위 (필수)
```
- 헤더 메뉴
- 로그인/회원가입
- 대시보드 주요 텍스트
- 알림 메시지
- 버튼 라벨
```

#### 2순위 (중요)
```
- 작가명 (유명 작가만)
- 도서 제목 (번역서가 있는 경우)
- 행사명 (주요 페스티벌)
- 문학상명
```

#### 3순위 (선택)
```
- 상세 설명
- 행사 장소명
- 긴 텍스트 콘텐츠
```

---

## 🔄 데이터 수집 시 다국어 처리

### 크롤링/API 수집 시
```python
# scripts/check_new_books.py
def fetch_book_from_api(isbn):
    """
    1. Open Library API에서 영어 정보 가져오기
    2. 한국어 번역 확인 (선택적)
    """
    # 영어 정보
    en_data = openlibrary_api.get_book(isbn)

    # 한국어 번역서가 있는지 확인 (Google Books API)
    ko_data = google_books_api.search(
        f"{en_data['title']} 한국어"
    )

    return {
        "title": en_data["title"],
        "title_ko": ko_data["title"] if ko_data else None,
        "description": en_data["description"],
        "description_ko": ko_data["description"] if ko_data else None,
    }
```

### 수동 번역 필요한 경우
```
주요 콘텐츠만 수동 번역:
- Top 100 작가명
- 주요 문학상 10개
- 연례 페스티벌 20개

나머지는 영어 원문 그대로 표시
```

---

## 🎯 사용자 경험

### 영어 사용자
```
1. 사이트 방문 (브라우저 언어: en)
2. 자동으로 영어 UI
3. 모든 콘텐츠 영어로 표시
```

### 한국어 사용자
```
1. 사이트 방문 (브라우저 언어: ko)
2. 자동으로 한국어 UI
3. 콘텐츠:
   - 한국어 번역 있음 → 한국어 표시
   - 한국어 번역 없음 → 영어 원문 표시
```

### 예시: 혼합 표시
```
┌─────────────────────────────────────────┐
│  안녕하세요, Sarah님!                    │  ← 한국어 UI
│  오늘 업데이트 (3건)                     │  ← 한국어 UI
├─────────────────────────────────────────┤
│  📚 힐러리 맨텔 신간 출시                │  ← 한국어 작가명
│     "The Mirror & The Light"             │  ← 영어 원제 (번역서 없음)
│     [구매하기]                           │  ← 한국어 버튼
│                                          │
│  🎭 헤이 페스티벌 티켓 오픈 (2일 후)    │  ← 한국어 행사명
│     [알림받기]                           │  ← 한국어 버튼
└─────────────────────────────────────────┘

→ 자연스러운 혼합 표시!
```

---

## 🗂️ 파일 구조 (다국어 지원 포함)

```
MyLitUK/
├── frontend/
│   ├── messages/
│   │   ├── en.json                  # 영어 번역
│   │   └── ko.json                  # 한국어 번역
│   ├── app/
│   │   └── [locale]/                # locale 기반 라우팅
│   │       ├── layout.tsx
│   │       ├── page.tsx
│   │       ├── events/
│   │       └── awards/
│   └── components/
│       └── LanguageSwitcher.tsx
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── utils/
│   │   │       └── i18n.py         # 다국어 헬퍼 함수
│   │   └── models/
│   │       └── base.py             # 다국어 필드 믹스인
│
└── scripts/
    └── translate_data.py           # 데이터 번역 스크립트
```

---

## 📊 API 응답 예시

### 영어 요청
```http
GET /api/dashboard
Accept-Language: en

Response:
{
  "updates": [
    {
      "type": "new_book",
      "author": "Hilary Mantel",
      "title": "The Mirror & The Light",
      "message": "Hilary Mantel has released a new book"
    },
    {
      "type": "event_ticket",
      "event": "Hay Festival",
      "message": "Hay Festival tickets are now on sale!"
    }
  ]
}
```

### 한국어 요청
```http
GET /api/dashboard
Accept-Language: ko

Response:
{
  "updates": [
    {
      "type": "new_book",
      "author": "힐러리 맨텔",
      "title": "The Mirror & The Light",
      "message": "힐러리 맨텔 작가의 신간 출시"
    },
    {
      "type": "event_ticket",
      "event": "헤이 페스티벌",
      "message": "헤이 페스티벌 티켓이 오픈되었습니다!"
    }
  ]
}
```

---

## ✅ 구현 체크리스트

### 데이터베이스
```
✅ authors 테이블에 name_ko, bio_ko 추가
✅ books 테이블에 title_ko, description_ko 추가
✅ events 테이블에 name_ko, description_ko, venue_ko 추가
✅ literary_awards 테이블에 name_ko, description_ko 추가
✅ users 테이블에 preferred_language 추가
```

### 백엔드
```
✅ Accept-Language 헤더 처리
✅ 다국어 필드 선택 로직
✅ API 응답 다국어화
```

### 프론트엔드
```
✅ next-intl 설치 및 설정
✅ messages/en.json, ko.json 작성
✅ [locale] 라우팅 설정
✅ LanguageSwitcher 컴포넌트
✅ 모든 UI 텍스트 t() 함수로 변경
```

### 데이터
```
✅ 주요 작가명 한국어 번역
✅ 주요 문학상 한국어 번역
✅ 주요 행사명 한국어 번역
```

---

## 🎉 결과

### 사용자에게 보이는 것
```
헤더에 언어 선택 버튼 [EN ▼]
클릭하면:
  - English (EN)
  - 한국어 (KO)

선택 즉시 전체 UI 언어 변경!
```

### 자동 감지
```
한국에서 접속 → 자동 한국어
미국에서 접속 → 자동 영어

로그인 사용자 → 설정한 언어 우선
```

### 유연한 표시
```
번역 있음 → 해당 언어로 표시
번역 없음 → 영어 원문 표시

자연스럽게 혼합 가능!
```

---

**작성일**: 2025-10-24
**언어**: 영어 (en) + 한국어 (ko)
**기본 언어**: 영어
