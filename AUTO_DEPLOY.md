# MyLitUK - 완전 자동 배포 가이드

이 가이드를 따라하면 **3단계 (약 10분)**만에 MyLitUK이 완전히 작동합니다!

---

## 🚀 1단계: 백엔드 자동 배포 (5분)

### Vercel에 백엔드 배포

1. 아래 버튼 클릭:

   [![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/bubilife1202/MyLitUK&project-name=mylituk-api&repository-name=mylituk-api)

2. **GitHub 계정으로 로그인**

3. **Import Git Repository** 화면에서:
   - Repository Name: `mylituk-api` (자동 입력됨)
   - **Import** 버튼 클릭

4. **Configure Project** 화면에서:
   - Framework Preset: `Other` 선택
   - Root Directory: **그대로 두기** (루트)
   - Build Command: `chmod +x build.sh && ./build.sh`
   - Output Directory: `api`

5. **Environment Variables** 섹션에서 추가:
   ```
   Name: SECRET_KEY
   Value: my-super-secret-key-change-this-in-production-12345
   ```
   > 나중에 더 안전한 키로 변경하세요

6. **Deploy** 버튼 클릭

7. **배포 완료 대기** (5-7분)
   - 배포가 완료되면 URL이 표시됩니다
   - 예: `https://mylituk-api-xxxxxxx.vercel.app`
   - **이 URL을 복사하세요!** 📋

---

## ✅ 2단계: 백엔드 테스트 (1분)

배포된 백엔드가 작동하는지 확인:

1. 브라우저에서 다음 URL 열기:
   ```
   https://your-api-url.vercel.app/docs
   ```
   (your-api-url을 1단계에서 받은 URL로 변경)

2. API 문서가 표시되면 성공! ✨

---

## 🔗 3단계: 프론트엔드와 백엔드 연결 (3분)

### Netlify 환경 변수 설정

1. https://app.netlify.com 접속

2. **mylituk** 사이트 선택

3. **Site settings** 클릭

4. 왼쪽 메뉴에서 **Environment variables** 클릭

5. **Add a variable** 버튼 클릭

6. 다음 입력:
   - **Key**: `NEXT_PUBLIC_API_URL`
   - **Value**: `https://your-api-url.vercel.app` (1단계의 URL)
   - **Values**: `All scopes` 선택
   - **Add variable** 클릭

7. 상단의 **Deploys** 탭으로 이동

8. **Trigger deploy** 버튼 클릭 > **Deploy site** 선택

9. **배포 완료 대기** (2-3분)

---

## 🎉 완료!

모든 설정이 완료되었습니다!

### 사이트 접속

https://mylituk.netlify.app 에서 회원가입과 로그인이 정상 작동합니다!

### 데모 계정

백엔드에 자동으로 생성된 데모 계정:
- **Email**: demo@mylituk.com
- **Password**: demo1234

---

## 📊 배포된 내용

✅ **백엔드 (Vercel)**:
- FastAPI 서버
- SQLite 데이터베이스
- 샘플 데이터 (작가 5명, 책 3권, 이벤트 3개, 어워드 3개)
- JWT 인증 시스템
- REST API

✅ **프론트엔드 (Netlify)**:
- Next.js 14 (App Router)
- 다국어 지원 (EN/KO)
- 반응형 디자인
- 실시간 알림

---

## ⚠️ 무료 플랜 참고사항

### Vercel 무료 플랜:
- 월 100GB 대역폭
- 100시간 실행 시간
- 10초 함수 실행 시간 제한

### Netlify 무료 플랜:
- 월 100GB 대역폭
- 월 300분 빌드 시간

---

## 🔧 문제 해결

### 회원가입 시 오류 발생
1. Netlify 환경 변수가 올바르게 설정되었는지 확인
2. 백엔드 URL 끝에 `/` 없는지 확인 (예: ~~https://api.com/~~)
3. Netlify를 재배포

### 백엔드 500 오류
1. Vercel 대시보드 > mylituk-api > Functions 탭
2. 최근 로그 확인
3. 환경 변수 `SECRET_KEY`가 설정되었는지 확인

### API 문서가 안 보임
1. Vercel 배포가 완료되었는지 확인
2. URL에 `/docs` 경로가 정확한지 확인

---

## 🚀 다음 단계

### 프로덕션 준비

1. **SECRET_KEY 변경**:
   - Vercel > mylituk-api > Settings > Environment Variables
   - SECRET_KEY를 더 안전한 값으로 변경

2. **PostgreSQL 사용** (선택사항):
   - SQLite는 재배포 시 데이터 손실
   - Vercel Postgres 또는 Supabase 연결 권장

3. **도메인 연결** (선택사항):
   - Netlify와 Vercel 모두 커스텀 도메인 지원
   - 예: mylituk.com

---

## 📚 추가 리소스

- [Vercel 문서](https://vercel.com/docs)
- [Netlify 문서](https://docs.netlify.com)
- [FastAPI 문서](https://fastapi.tiangolo.com)
- [Next.js 문서](https://nextjs.org/docs)

---

**축하합니다! 🎊 MyLitUK이 성공적으로 배포되었습니다!**
