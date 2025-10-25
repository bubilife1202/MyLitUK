# MyLitUK - 백엔드 배포 (초간단 버전)

## 🚀 원클릭 배포

아래 버튼을 클릭하면 자동으로 백엔드가 배포됩니다:

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/bubilife1202/MyLitUK)

## 배포 후 할 일

### 1단계: 배포 버튼 클릭
위 "Deploy to Render" 버튼 클릭 → GitHub 로그인 → 자동 배포 시작

### 2단계: 환경 변수 확인
자동으로 설정되지만, 확인:
- `DATABASE_URL`: `sqlite:///./mylituk.db` (자동)
- `SECRET_KEY`: 자동 생성됨
- `ALLOWED_ORIGINS`: `https://mylituk.netlify.app,http://localhost:3000` (자동)

### 3단계: 배포 완료 기다리기 (5-10분)
배포가 완료되면 URL이 생성됩니다 (예: `https://mylituk-api.onrender.com`)

### 4단계: Shell에서 데이터베이스 초기화

Render 대시보드에서:
1. 배포된 서비스 클릭
2. "Shell" 탭 클릭
3. 다음 명령어 실행:

```bash
# 테이블 생성
python -c "from app.core.database import Base, engine; Base.metadata.create_all(bind=engine)"

# 샘플 데이터 추가
python seed_data.py
```

### 5단계: Netlify 환경 변수 설정

**이 부분만 수동으로 해주세요:**

1. https://app.netlify.com 접속
2. mylituk 사이트 선택
3. `Site settings` > `Environment variables` 클릭
4. `Add a variable` 클릭
5. 다음 입력:
   - **Key**: `NEXT_PUBLIC_API_URL`
   - **Value**: `https://your-app-name.onrender.com` (4단계에서 받은 URL)
6. `Save` 클릭
7. `Deploys` 탭 > `Trigger deploy` > `Clear cache and deploy site`

## ✅ 완료!

약 2-3분 후 https://mylituk.netlify.app 에서 회원가입이 정상 작동합니다!

## 데모 계정
- Email: demo@mylituk.com
- Password: demo1234

## 무료 플랜 참고사항
- 15분간 요청 없으면 sleep (첫 요청 시 30초 대기)
- 750시간/월 무료
