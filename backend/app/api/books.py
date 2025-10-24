from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.book import Book
from app.schemas.book import BookResponse, BookList

router = APIRouter()

@router.get("", response_model=BookList)
async def list_books(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    author_id: int = Query(None),
    genre: str = Query(None),
    db: Session = Depends(get_db)
):
    """List books with filters"""
    query = db.query(Book)

    if author_id:
        query = query.filter(Book.author_id == author_id)
    if genre:
        query = query.filter(Book.genre == genre)

    total = query.count()
    books = query.order_by(Book.created_at.desc()).offset((page - 1) * size).limit(size).all()

    return {
        "items": books,
        "total": total,
        "page": page,
        "size": size
    }

@router.get("/new", response_model=BookList)
async def new_books(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get recently added books"""
    query = db.query(Book)
    total = query.count()
    books = query.order_by(Book.created_at.desc()).offset((page - 1) * size).limit(size).all()

    return {
        "items": books,
        "total": total,
        "page": page,
        "size": size
    }

@router.get("/{book_id}", response_model=BookResponse)
async def get_book(book_id: int, db: Session = Depends(get_db)):
    """Get book details"""
    book = db.query(Book).filter(Book.id == book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return book
