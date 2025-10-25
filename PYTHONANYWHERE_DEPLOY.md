# MyLitUK - PythonAnywhere 무료 배포 가이드

## ✅ 완전 무료 (신용카드 불필요!)

이 가이드를 따라하면 **백엔드를 완전 무료로 배포**할 수 있습니다!

---

## 📋 1단계: PythonAnywhere 가입 (2분)

### 가입하기

1. https://www.pythonanywhere.com 접속
2. 우측 상단 **"Pricing & signup"** 클릭
3. **"Create a Beginner account"** 클릭 (완전 무료!)
4. 정보 입력:
   - Username: 원하는 이름 (예: `mylituk` 또는 본인 이름)
   - Email: 본인 이메일
   - Password: 비밀번호
5. **"Register"** 클릭
6. 이메일 확인 링크 클릭
7. ✅ 가입 완료!

**참고:** Username이 백엔드 URL이 됩니다
- 예: `mylituk` → `https://mylituk.pythonanywhere.com`

---

## 🚀 2단계: 자동 배포 스크립트 실행 (5분)

### Bash 콘솔 열기

1. PythonAnywhere 대시보드 접속 (로그인 후 자동으로 이동)
2. 상단 메뉴에서 **"Consoles"** 탭 클릭
3. **"Bash"** 클릭 (새 콘솔 열림)

### 배포 스크립트 실행

콘솔에 다음 명령어 **복사해서 붙여넣기**:

```bash
wget https://raw.githubusercontent.com/bubilife1202/MyLitUK/claude/add-event-award-alerts-011CUSghoXR5QUSyqLWKyYKA/deploy_pythonanywhere.sh
chmod +x deploy_pythonanywhere.sh
./deploy_pythonanywhere.sh
```

엔터 누르고 기다리기 (5분 정도 소요)

스크립트가 자동으로:
- ✅ GitHub에서 코드 다운로드
- ✅ 가상 환경 생성
- ✅ 패키지 설치
- ✅ 데이터베이스 생성 및 샘플 데이터 추가
- ✅ WSGI 설정 파일 준비

완료되면 메시지가 표시됩니다!

---

## 🌐 3단계: Web App 설정 (3분)

### Web App 생성

1. 상단 메뉴에서 **"Web"** 탭 클릭
2. **"Add a new web app"** 버튼 클릭
3. 도메인 이름 확인 → **"Next"** 클릭
4. **"Manual configuration"** 선택
5. **"Python 3.10"** 선택
6. **"Next"** 클릭
7. ✅ Web app 생성 완료!

### WSGI 파일 설정

화면 아래로 스크롤해서 **"Code"** 섹션:

1. **"WSGI configuration file"** 링크 클릭
   - 경로: `/var/www/YOUR_USERNAME_pythonanywhere_com_wsgi.py`
2. 에디터가 열리면 **모든 내용 삭제**
3. 다음 내용 복사해서 붙여넣기:

**⚠️ YOUR_USERNAME을 본인 username으로 변경하세요!**

```python
import sys
import os

# 프로젝트 경로 설정
project_home = '/home/YOUR_USERNAME/MyLitUK'
if project_home not in sys.path:
    sys.path.insert(0, project_home)
    sys.path.insert(0, os.path.join(project_home, 'backend'))

# 환경 변수 설정
os.environ['DATABASE_URL'] = 'sqlite:////home/YOUR_USERNAME/MyLitUK/mylituk.db'
os.environ['SECRET_KEY'] = 'your-secret-key-change-this-12345'
os.environ['ALLOWED_ORIGINS'] = 'https://mylituk.netlify.app,http://localhost:3000'

# FastAPI 앱 임포트
from app.main import app

# ASGI를 WSGI로 변환
from a2wsgi import ASGIMiddleware
application = ASGIMiddleware(app)
```

4. **"Save"** 버튼 클릭 (우측 상단)

### 가상 환경 설정

Web 탭으로 돌아가서:

1. **"Virtualenv"** 섹션 찾기
2. **"Enter path to a virtualenv"** 입력 필드에 입력:
   ```
   /home/YOUR_USERNAME/MyLitUK/venv
   ```
   (YOUR_USERNAME을 본인 username으로 변경)
3. 체크 버튼 클릭

### 앱 시작

