"""
WSGI configuration for PythonAnywhere deployment
FastAPI를 WSGI로 감싸서 PythonAnywhere에서 실행
"""
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
