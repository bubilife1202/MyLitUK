from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.author import Author
from app.models.user import User
from app.models.follows import UserAuthorFollow
from app.schemas.author import AuthorResponse, AuthorList

router = APIRouter()

@router.get("", response_model=AuthorList)
async def list_authors(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    search: str = Query(None),
    db: Session = Depends(get_db)
):
    """List all authors with pagination"""
    query = db.query(Author)

    if search:
        query = query.filter(Author.name.ilike(f"%{search}%"))

    total = query.count()
    authors = query.offset((page - 1) * size).limit(size).all()

    return {
        "items": authors,
        "total": total,
        "page": page,
        "size": size
    }

@router.get("/{author_id}", response_model=AuthorResponse)
async def get_author(author_id: int, db: Session = Depends(get_db)):
    """Get author details"""
    author = db.query(Author).filter(Author.id == author_id).first()

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    return author

@router.post("/{author_id}/follow", status_code=status.HTTP_201_CREATED)
async def follow_author(
    author_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Follow an author (requires authentication)"""
    # Check if author exists
    author = db.query(Author).filter(Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    # Check if already following
    existing = db.query(UserAuthorFollow).filter(
        UserAuthorFollow.user_id == current_user.id,
        UserAuthorFollow.author_id == author_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Already following this author")

    # Create follow
    follow = UserAuthorFollow(user_id=current_user.id, author_id=author_id)
    db.add(follow)
    db.commit()

    return {"message": "Successfully followed author", "author_id": author_id}

@router.delete("/{author_id}/follow", status_code=status.HTTP_204_NO_CONTENT)
async def unfollow_author(
    author_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Unfollow an author (requires authentication)"""
    # Find follow relationship
    follow = db.query(UserAuthorFollow).filter(
        UserAuthorFollow.user_id == current_user.id,
        UserAuthorFollow.author_id == author_id
    ).first()

    if not follow:
        raise HTTPException(status_code=404, detail="Not following this author")

    # Delete follow
    db.delete(follow)
    db.commit()

    return None
