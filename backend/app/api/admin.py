from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
import subprocess
import os

router = APIRouter()

@router.post("/seed")
async def seed_database(db: Session = Depends(get_db)):
    """데이터베이스에 샘플 데이터 추가 (개발용)"""
    try:
        # seed_data.py 실행
        seed_script = os.path.join(os.path.dirname(__file__), "..", "..", "seed_data.py")
        result = subprocess.run(["python", seed_script], capture_output=True, text=True)

        if result.returncode == 0:
            return {
                "message": "Sample data seeded successfully",
                "output": result.stdout
            }
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Seed failed: {result.stderr}"
            )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error seeding database: {str(e)}"
        )
