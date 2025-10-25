# Netlify 배포 가이드

mylituk.netlify.app이 제대로 작동하도록 설정하는 방법입니다.

## 문제 해결

**아무것도 안 나올 때:**

1. **Netlify 대시보드 확인**
   - https://app.netlify.com 로그인
   - 사이트 선택 → "Site configuration" → "Build & deploy"

2. **빌드 설정 확인**
   ```
   Base directory: frontend
   Build command: npm install && npm run build
   Publish directory: frontend/.next
   ```

3. **환경 변수 설정**
   - "Site configuration" → "Environment variables" → "Add a variable"
   - 이름: `NEXT_PUBLIC_API_URL`
   - 값: `http://localhost:8000` (또는 배포된 백엔드 URL)

4. **재배포**
   - "Deploys" 탭 → "Trigger deploy" → "Deploy site"

## 자동 배포 설정 (권장)

### 방법 1: Git Push로 자동 배포

netlify.toml 파일이 있으므로 git push만 하면 자동 배포됩니다:

```bash
git add .
git commit -m "Add Netlify configuration"
git push
```

Netlify가 자동으로 감지하고 빌드를 시작합니다!

### 방법 2: Netlify 대시보드에서 수동 배포

1. Netlify 대시보드 → 사이트 선택
2. "Deploys" 탭
3. "Trigger deploy" → "Deploy site"

## 빌드 로그 확인

배포가 실패하면:

1. Netlify 대시보드 → "Deploys"
2. 최신 배포 클릭
3. "Deploy log" 보기
4. 에러 메시지 확인

**일반적인 에러:**

### 에러 1: "Module not found"
```bash
# 해결: package.json에 패키지 추가 확인
cd frontend
npm install
```

### 에러 2: "Build command failed"
```bash
# 해결: 로컬에서 빌드 테스트
cd frontend
npm run build
```

### 에러 3: "Page not found (404)"
이는 Next.js 라우팅 문제입니다.
- netlify.toml의 리다이렉트 설정이 있어야 합니다
- 이미 추가되어 있으니 재배포하세요

## 빠른 체크리스트

✅ **Netlify에서 확인할 사항:**

1. **Site settings → Build & deploy → Build settings**
   - [ ] Base directory: `frontend`
   - [ ] Build command: `npm install && npm run build`
   - [ ] Publish directory: `frontend/.next`

2. **Site settings → Environment variables**
   - [ ] `NEXT_PUBLIC_API_URL` 설정됨
   - [ ] `NODE_VERSION` = `18` (선택사항, netlify.toml에 있음)

3. **Deploys 탭**
   - [ ] 최신 배포가 "Published" 상태
   - [ ] 에러 없음

## 테스트

배포 후 테스트:

1. **홈페이지 확인**
   ```
   https://mylituk.netlify.app
   ```
   → "MyLitUK" 타이틀과 Hero 섹션이 보여야 합니다

2. **언어 전환 테스트**
   ```
   https://mylituk.netlify.app/en
   https://mylituk.netlify.app/ko
   ```
   → 영어/한국어로 전환되어야 합니다

3. **페이지 라우팅 테스트**
   ```
   https://mylituk.netlify.app/en/login
   https://mylituk.netlify.app/ko/register
   ```
   → 404 에러 없이 페이지가 로드되어야 합니다

## 백엔드 연결 (선택사항)

현재는 프론트엔드만 배포된 상태입니다. 백엔드를 연결하려면:

1. **백엔드 먼저 배포** (Render.com 권장)
   - `DEPLOYMENT.md` 참고

2. **Netlify 환경 변수 업데이트**
   ```
   NEXT_PUBLIC_API_URL=https://your-backend.onrender.com
   ```

3. **재배포**
   - Netlify에서 자동으로 재배포되거나
   - "Trigger deploy" 클릭

## 도메인 설정 (선택사항)

커스텀 도메인 사용하려면:

1. Netlify 대시보드 → "Domain management"
2. "Add custom domain"
3. 도메인 입력 (예: mylituk.com)
4. DNS 설정 안내 따라하기

## 문제가 계속되면

1. **netlify.toml 파일 확인**
   ```bash
   cat netlify.toml
   ```

2. **로컬에서 빌드 테스트**
   ```bash
   cd frontend
   npm run build
   npm start
   ```

3. **Netlify 서포트 문서**
   - https://docs.netlify.com/frameworks/next-js/overview/

4. **빌드 로그 확인**
   - Netlify 대시보드에서 자세한 에러 메시지 확인

## 성공 확인

배포가 성공하면:
- ✅ mylituk.netlify.app에 접속 가능
- ✅ 홈페이지가 제대로 표시됨
- ✅ 언어 전환 작동
- ✅ 로그인/회원가입 페이지 접근 가능

이제 git push만 하면 자동으로 배포됩니다! 🎉
