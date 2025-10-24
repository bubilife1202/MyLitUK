from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db

router = APIRouter()

@router.get("")
async def list_awards(db: Session = Depends(get_db)):
    """List literary awards"""
    return {"message": "Awards endpoint - to be implemented"}

@router.get("/{award_id}")
async def get_award(award_id: int, db: Session = Depends(get_db)):
    """Get award details"""
    return {"message": f"Award {award_id} - to be implemented"}
