from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import auth, authors, books, events, awards, notifications, dashboard, admin
from app.core.database import Base, engine
import os
import subprocess

app = FastAPI(
    title="MyLitUK API",
    description="Personalized UK Literature Curation Platform",
    version="3.1.0"
)

@app.on_event("startup")
async def startup_event():
    """서버 시작 시 데이터베이스 초기화"""
    # 테이블 생성
    Base.metadata.create_all(bind=engine)

    # seed_data.py 무조건 실행 (Render는 매번 초기화됨)
    seed_script = os.path.join(os.path.dirname(__file__), "..", "seed_data.py")
    if os.path.exists(seed_script):
        try:
            result = subprocess.run(
                ["python", seed_script],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                print("✅ Sample data seeded successfully")
            else:
                print(f"⚠️ Seed data error: {result.stderr}")
        except Exception as e:
            print(f"⚠️ Could not seed data: {e}")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 등록
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(authors.router, prefix="/api/authors", tags=["Authors"])
app.include_router(books.router, prefix="/api/books", tags=["Books"])
app.include_router(events.router, prefix="/api/events", tags=["Events"])
app.include_router(awards.router, prefix="/api/awards", tags=["Awards"])
app.include_router(notifications.router, prefix="/api/notifications", tags=["Notifications"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])

@app.get("/")
async def root():
    return {
        "message": "MyLitUK API v3.1",
        "docs": "/docs",
        "features": [
            "Personalized curation",
            "Event & award alerts",
            "Multilingual (EN/KO)"
        ]
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
