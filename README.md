# MyLitUK - 영국 문학 개인화 큐레이션 플랫폼

> "내가 원하는 영국 문학 정보만 모아서 보는 곳"

## 📋 프로젝트 개요

MyLitUK는 영국 문학 애호가들을 위한 개인화 큐레이션 플랫폼입니다.

### 핵심 기능
- ✅ **신간 알림**: 팔로우한 작가의 신간 출시 알림
- ✅ **행사 알림**: 관심있는 문학 행사 티켓 오픈 알림
- ✅ **문학상 알림**: 팔로우한 문학상의 발표 소식
- ✅ **다국어**: 영어/한국어 지원
- ✅ **100% 무료**: 사용자 5,000명까지 무료 운영

---

## 🚀 빠른 시작

### 필수 요구사항
```bash
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis (선택)
```

### 1. 저장소 클론
```bash
git clone https://github.com/bubilife1202/MyLitUK.git
cd MyLitUK
```

### 2. 백엔드 설정
```bash
cd backend

# 가상환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env
# .env 파일을 열어서 DATABASE_URL 등 설정

# 데이터베이스 마이그레이션
alembic upgrade head

# 서버 실행
uvicorn app.main:app --reload
```

서버가 http://localhost:8000 에서 실행됩니다.
API 문서: http://localhost:8000/docs

### 3. 프론트엔드 설정
```bash
cd frontend

# 의존성 설치
npm install

# 환경 변수 설정
cp .env.example .env.local
# NEXT_PUBLIC_API_URL=http://localhost:8000

# 개발 서버 실행
npm run dev
```

프론트엔드가 http://localhost:3000 에서 실행됩니다.

---

## 📁 프로젝트 구조

```
MyLitUK/
├── backend/                    # FastAPI 백엔드
│   ├── app/
│   │   ├── api/               # API 라우터
│   │   ├── models/            # SQLAlchemy 모델
│   │   ├── schemas/           # Pydantic 스키마
│   │   ├── core/              # 설정, 데이터베이스
│   │   ├── services/          # 비즈니스 로직
│   │   └── main.py            # FastAPI 앱
│   ├── alembic/               # 데이터베이스 마이그레이션
│   └── requirements.txt
│
├── frontend/                   # Next.js 프론트엔드
│   ├── app/
│   │   └── [locale]/          # 다국어 라우팅
│   ├── components/            # React 컴포넌트
│   ├── lib/                   # 유틸리티
│   ├── messages/              # 다국어 번역
│   │   ├── en.json
│   │   └── ko.json
│   └── package.json
│
├── scripts/                    # 크롤링, 자동화
│   ├── scrape_events.py
│   ├── scrape_awards.py
│   └── check_new_books.py
│
├── .github/
│   └── workflows/             # GitHub Actions
│
└── docs/                       # 기획 문서
    ├── PLANNING.md
    ├── MULTILINGUAL_SUPPORT.md
    └── 100_PERCENT_FREE_ARCHITECTURE.md
```

---

## 🛠️ 기술 스택

### Backend
- **FastAPI** - 빠르고 현대적인 Python 웹 프레임워크
- **SQLAlchemy** - ORM
- **PostgreSQL** - 데이터베이스
- **Redis** - 캐싱 (선택)
- **Alembic** - 데이터베이스 마이그레이션

### Frontend
- **Next.js 14** - React 프레임워크
- **TypeScript** - 타입 안전성
- **Tailwind CSS** - 스타일링
- **next-intl** - 다국어 지원

### Infrastructure (100% 무료!)
- **Vercel** - 프론트엔드 호스팅
- **Render.com** - 백엔드 호스팅
- **Supabase** - PostgreSQL 데이터베이스
- **Upstash** - Redis
- **GitHub Actions** - 자동화

---

## 🗄️ 데이터베이스 스키마

주요 테이블:
- `users` - 사용자
- `authors` - 작가
- `books` - 도서
- `events` - 행사
- `literary_awards` - 문학상
- `notifications` - 알림
- `user_author_follows` - 작가 팔로우
- `user_event_follows` - 행사 팔로우
- `user_award_follows` - 문학상 팔로우

