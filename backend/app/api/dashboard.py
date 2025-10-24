from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db

router = APIRouter()

@router.get("")
async def get_dashboard(db: Session = Depends(get_db)):
    """Get personalized dashboard feed"""
    # This is the core feature!
    # Returns updates from followed authors, events, awards
    return {
        "message": "Personalized dashboard - to be implemented",
        "updates": []
    }

@router.get("/today")
async def get_today_updates(db: Session = Depends(get_db)):
    """Get today's updates"""
    return {"updates": []}
