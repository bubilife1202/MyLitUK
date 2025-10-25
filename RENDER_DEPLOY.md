# Render.com 백엔드 배포 가이드

## 1단계: Render 계정 생성

1. https://render.com 접속
2. GitHub 계정으로 로그인
3. bubilife1202/MyLitUK 저장소 접근 권한 허용

## 2단계: 새 Web Service 생성

1. Dashboard에서 "New +" 버튼 클릭
2. "Web Service" 선택
3. MyLitUK 저장소 선택
4. 다음 설정 입력:

### 기본 설정
- **Name**: `mylituk-api`
- **Region**: Oregon (US West) - 무료
- **Branch**: `claude/add-event-award-alerts-011CUSghoXR5QUSyqLWKyYKA`
- **Root Directory**: `backend`
- **Runtime**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 환경 변수 설정 (Environment Variables)
다음 환경 변수를 추가:

```
DATABASE_URL=sqlite:///./mylituk.db
SECRET_KEY=your-super-secret-key-here-change-this
ALLOWED_ORIGINS=https://mylituk.netlify.app,http://localhost:3000
```

### 플랜 선택
- **Instance Type**: Free

## 3단계: 배포

1. "Create Web Service" 클릭
2. 배포가 시작됩니다 (약 5-10분 소요)
3. 배포 완료 후 URL 확인 (예: `https://mylituk-api.onrender.com`)

## 4단계: 데이터베이스 초기화

배포 완료 후, Render 콘솔에서 다음 명령 실행:

### Shell 접속
1. 서비스 페이지에서 "Shell" 탭 클릭
2. 다음 명령 실행:

```bash
# 데이터베이스 테이블 생성
python -c "from app.core.database import Base, engine; Base.metadata.create_all(bind=engine)"

# 샘플 데이터 추가
python seed_data.py
```

## 5단계: API 테스트

배포된 API URL로 테스트:

```bash
# Health check
curl https://mylituk-api.onrender.com/health

# API 문서 확인
https://mylituk-api.onrender.com/docs
```

## 6단계: Netlify 환경 변수 업데이트

1. Netlify Dashboard 접속 (https://app.netlify.com)
2. mylituk 사이트 선택
3. "Site settings" > "Environment variables" 클릭
4. 새 변수 추가:
   - **Key**: `NEXT_PUBLIC_API_URL`
   - **Value**: `https://mylituk-api.onrender.com` (실제 Render URL로 변경)
5. "Save" 클릭
6. "Deploys" 탭에서 "Trigger deploy" > "Clear cache and deploy site"

## 주의사항

### 무료 플랜 제한사항
- 15분 동안 요청이 없으면 자동으로 sleep 상태가 됩니다
- Sleep 상태에서 첫 요청 시 약 30초-1분 정도 깨어나는 시간이 필요합니다
- 750시간/월 무료 (충분함)
- SQLite 사용 시 재배포하면 데이터가 초기화됩니다

### SQLite 데이터 유지
무료 플랜에서 데이터를 유지하려면:
1. PostgreSQL 무료 데이터베이스 사용 (Render 제공)
2. 또는 데이터를 정기적으로 백업

## 문제 해결

### 빌드 실패
- Logs 탭에서 오류 확인
- requirements.txt 파일 확인
- Python 버전 확인 (3.11 사용)

### 500 에러
- Logs에서 백엔드 오류 확인
- 환경 변수가 올바르게 설정되었는지 확인
- DATABASE_URL이 정확한지 확인

### CORS 오류
- ALLOWED_ORIGINS에 Netlify URL이 포함되었는지 확인
- https://mylituk.netlify.app (프로토콜 포함)

## 데모 계정

백엔드 배포 후 seed_data.py로 생성된 데모 계정:
- **Email**: demo@mylituk.com
- **Password**: demo1234

## 다음 단계

배포가 완료되면:
1. https://mylituk.netlify.app 접속
2. 회원가입 또는 데모 계정으로 로그인
3. 정상 작동 확인