1. 페이지 맨 위로 스크롤
2. 녹색 **"Reload YOUR_USERNAME.pythonanywhere.com"** 버튼 클릭
3. ✅ 배포 완료!

---

## 🧪 4단계: 테스트 (1분)

### API 확인

1. 브라우저 새 탭에서 접속:
   ```
   https://YOUR_USERNAME.pythonanywhere.com/docs
   ```
   (YOUR_USERNAME을 본인 username으로 변경)

2. API 문서가 표시되면 성공! ✨

### Health Check

```
https://YOUR_USERNAME.pythonanywhere.com/health
```

응답:
```json
{"status": "healthy"}
```

---

## 🔗 5단계: Netlify 연결 (2분)

### 환경 변수 설정

1. https://app.netlify.com 접속
2. **mylituk** 사이트 선택
3. **Site settings** → **Environment variables** 클릭
4. **Add a variable** 클릭
5. 입력:
   - **Key**: `NEXT_PUBLIC_API_URL`
   - **Value**: `https://YOUR_USERNAME.pythonanywhere.com`
   - **Scopes**: 모두 체크
6. **Create variable** 클릭

### 재배포

1. **Deploys** 탭 클릭
2. **Trigger deploy** → **Deploy site** 클릭
3. 2-3분 대기

---

## 🎉 완료!

https://mylituk.netlify.app 에서 회원가입이 정상 작동합니다!

### 데모 계정
- **Email**: demo@mylituk.com
- **Password**: demo1234

---

## ⚠️ 무료 플랜 제약사항

### 자동 Sleep (24시간 후)

PythonAnywhere 무료 플랜은 24시간마다 웹앱을 재시작해야 합니다.

**해결 방법:** 매일 자동 Reload 설정

1. PythonAnywhere 대시보드 → **Tasks** 탭
2. **"Create a new scheduled task"** 클릭
3. 입력:
   - **Hour**: `0` (UTC 기준 자정)
   - **Minute**: `0`
   - **Command**:
     ```bash
     /usr/local/bin/pa_reload_webapp.py YOUR_USERNAME.pythonanywhere.com
     ```
     (YOUR_USERNAME을 본인 username으로 변경)
4. **"Create"** 클릭

이제 매일 자동으로 웹앱이 재시작됩니다!

### 기타 제약

- CPU 제한: 100 CPU-seconds/day
- 디스크 용량: 512MB
- 외부 API 접근: 화이트리스트 도메인만 가능

하지만 MyLitUK은 이 제약 내에서 충분히 작동합니다! ✅

---

## 🔧 문제 해결

### "ImportError" 발생 시

1. **Web** 탭 → 우측 **Error log** 클릭
2. 오류 내용 확인
3. **Consoles** → **Bash** 열기
4. 다음 실행:
   ```bash
   cd ~/MyLitUK
   source venv/bin/activate
   pip install -r backend/requirements.txt
   ```
5. **Web** 탭에서 **Reload** 클릭

### 500 에러 발생 시

1. **Web** 탭 → **Error log** 확인
2. WSGI 파일의 경로가 정확한지 확인
3. Username이 올바른지 확인

### 데이터베이스 초기화 실패 시

**Bash** 콘솔에서:
```bash
cd ~/MyLitUK/backend
source ../venv/bin/activate
python -c "from app.core.database import Base, engine; Base.metadata.create_all(bind=engine)"
python seed_data.py
```

---

## 📊 백엔드 URL

백엔드가 배포된 URL:
```
https://YOUR_USERNAME.pythonanywhere.com
```

API 문서:
```
https://YOUR_USERNAME.pythonanywhere.com/docs
```

---

## 🎁 포함된 샘플 데이터

자동으로 생성된 데이터:
- ✅ 작가 5명 (Zadie Smith, Kazuo Ishiguro, Ian McEwan, Hilary Mantel, Bernardine Evaristo)
- ✅ 책 3권
- ✅ 이벤트 3개 (Hay Festival, Edinburgh Book Festival, London Book Fair)
- ✅ 어워드 3개 (Booker Prize, Women's Prize, Costa Book Awards)
- ✅ 데모 계정 1개

---

**축하합니다! 🎊**

완전 무료로 MyLitUK 백엔드를 배포했습니다!
