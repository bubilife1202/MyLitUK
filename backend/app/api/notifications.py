from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db

router = APIRouter()

@router.get("")
async def list_notifications(db: Session = Depends(get_db)):
    """Get user notifications"""
    return {"message": "Notifications endpoint - to be implemented"}

@router.get("/count")
async def get_unread_count(db: Session = Depends(get_db)):
    """Get unread notification count"""
    return {"count": 0}

@router.put("/{notification_id}/read")
async def mark_as_read(notification_id: int, db: Session = Depends(get_db)):
    """Mark notification as read"""
    return {"message": "Marked as read"}
