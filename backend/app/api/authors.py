from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.author import Author
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

@router.post("/{author_id}/follow")
async def follow_author(author_id: int, db: Session = Depends(get_db)):
    """Follow an author (requires authentication)"""
    # TODO: Implement with authentication
    raise HTTPException(status_code=501, detail="Not implemented yet")

@router.delete("/{author_id}/follow")
async def unfollow_author(author_id: int, db: Session = Depends(get_db)):
    """Unfollow an author (requires authentication)"""
    # TODO: Implement with authentication
    raise HTTPException(status_code=501, detail="Not implemented yet")
