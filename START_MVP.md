# 🚀 MyLitUK MVP 빠른 시작 가이드

## 1단계: 백엔드 설정 및 실행 (5분)

### 백엔드 디렉토리로 이동
```bash
cd backend
```

### Python 가상환경 생성 및 활성화
```bash
python -m venv venv

# Mac/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

### 패키지 설치
```bash
pip install -r requirements.txt
```

### 샘플 데이터 생성 (SQLite 사용)
```bash
# .env.local 파일 사용 (SQLite)
cp .env.local .env

# 샘플 데이터 추가
python seed_data.py
```

이 명령어는 다음을 추가합니다:
- ✍️ 작가 5명 (Zadie Smith, Kazuo Ishiguro 등)
- 📚 책 3권
- 🎭 행사 3개 (Hay Festival, Edinburgh Book Festival 등)
- 🏆 문학상 3개 (Booker Prize, Women's Prize 등)
- 👤 테스트 계정 1개

**테스트 계정 정보:**
- 이메일: `demo@mylituk.com`
- 비밀번호: `demo1234`

### 백엔드 서버 실행
```bash
uvicorn app.main:app --reload
```

서버가 http://localhost:8000 에서 실행됩니다.
API 문서: http://localhost:8000/docs 에서 확인하세요!

---

## 2단계: 프론트엔드 실행 (5분)

### 새 터미널을 열고 프론트엔드로 이동
```bash
cd frontend
```

### 패키지 설치
```bash
npm install
```

### 환경 변수 설정
```bash
# .env.local 파일 생성
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
```

### 프론트엔드 실행
```bash
npm run dev
```

프론트엔드가 http://localhost:3000 에서 실행됩니다!

---

## 3단계: MVP 테스트하기

### 1. 로그인하기
1. 브라우저에서 http://localhost:3000 열기
2. 우측 상단 "Login" 클릭
3. 테스트 계정으로 로그인:
   - 이메일: `demo@mylituk.com`
   - 비밀번호: `demo1234`

### 2. 대시보드 보기
로그인 후 자동으로 대시보드로 이동합니다.
- 아직 팔로우한 작가/행사/문학상이 없어서 비어있습니다.

### 3. 작가 팔로우하기 (API로 테스트)
http://localhost:8000/docs 에서:

1. `/api/auth/login` 엔드포인트로 로그인해서 토큰 받기
2. 우측 상단 "Authorize" 클릭하고 토큰 입력
3. `/api/authors` 로 작가 목록 보기
4. `/api/authors/{id}/follow` 로 작가 팔로우하기 (예: id=1)
5. 다시 대시보드 새로고침 → 팔로우한 작가 정보 표시!

### 4. 언어 변경하기
- 우측 상단 언어 선택기로 English ↔ 한국어 전환
- 모든 UI 텍스트가 즉시 변경됩니다!

---

## 빠른 명령어 모음

### 백엔드 다시 시작
```bash
cd backend
source venv/bin/activate  # 가상환경 활성화
uvicorn app.main:app --reload
```

### 프론트엔드 다시 시작
```bash
cd frontend
npm run dev
```

### 데이터 초기화 (처음부터 다시)
```bash
cd backend
rm mylituk.db  # SQLite 파일 삭제
python seed_data.py  # 샘플 데이터 재생성
```

---

## 문제 해결

### 백엔드가 실행 안 됨
```bash
# Python 버전 확인 (3.11+ 필요)
python --version

# 패키지 재설치
pip install --upgrade -r requirements.txt
```

### 프론트엔드가 실행 안 됨
```bash
# Node 버전 확인 (18+ 필요)
node --version

# 캐시 삭제 후 재설치
rm -rf node_modules .next
npm install
```

### "Module not found" 오류
```bash
# backend 폴더에서:
pip install -r requirements.txt

# frontend 폴더에서:
npm install
```

---

## MVP에 포함된 기능

✅ **사용자 인증**
- 회원가입
- 로그인
- JWT 토큰 인증

✅ **작가 관리**
- 작가 목록 보기
- 작가 상세 정보
- 작가 팔로우/언팔로우

✅ **책 정보**
- 책 목록 보기
- 책 상세 정보

✅ **행사 관리**
- 행사 목록 보기 (필터링)
- 행사 팔로우/언팔로우

✅ **문학상 관리**
- 문학상 목록 보기
- 문학상 팔로우/언팔로우

✅ **개인화 대시보드** (핵심!)
- 팔로우한 작가의 신간
- 팔로우한 행사 일정
- 팔로우한 문학상 발표

✅ **다국어 지원**
- 영어/한국어 전환
- 모든 UI 텍스트 번역

---

## 다음 단계

MVP를 테스트한 후:

1. **배포하기**: `DEPLOYMENT.md` 참고
2. **더 많은 데이터 추가**: seed_data.py 수정
3. **추가 페이지 구현**: 작가/행사/문학상 목록 페이지
4. **알림 시스템**: 자동 알림 생성 스크립트

---

## 도움말

- **전체 문서**: `README.md`
- **API 문서**: http://localhost:8000/docs
- **구현 상세**: `IMPLEMENTATION_SUMMARY.md`
- **배포 가이드**: `DEPLOYMENT.md`

즐거운 테스트 되세요! 🎉
