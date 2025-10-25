#!/bin/bash

echo "🚀 MyLitUK MVP 빠른 시작"
echo "========================"
echo ""

# 색상 정의
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 백엔드 설정
echo -e "${BLUE}📦 백엔드 설정 중...${NC}"
cd backend

# 가상환경 확인
if [ ! -d "venv" ]; then
    echo "가상환경 생성 중..."
    python3 -m venv venv
fi

# 가상환경 활성화
source venv/bin/activate

# 패키지 설치 확인
if [ ! -f "venv/bin/uvicorn" ]; then
    echo "패키지 설치 중..."
    pip install -r requirements.txt
fi

# .env 파일 설정
if [ ! -f ".env" ]; then
    echo "환경 변수 설정 중..."
    cp .env.local .env
fi

# SQLite 데이터베이스 확인
if [ ! -f "mylituk.db" ]; then
    echo "샘플 데이터 생성 중..."
    python seed_data.py
fi

echo -e "${GREEN}✅ 백엔드 준비 완료!${NC}"
echo ""

# 백엔드 실행
echo -e "${BLUE}🚀 백엔드 서버 시작 중...${NC}"
echo "   → http://localhost:8000"
echo "   → API 문서: http://localhost:8000/docs"
echo ""

uvicorn app.main:app --reload
