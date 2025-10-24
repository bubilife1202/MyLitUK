from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.core.database import get_db
from app.core.deps import get_current_user, get_current_user_optional
from app.models.literary_award import LiteraryAward, AwardAnnouncement
from app.models.user import User
from app.models.follows import UserAwardFollow
from app.schemas.award import AwardResponse, AwardList

router = APIRouter()

@router.get("", response_model=AwardList)
async def list_awards(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    search: str = Query(None),
    category: str = Query(None),
    current_user: User = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """List literary awards with filters"""
    query = db.query(LiteraryAward)

    # Filter by search term
    if search:
        query = query.filter(
            or_(
                LiteraryAward.name.ilike(f"%{search}%"),
                LiteraryAward.name_ko.ilike(f"%{search}%") if LiteraryAward.name_ko else False
            )
        )

    # Filter by category
    if category:
        query = query.filter(LiteraryAward.category == category)

    # Order by name
    query = query.order_by(LiteraryAward.name.asc())

    total = query.count()
    awards = query.offset((page - 1) * size).limit(size).all()

    # Check if user follows each award
    if current_user:
        followed_award_ids = {f.award_id for f in db.query(UserAwardFollow).filter(
            UserAwardFollow.user_id == current_user.id
        ).all()}
        for award in awards:
            award.is_followed = award.id in followed_award_ids

    return {
        "items": awards,
        "total": total,
        "page": page,
        "size": size
    }

@router.get("/{award_id}", response_model=AwardResponse)
async def get_award(
    award_id: int,
    current_user: User = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """Get award details with announcements"""
    award = db.query(LiteraryAward).filter(LiteraryAward.id == award_id).first()

    if not award:
        raise HTTPException(status_code=404, detail="Award not found")

    # Check if user follows this award
    if current_user:
        follow = db.query(UserAwardFollow).filter(
            UserAwardFollow.user_id == current_user.id,
            UserAwardFollow.award_id == award_id
        ).first()
        award.is_followed = follow is not None

    return award

@router.post("/{award_id}/follow", status_code=status.HTTP_201_CREATED)
async def follow_award(
    award_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Follow a literary award"""
    # Check if award exists
    award = db.query(LiteraryAward).filter(LiteraryAward.id == award_id).first()
    if not award:
        raise HTTPException(status_code=404, detail="Award not found")

    # Check if already following
    existing = db.query(UserAwardFollow).filter(
        UserAwardFollow.user_id == current_user.id,
        UserAwardFollow.award_id == award_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Already following this award")

    # Create follow
    follow = UserAwardFollow(user_id=current_user.id, award_id=award_id)
    db.add(follow)
    db.commit()

    return {"message": "Successfully followed award", "award_id": award_id}

@router.delete("/{award_id}/follow", status_code=status.HTTP_204_NO_CONTENT)
async def unfollow_award(
    award_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Unfollow a literary award"""
    # Find follow relationship
    follow = db.query(UserAwardFollow).filter(
        UserAwardFollow.user_id == current_user.id,
        UserAwardFollow.award_id == award_id
    ).first()

    if not follow:
        raise HTTPException(status_code=404, detail="Not following this award")

    # Delete follow
    db.delete(follow)
    db.commit()

    return None