상세 스키마: [PLANNING.md](PLANNING.md#데이터베이스-스키마-설계)

---

## 🔑 API 엔드포인트

### 인증
```
POST   /api/auth/register      # 회원가입
POST   /api/auth/login         # 로그인
GET    /api/auth/me            # 내 정보
```

### 작가
```
GET    /api/authors            # 작가 목록
GET    /api/authors/:id        # 작가 상세
POST   /api/authors/:id/follow # 팔로우
```

### 대시보드 (핵심!)
```
GET    /api/dashboard          # 개인화 피드
  → 내가 팔로우한 것의 최신 업데이트
```

### 알림
```
GET    /api/notifications      # 알림 목록
GET    /api/notifications/count # 안 읽은 개수
```

전체 API: http://localhost:8000/docs

---

## 🌍 다국어 지원

영어와 한국어를 지원합니다.

### 사용 방법
1. 헤더의 언어 선택 버튼 클릭 `[EN ▼]`
2. English 또는 한국어 선택
3. 전체 UI 즉시 변경

### 번역 추가
```json
// frontend/messages/ko.json
{
  "header": {
    "home": "홈",
    "events": "행사"
  }
}
```

상세 가이드: [MULTILINGUAL_SUPPORT.md](MULTILINGUAL_SUPPORT.md)

---

## 🤖 데이터 수집 자동화

GitHub Actions로 매일 자동 실행:

```bash
# 로컬 테스트
python scripts/check_new_books.py
python scripts/scrape_events.py
python scripts/scrape_awards.py
```

상세: [FREE_DATA_SOURCES.md](FREE_DATA_SOURCES.md)

---

## 🚀 배포

**완전한 배포 가이드**: [DEPLOYMENT.md](DEPLOYMENT.md)

### 빠른 배포 요약

#### 1. Supabase (Database)
1. supabase.com → 새 프로젝트 생성
2. DATABASE_URL 복사

#### 2. Render (Backend)
```bash
# Render.com에서:
- New Web Service 선택
- GitHub 저장소 연결
- Root Directory: backend
- Build: pip install -r requirements.txt
- Start: uvicorn app.main:app --host 0.0.0.0 --port $PORT
- 환경 변수 설정 (DATABASE_URL, SECRET_KEY)
```

#### 3. Vercel (Frontend)
```bash
# Vercel CLI 또는 웹에서:
npm i -g vercel
cd frontend
vercel
# 환경 변수: NEXT_PUBLIC_API_URL=https://your-backend.onrender.com
```

### 무료 호스팅 전략
상세 가이드: [100_PERCENT_FREE_ARCHITECTURE.md](100_PERCENT_FREE_ARCHITECTURE.md)

---

## 📈 개발 진행률

### ✅ 완료 (Phase 1 & 2)
- [x] 전체 시스템 기획
- [x] 데이터베이스 설계 (14개 테이블)
- [x] API 설계
- [x] 다국어 지원 설계
- [x] 무료 호스팅 전략
- [x] **FastAPI 백엔드 완전 구현**
  - [x] 인증 시스템 (JWT)
  - [x] 7개 API 라우터 (auth, authors, books, events, awards, notifications, dashboard)
  - [x] Follow/Unfollow 기능
  - [x] 개인화 대시보드 (핵심 기능!)
  - [x] 14개 SQLAlchemy 모델
  - [x] Pydantic 스키마
- [x] **Next.js 프론트엔드 완전 구현**
  - [x] TypeScript + Tailwind CSS
  - [x] next-intl 다국어 지원 (EN/KO)
  - [x] 홈, 로그인, 회원가입, 대시보드 페이지
  - [x] API 클라이언트
  - [x] 상태 관리 (Zustand)

### ⏳ 예정 (Phase 3 - 배포)
- [ ] Vercel 프론트엔드 배포
- [ ] Render 백엔드 배포
- [ ] Supabase 데이터베이스 설정
- [ ] 초기 데이터 입력 (작가, 이벤트, 문학상)
- [ ] 데이터 수집 스크립트
- [ ] GitHub Actions 자동화 설정

---

## 📝 개발 가이드

### 1. 새 API 추가
```python
# backend/app/api/new_endpoint.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db

router = APIRouter()

@router.get("/")
async def get_items(db: Session = Depends(get_db)):
    return {"items": []}
```

### 2. 새 컴포넌트 추가
```tsx
// frontend/components/NewComponent.tsx
import { useTranslations } from 'next-intl';

export function NewComponent() {
  const t = useTranslations('componentName');
  return <div>{t('title')}</div>;
}
```

### 3. 데이터베이스 마이그레이션
```bash
# 마이그레이션 생성
alembic revision --autogenerate -m "add new table"

# 적용
alembic upgrade head
```

---

## 🐛 문제 해결

### Backend 실행 안 됨
```bash
# PostgreSQL 확인
psql -U postgres

# 데이터베이스 생성
CREATE DATABASE mylituk;

# 마이그레이션
alembic upgrade head
```

### Frontend 실행 안 됨
```bash
# 캐시 삭제
rm -rf .next node_modules
npm install
npm run dev
```

---

## 📚 문서

- [배포 가이드](DEPLOYMENT.md) - **완전한 배포 가이드 (Vercel + Render + Supabase)**
- [전체 기획서](PLANNING.md) - 프로젝트 전체 설계
- [무료 아키텍처](100_PERCENT_FREE_ARCHITECTURE.md) - 무료 호스팅 전략
- [다국어 지원](MULTILINGUAL_SUPPORT.md) - i18n 가이드
- [데이터 소스](FREE_DATA_SOURCES.md) - API 및 크롤링
- [단순화 컨셉](SIMPLIFIED_CONCEPT.md) - 핵심 아이디어
- [마이그레이션 가이드](backend/MIGRATION_GUIDE.md) - 데이터베이스 마이그레이션

---

## 💰 비용

**완전 무료 운영 가능! (사용자 5,000명까지)**

- Vercel: $0
- Render: $0
- Supabase: $0
- Upstash: $0
- GitHub Actions: $0

**총: $0/월** 🎉

---

## 🤝 기여

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

---

## 📄 라이선스

MIT License

---

## 👤 제작

**MyLitUK** - 영국 문학 개인화 큐레이션 플랫폼

v3.1 - 다국어 지원 (2025-10-24)
