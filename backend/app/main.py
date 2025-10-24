from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import auth, authors, books, events, awards, notifications, dashboard

app = FastAPI(
    title="MyLitUK API",
    description="Personalized UK Literature Curation Platform",
    version="3.1.0"
)

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
