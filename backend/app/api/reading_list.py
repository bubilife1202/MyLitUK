from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import date, datetime

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.reading import UserBookList, UserActivity
from app.models.book import Book
from app.models.author import Author
from pydantic import BaseModel, Field


router = APIRouter(prefix="/api/reading-list", tags=["Reading List"])


# Schemas
class BookListCreate(BaseModel):
    book_id: int
    status: str = Field(default="want_to_read", pattern="^(want_to_read|reading|finished)$")
    rating: Optional[float] = Field(None, ge=0.0, le=5.0)
    started_date: Optional[date] = None
    finished_date: Optional[date] = None
    current_page: Optional[int] = None
    total_pages: Optional[int] = None
    notes: Optional[str] = None
    is_favorite: bool = False


class BookListUpdate(BaseModel):
    status: Optional[str] = Field(None, pattern="^(want_to_read|reading|finished)$")
    rating: Optional[float] = Field(None, ge=0.0, le=5.0)
    started_date: Optional[date] = None
    finished_date: Optional[date] = None
    current_page: Optional[int] = None
    total_pages: Optional[int] = None
    notes: Optional[str] = None
    is_favorite: Optional[bool] = None


class BookInList(BaseModel):
    id: int
    title: str
    title_ko: Optional[str]
    author_name: str
    cover_image_url: Optional[str]
    genre: Optional[str]

    class Config:
        from_attributes = True


class BookListResponse(BaseModel):
    id: int
    book: BookInList
    status: str
    rating: Optional[float]
    started_date: Optional[date]
    finished_date: Optional[date]
    current_page: Optional[int]
    total_pages: Optional[int]
    progress_percentage: Optional[float]
    notes: Optional[str]
    is_favorite: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Endpoints
@router.post("", response_model=BookListResponse, status_code=status.HTTP_201_CREATED)
async def add_book_to_list(
    data: BookListCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """책을 독서 리스트에 추가"""
    # Check if book exists
    book = db.query(Book).filter(Book.id == data.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    # Check if already in list
    existing = db.query(UserBookList).filter(
        UserBookList.user_id == current_user.id,
        UserBookList.book_id == data.book_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Book already in your list")

    # Create new entry
    book_list_item = UserBookList(
        user_id=current_user.id,
        **data.model_dump()
    )
    db.add(book_list_item)

    # Create activity
    activity = UserActivity(
        user_id=current_user.id,
        activity_type='added_to_list',
        related_id=data.book_id,
        related_type='book'
    )
    db.add(activity)

    db.commit()
    db.refresh(book_list_item)

    # Load book with author
    book_list_item = db.query(UserBookList).options(
        joinedload(UserBookList.book).joinedload(Book.author)
    ).filter(UserBookList.id == book_list_item.id).first()

    # Format response
    progress = None
    if book_list_item.current_page and book_list_item.total_pages:
        progress = (book_list_item.current_page / book_list_item.total_pages) * 100

    return BookListResponse(
        id=book_list_item.id,
        book=BookInList(
            id=book_list_item.book.id,
            title=book_list_item.book.title,
            title_ko=book_list_item.book.title_ko,
            author_name=book_list_item.book.author.name,
            cover_image_url=book_list_item.book.cover_image_url,
            genre=book_list_item.book.genre
        ),
        status=book_list_item.status,
        rating=book_list_item.rating,
        started_date=book_list_item.started_date,
        finished_date=book_list_item.finished_date,
        current_page=book_list_item.current_page,
        total_pages=book_list_item.total_pages,
        progress_percentage=progress,
        notes=book_list_item.notes,
        is_favorite=book_list_item.is_favorite,
        created_at=book_list_item.created_at,
        updated_at=book_list_item.updated_at
    )


@router.get("", response_model=List[BookListResponse])
async def get_my_reading_list(
    status_filter: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """내 독서 리스트 조회"""
    query = db.query(UserBookList).options(
        joinedload(UserBookList.book).joinedload(Book.author)
    ).filter(UserBookList.user_id == current_user.id)

    if status_filter:
        query = query.filter(UserBookList.status == status_filter)

    items = query.order_by(UserBookList.updated_at.desc()).all()

    results = []
    for item in items:
        progress = None
        if item.current_page and item.total_pages:
            progress = (item.current_page / item.total_pages) * 100

        results.append(BookListResponse(
            id=item.id,
            book=BookInList(
                id=item.book.id,
                title=item.book.title,
                title_ko=item.book.title_ko,
                author_name=item.book.author.name,
                cover_image_url=item.book.cover_image_url,
                genre=item.book.genre
            ),
            status=item.status,
            rating=item.rating,
            started_date=item.started_date,
            finished_date=item.finished_date,
            current_page=item.current_page,
            total_pages=item.total_pages,
            progress_percentage=progress,
            notes=item.notes,
            is_favorite=item.is_favorite,
            created_at=item.created_at,
            updated_at=item.updated_at
        ))

    return results


@router.patch("/{book_id}", response_model=BookListResponse)
async def update_book_in_list(
    book_id: int,
    data: BookListUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """독서 리스트 항목 업데이트"""
    item = db.query(UserBookList).filter(
        UserBookList.user_id == current_user.id,
        UserBookList.book_id == book_id
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="Book not in your list")

    # Update fields
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)

    # If status changed to finished, create activity
    if data.status == 'finished' and item.status != 'finished':
        activity = UserActivity(
            user_id=current_user.id,
            activity_type='finished_book',
            related_id=book_id,
            related_type='book'
        )
        db.add(activity)

    db.commit()
    db.refresh(item)

    # Load with relations
    item = db.query(UserBookList).options(
        joinedload(UserBookList.book).joinedload(Book.author)
    ).filter(UserBookList.id == item.id).first()

    progress = None
    if item.current_page and item.total_pages:
        progress = (item.current_page / item.total_pages) * 100

    return BookListResponse(
        id=item.id,
        book=BookInList(
            id=item.book.id,
            title=item.book.title,
            title_ko=item.book.title_ko,
            author_name=item.book.author.name,
            cover_image_url=item.book.cover_image_url,
            genre=item.book.genre
        ),
        status=item.status,
        rating=item.rating,
        started_date=item.started_date,
        finished_date=item.finished_date,
        current_page=item.current_page,
        total_pages=item.total_pages,
        progress_percentage=progress,
        notes=item.notes,
        is_favorite=item.is_favorite,
        created_at=item.created_at,
        updated_at=item.updated_at
    )


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_book_from_list(
    book_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """독서 리스트에서 책 제거"""
    item = db.query(UserBookList).filter(
        UserBookList.user_id == current_user.id,
        UserBookList.book_id == book_id
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="Book not in your list")

    db.delete(item)
    db.commit()

    return None


@router.get("/stats", response_model=dict)
async def get_reading_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """독서 통계"""
    want_to_read = db.query(UserBookList).filter(
        UserBookList.user_id == current_user.id,
        UserBookList.status == 'want_to_read'
    ).count()

    reading = db.query(UserBookList).filter(
        UserBookList.user_id == current_user.id,
        UserBookList.status == 'reading'
    ).count()

    finished = db.query(UserBookList).filter(
        UserBookList.user_id == current_user.id,
        UserBookList.status == 'finished'
    ).count()

    favorites = db.query(UserBookList).filter(
        UserBookList.user_id == current_user.id,
        UserBookList.is_favorite == True
    ).count()

    return {
        "want_to_read": want_to_read,
        "reading": reading,
        "finished": finished,
        "favorites": favorites,
        "total": want_to_read + reading + finished
    }
