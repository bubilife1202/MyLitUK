#!/bin/bash

# PythonAnywhere 자동 배포 스크립트
# PythonAnywhere Bash 콘솔에서 실행하세요

echo "======================================"
echo "MyLitUK 백엔드 배포 시작"
echo "======================================"

# 1. 저장소 클론
echo ""
echo "[1/5] GitHub 저장소 클론 중..."
cd ~
if [ -d "MyLitUK" ]; then
    echo "기존 디렉토리 발견. 업데이트 중..."
    cd MyLitUK
    git pull origin claude/add-event-award-alerts-011CUSghoXR5QUSyqLWKyYKA
else
    git clone -b claude/add-event-award-alerts-011CUSghoXR5QUSyqLWKyYKA https://github.com/bubilife1202/MyLitUK.git
    cd MyLitUK
fi

# 2. 가상 환경 생성
echo ""
echo "[2/5] 가상 환경 생성 중..."
if [ ! -d "venv" ]; then
    python3.10 -m venv venv
fi
source venv/bin/activate

# 3. 의존성 설치
echo ""
echo "[3/5] 패키지 설치 중..."
pip install --upgrade pip
pip install -r backend/requirements.txt

# 4. 데이터베이스 초기화
echo ""
echo "[4/5] 데이터베이스 초기화 중..."
cd backend
python -c "from app.core.database import Base, engine; Base.metadata.create_all(bind=engine)"
python seed_data.py
cd ..

# 5. WSGI 파일 복사
echo ""
echo "[5/5] WSGI 설정 파일 준비 중..."
USERNAME=$(whoami)
sed "s/YOUR_USERNAME/$USERNAME/g" pythonanywhere_wsgi.py > ~/mysite_wsgi.py

echo ""
echo "======================================"
echo "✅ 배포 완료!"
echo "======================================"
echo ""
echo "다음 단계:"
echo "1. PythonAnywhere 웹 인터페이스에서 Web 탭 클릭"
echo "2. 'Add a new web app' 클릭"
echo "3. Manual configuration → Python 3.10 선택"
echo "4. WSGI configuration file 경로를 다음으로 변경:"
echo "   /home/$USERNAME/mysite_wsgi.py"
echo "5. Reload 버튼 클릭"
echo ""
echo "백엔드 URL: https://$USERNAME.pythonanywhere.com"
echo "======================================"
