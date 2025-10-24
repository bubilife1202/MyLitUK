from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db

router = APIRouter()

@router.get("")
async def list_events(db: Session = Depends(get_db)):
    """List events"""
    return {"message": "Events endpoint - to be implemented"}

@router.get("/{event_id}")
async def get_event(event_id: int, db: Session = Depends(get_db)):
    """Get event details"""
    return {"message": f"Event {event_id} - to be implemented"}

@router.post("/{event_id}/follow")
async def follow_event(event_id: int, db: Session = Depends(get_db)):
    """Follow an event"""
    raise HTTPException(status_code=501, detail="Not implemented yet")
