from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List
from datetime import datetime

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.models.reading import UserActivity, UserFollow
from app.models.book import Book
from app.models.author import Author
from pydantic import BaseModel


router = APIRouter(prefix="/api/feed", tags=["Feed"])


# Schemas
class ActivityItem(BaseModel):
    id: int
    user_id: int
    username: str
    activity_type: str
    related_id: int
    related_type: str
    display_text: str
    created_at: datetime

    class Config:
        from_attributes = True


# Endpoints
@router.get("", response_model=List[ActivityItem])
async def get_community_feed(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100)
):
    """커뮤니티 피드 - 팔로우한 사용자들의 활동"""

    # Get users I'm following
    following_ids = db.query(UserFollow.following_id).filter(
        UserFollow.follower_id == current_user.id
    ).all()
    following_ids = [fid[0] for fid in following_ids]

    # If not following anyone, return empty feed
    if not following_ids:
        return []

    # Get activities from followed users
    activities = db.query(UserActivity).filter(
        UserActivity.user_id.in_(following_ids),
        UserActivity.visibility.in_(['public', 'followers_only'])
    ).order_by(desc(UserActivity.created_at)).offset(skip).limit(limit).all()

    # Build feed items
    feed_items = []
    for activity in activities:
        user = db.query(User).filter(User.id == activity.user_id).first()
        if not user:
            continue

        display_text = ""

        if activity.activity_type == 'finished_book':
            book = db.query(Book).filter(Book.id == activity.related_id).first()
            display_text = f"{user.username} finished reading '{book.title}'" if book else f"{user.username} finished a book"

        elif activity.activity_type == 'added_review':
            book = db.query(Book).filter(Book.id == activity.related_id).first()
            display_text = f"{user.username} reviewed '{book.title}'" if book else f"{user.username} added a review"

        elif activity.activity_type == 'followed_author':
            author = db.query(Author).filter(Author.id == activity.related_id).first()
            display_text = f"{user.username} followed {author.name}" if author else f"{user.username} followed an author"

        elif activity.activity_type == 'added_to_list':
            book = db.query(Book).filter(Book.id == activity.related_id).first()
            display_text = f"{user.username} added '{book.title}' to reading list" if book else f"{user.username} added a book to list"

        feed_items.append(ActivityItem(
            id=activity.id,
            user_id=activity.user_id,
            username=user.username,
            activity_type=activity.activity_type,
            related_id=activity.related_id,
            related_type=activity.related_type,
            display_text=display_text,
            created_at=activity.created_at
        ))

    return feed_items


@router.post("/follow/{user_id}")
async def follow_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """다른 사용자 팔로우"""
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot follow yourself")

    target_user = db.query(User).filter(User.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    existing = db.query(UserFollow).filter(
        UserFollow.follower_id == current_user.id,
        UserFollow.following_id == user_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Already following this user")

    follow = UserFollow(follower_id=current_user.id, following_id=user_id)
    db.add(follow)
    db.commit()

    return {"message": "Successfully followed user", "user_id": user_id}


@router.delete("/follow/{user_id}")
async def unfollow_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """사용자 언팔로우"""
    follow = db.query(UserFollow).filter(
        UserFollow.follower_id == current_user.id,
        UserFollow.following_id == user_id
    ).first()

    if not follow:
        raise HTTPException(status_code=404, detail="Not following this user")

    db.delete(follow)
    db.commit()

    return {"message": "Successfully unfollowed user"}
