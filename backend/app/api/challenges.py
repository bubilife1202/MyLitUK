from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from typing import List, Optional
from datetime import datetime

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.reading import ReadingChallenge, UserBookList
from pydantic import BaseModel, Field


router = APIRouter(prefix="/api/challenges", tags=["Reading Challenges"])


# Schemas
class ChallengeCreate(BaseModel):
    year: int = Field(..., ge=2020, le=2030)
    goal_count: int = Field(..., ge=1, le=1000)


class ChallengeUpdate(BaseModel):
    goal_count: Optional[int] = Field(None, ge=1, le=1000)
    is_active: Optional[bool] = None


class ChallengeResponse(BaseModel):
    id: int
    year: int
    goal_count: int
    current_count: int
    percentage: float
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Endpoints
@router.post("", response_model=ChallengeResponse, status_code=status.HTTP_201_CREATED)
async def create_challenge(
    data: ChallengeCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """독서 챌린지 생성"""
    # Check if challenge for this year already exists
    existing = db.query(ReadingChallenge).filter(
        ReadingChallenge.user_id == current_user.id,
        ReadingChallenge.year == data.year
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Challenge for year {data.year} already exists"
        )

    # Count books finished this year
    current_count = db.query(UserBookList).filter(
        UserBookList.user_id == current_user.id,
        UserBookList.status == 'finished',
        UserBookList.finished_date.isnot(None),
        extract('year', UserBookList.finished_date) == data.year
    ).count()

    # Create challenge
    challenge = ReadingChallenge(
        user_id=current_user.id,
        year=data.year,
        goal_count=data.goal_count,
        current_count=current_count,
        is_active=True
    )
    db.add(challenge)
    db.commit()
    db.refresh(challenge)

    percentage = (current_count / data.goal_count) * 100 if data.goal_count > 0 else 0

    return ChallengeResponse(
        id=challenge.id,
        year=challenge.year,
        goal_count=challenge.goal_count,
        current_count=challenge.current_count,
        percentage=round(percentage, 1),
        is_active=challenge.is_active,
        created_at=challenge.created_at,
        updated_at=challenge.updated_at
    )


@router.get("", response_model=List[ChallengeResponse])
async def get_my_challenges(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """내 독서 챌린지 목록"""
    challenges = db.query(ReadingChallenge).filter(
        ReadingChallenge.user_id == current_user.id
    ).order_by(ReadingChallenge.year.desc()).all()

    results = []
    for challenge in challenges:
        percentage = (challenge.current_count / challenge.goal_count) * 100 if challenge.goal_count > 0 else 0
        results.append(ChallengeResponse(
            id=challenge.id,
            year=challenge.year,
            goal_count=challenge.goal_count,
            current_count=challenge.current_count,
            percentage=round(percentage, 1),
            is_active=challenge.is_active,
            created_at=challenge.created_at,
            updated_at=challenge.updated_at
        ))

    return results


@router.get("/current", response_model=ChallengeResponse)
async def get_current_challenge(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """현재 연도의 독서 챌린지"""
    current_year = datetime.now().year

    challenge = db.query(ReadingChallenge).filter(
        ReadingChallenge.user_id == current_user.id,
        ReadingChallenge.year == current_year,
        ReadingChallenge.is_active == True
    ).first()

    if not challenge:
        raise HTTPException(
            status_code=404,
            detail=f"No active challenge found for {current_year}"
        )

    percentage = (challenge.current_count / challenge.goal_count) * 100 if challenge.goal_count > 0 else 0

    return ChallengeResponse(
        id=challenge.id,
        year=challenge.year,
        goal_count=challenge.goal_count,
        current_count=challenge.current_count,
        percentage=round(percentage, 1),
        is_active=challenge.is_active,
        created_at=challenge.created_at,
        updated_at=challenge.updated_at
    )


@router.patch("/{challenge_id}", response_model=ChallengeResponse)
async def update_challenge(
    challenge_id: int,
    data: ChallengeUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """독서 챌린지 수정"""
    challenge = db.query(ReadingChallenge).filter(
        ReadingChallenge.id == challenge_id,
        ReadingChallenge.user_id == current_user.id
    ).first()

    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")

    # Update fields
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(challenge, key, value)

    db.commit()
    db.refresh(challenge)

    percentage = (challenge.current_count / challenge.goal_count) * 100 if challenge.goal_count > 0 else 0

    return ChallengeResponse(
        id=challenge.id,
        year=challenge.year,
        goal_count=challenge.goal_count,
        current_count=challenge.current_count,
        percentage=round(percentage, 1),
        is_active=challenge.is_active,
        created_at=challenge.created_at,
        updated_at=challenge.updated_at
    )


@router.delete("/{challenge_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_challenge(
    challenge_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """독서 챌린지 삭제"""
    challenge = db.query(ReadingChallenge).filter(
        ReadingChallenge.id == challenge_id,
        ReadingChallenge.user_id == current_user.id
    ).first()

    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")

    db.delete(challenge)
    db.commit()

    return None


@router.post("/{challenge_id}/update-progress")
async def update_challenge_progress(
    challenge_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """독서 챌린지 진행도 업데이트 (완독한 책 수 재계산)"""
    challenge = db.query(ReadingChallenge).filter(
        ReadingChallenge.id == challenge_id,
        ReadingChallenge.user_id == current_user.id
    ).first()

    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")

    # Recount finished books for this year
    current_count = db.query(UserBookList).filter(
        UserBookList.user_id == current_user.id,
        UserBookList.status == 'finished',
        UserBookList.finished_date.isnot(None),
        extract('year', UserBookList.finished_date) == challenge.year
    ).count()

    challenge.current_count = current_count
    db.commit()

    return {
        "message": "Progress updated",
        "current_count": current_count,
        "goal_count": challenge.goal_count
    }
