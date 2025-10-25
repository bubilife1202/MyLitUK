from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from app.core.database import get_db
from app.models.book import Book
from app.models.author import Author
from app.schemas.book import BookResponse, BookList
from app.services.bookstore_links import generate_bookstore_links

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
    query = db.query(Book).options(joinedload(Book.author))

    if author_id:
        query = query.filter(Book.author_id == author_id)
    if genre:
        query = query.filter(Book.genre == genre)

    total = query.count()
    books = query.order_by(Book.created_at.desc()).offset((page - 1) * size).limit(size).all()

    # Add author_name to each book
    items = []
    for book in books:
        book_dict = {
            "id": book.id,
            "title": book.title,
            "title_ko": book.title_ko,
            "author_id": book.author_id,
            "author_name": book.author.name if book.author else None,
            "isbn": book.isbn,
            "publication_date": book.publication_date,
            "publisher": book.publisher,
            "genre": book.genre,
            "description": book.description,
            "description_ko": book.description_ko,
            "cover_image_url": book.cover_image_url,
            "amazon_url": book.amazon_url,
            "waterstones_url": book.waterstones_url,
            "created_at": book.created_at
        }
        items.append(book_dict)

    return {
        "items": items,
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
    query = db.query(Book).options(joinedload(Book.author))
    total = query.count()
    books = query.order_by(Book.created_at.desc()).offset((page - 1) * size).limit(size).all()

    # Add author_name to each book
    items = []
    for book in books:
        book_dict = {
            "id": book.id,
            "title": book.title,
            "title_ko": book.title_ko,
            "author_id": book.author_id,
            "author_name": book.author.name if book.author else None,
            "isbn": book.isbn,
            "publication_date": book.publication_date,
            "publisher": book.publisher,
            "genre": book.genre,
            "description": book.description,
            "description_ko": book.description_ko,
            "cover_image_url": book.cover_image_url,
            "amazon_url": book.amazon_url,
            "waterstones_url": book.waterstones_url,
            "created_at": book.created_at
        }
        items.append(book_dict)

    return {
        "items": items,
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


@router.get("/{book_id}/bookstores")
async def get_book_purchase_links(book_id: int, db: Session = Depends(get_db)):
    """
    영국 서점 구매 링크 생성

    제공 서점:
    - Waterstones (UK 최대 서점)
    - Bookshop.org (독립 서점 지원)
    - Foyles (런던 유명 서점)
    - Blackwell's (옥스포드/캠브리지)
    - WHSmith (전국 체인)
    - Amazon UK
    """
    book = db.query(Book).options(joinedload(Book.author)).filter(Book.id == book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    # 서점 링크 생성
    links = generate_bookstore_links(
        title=book.title,
        author=book.author.name if book.author else "Unknown",
        isbn=book.isbn
    )

    return {
        "book_id": book.id,
        "title": book.title,
        "author": book.author.name if book.author else None,
        "isbn": book.isbn,
        "purchase_links": links
    }
