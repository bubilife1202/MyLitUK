"""
MyLitUK Backend API
FastAPI application entry point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# Import routers (will be created later)
# from app.api import auth, authors, books, events, awards, notifications

# App metadata
APP_VERSION = "0.1.0"
APP_TITLE = "MyLitUK API"
APP_DESCRIPTION = """
MyLitUK - Personalized UK Literature Platform

## Features

* 📚 **Authors & Books**: Follow your favorite UK authors and get notified of new releases
* 🎭 **Literary Events**: Never miss tickets for Hay Festival, Edinburgh Book Festival, etc.
* 🏆 **Literary Awards**: Track Booker Prize, Women's Prize, and more
* 🌍 **Multilingual**: English and Korean support
* 🆓 **100% Free**: Completely free to use!

## Core Endpoints

* `/auth` - Authentication (register, login)
* `/authors` - Authors management
* `/books` - Books catalog
* `/events` - Literary events
* `/awards` - Literary awards
* `/dashboard` - Personalized feed
* `/notifications` - User notifications
"""

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup and shutdown events
    """
    # Startup
    print("🚀 Starting MyLitUK API...")
    print(f"📍 Version: {APP_VERSION}")
    print(f"🌐 Environment: Development")

    yield

    # Shutdown
    print("👋 Shutting down MyLitUK API...")

# Create FastAPI app
app = FastAPI(
    title=APP_TITLE,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js dev server
        "http://localhost:3001",
        "https://*.vercel.app",    # Vercel preview/production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Root endpoint
@app.get("/")
async def root():
    """
    Root endpoint - API info
    """
    return {
        "message": "Welcome to MyLitUK API!",
        "version": APP_VERSION,
        "docs": "/docs",
        "status": "running"
    }


# Health check
@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring
    """
    return {
        "status": "healthy",
        "version": APP_VERSION
    }


# Include routers (will be uncommented as we create them)
# app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
# app.include_router(authors.router, prefix="/api/authors", tags=["Authors"])
# app.include_router(books.router, prefix="/api/books", tags=["Books"])
# app.include_router(events.router, prefix="/api/events", tags=["Events"])
# app.include_router(awards.router, prefix="/api/awards", tags=["Awards"])
# app.include_router(notifications.router, prefix="/api/notifications", tags=["Notifications"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
