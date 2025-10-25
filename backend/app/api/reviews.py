from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, desc
from typing import List, Optional
from datetime import datetime

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.reading import BookReview, ReviewLike, UserActivity
from app.models.book import Book
from app.models.author import Author
from pydantic import BaseModel, Field


router = APIRouter(prefix="/api/reviews", tags=["Reviews"])


# Schemas
class ReviewCreate(BaseModel):
    book_id: int
    rating: float = Field(..., ge=0.0, le=5.0)
    title: Optional[str] = Field(None, max_length=200)
    content: Optional[str] = None
    spoiler: bool = False
    is_published: bool = True


class ReviewUpdate(BaseModel):
    rating: Optional[float] = Field(None, ge=0.0, le=5.0)
    title: Optional[str] = Field(None, max_length=200)
    content: Optional[str] = None
    spoiler: Optional[bool] = None
    is_published: Optional[bool] = None


class UserBasic(BaseModel):
    id: int
    username: str
    full_name: Optional[str]

    class Config:
        from_attributes = True


class BookBasic(BaseModel):
    id: int
    title: str
    title_ko: Optional[str]
    author_name: str
    cover_image_url: Optional[str]

    class Config:
        from_attributes = True


class ReviewResponse(BaseModel):
    id: int
    user: UserBasic
    book: BookBasic
    rating: float
    title: Optional[str]
    content: Optional[str]
    spoiler: bool
    likes_count: int
    is_published: bool
    user_has_liked: bool = False
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Endpoints
@router.post("", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
async def create_review(
    data: ReviewCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """리뷰 작성"""
    # Check if book exists
    book = db.query(Book).options(joinedload(Book.author)).filter(Book.id == data.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    # Check if review already exists
    existing = db.query(BookReview).filter(
        BookReview.user_id == current_user.id,
        BookReview.book_id == data.book_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="You already reviewed this book")

    # Create review
    review = BookReview(
        user_id=current_user.id,
        **data.model_dump()
    )
    db.add(review)

    # Create activity
    if data.is_published:
        activity = UserActivity(
            user_id=current_user.id,
            activity_type='added_review',
            related_id=data.book_id,
            related_type='review'
        )
        db.add(activity)

    db.commit()
    db.refresh(review)

    # Load with relations
    review = db.query(BookReview).options(
        joinedload(BookReview.user),
        joinedload(BookReview.book).joinedload(Book.author)
    ).filter(BookReview.id == review.id).first()

    return ReviewResponse(
        id=review.id,
        user=UserBasic(
            id=review.user.id,
            username=review.user.username,
            full_name=review.user.full_name
        ),
        book=BookBasic(
            id=review.book.id,
            title=review.book.title,
            title_ko=review.book.title_ko,
            author_name=review.book.author.name,
            cover_image_url=review.book.cover_image_url
        ),
        rating=review.rating,
        title=review.title,
        content=review.content,
        spoiler=review.spoiler,
        likes_count=review.likes_count,
        is_published=review.is_published,
        user_has_liked=False,
        created_at=review.created_at,
        updated_at=review.updated_at
    )


@router.get("", response_model=List[ReviewResponse])
async def get_reviews(
    book_id: Optional[int] = None,
    user_id: Optional[int] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: Optional[User] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """리뷰 목록 조회"""
    query = db.query(BookReview).options(
        joinedload(BookReview.user),
        joinedload(BookReview.book).joinedload(Book.author)
    ).filter(BookReview.is_published == True)

    if book_id:
        query = query.filter(BookReview.book_id == book_id)
    if user_id:
        query = query.filter(BookReview.user_id == user_id)

    reviews = query.order_by(desc(BookReview.created_at)).offset(skip).limit(limit).all()

    # Check if current user liked each review
    user_likes = set()
    if current_user:
        likes = db.query(ReviewLike.review_id).filter(
            ReviewLike.user_id == current_user.id,
            ReviewLike.review_id.in_([r.id for r in reviews])
        ).all()
        user_likes = {like[0] for like in likes}

    results = []
    for review in reviews:
        results.append(ReviewResponse(
            id=review.id,
            user=UserBasic(
                id=review.user.id,
                username=review.user.username,
                full_name=review.user.full_name
            ),
            book=BookBasic(
                id=review.book.id,
                title=review.book.title,
                title_ko=review.book.title_ko,
                author_name=review.book.author.name,
                cover_image_url=review.book.cover_image_url
            ),
            rating=review.rating,
            title=review.title,
            content=review.content,
            spoiler=review.spoiler,
            likes_count=review.likes_count,
            is_published=review.is_published,
            user_has_liked=review.id in user_likes,
            created_at=review.created_at,
            updated_at=review.updated_at
        ))

    return results


@router.get("/my-reviews", response_model=List[ReviewResponse])
async def get_my_reviews(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """내가 작성한 리뷰 목록"""
    reviews = db.query(BookReview).options(
        joinedload(BookReview.user),
        joinedload(BookReview.book).joinedload(Book.author)
    ).filter(BookReview.user_id == current_user.id).order_by(desc(BookReview.created_at)).all()

    results = []
    for review in reviews:
        results.append(ReviewResponse(
            id=review.id,
            user=UserBasic(
                id=review.user.id,
                username=review.user.username,
                full_name=review.user.full_name
            ),
            book=BookBasic(
                id=review.book.id,
                title=review.book.title,
                title_ko=review.book.title_ko,
                author_name=review.book.author.name,
                cover_image_url=review.book.cover_image_url
            ),
            rating=review.rating,
            title=review.title,
            content=review.content,
            spoiler=review.spoiler,
            likes_count=review.likes_count,
            is_published=review.is_published,
            user_has_liked=False,
            created_at=review.created_at,
            updated_at=review.updated_at
        ))

    return results


@router.patch("/{review_id}", response_model=ReviewResponse)
async def update_review(
    review_id: int,
    data: ReviewUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """리뷰 수정"""
    review = db.query(BookReview).filter(
        BookReview.id == review_id,
        BookReview.user_id == current_user.id
    ).first()

    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    # Update fields
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(review, key, value)

    db.commit()
    db.refresh(review)

    # Load with relations
    review = db.query(BookReview).options(
        joinedload(BookReview.user),
        joinedload(BookReview.book).joinedload(Book.author)
    ).filter(BookReview.id == review.id).first()

    return ReviewResponse(
        id=review.id,
        user=UserBasic(
            id=review.user.id,
            username=review.user.username,
            full_name=review.user.full_name
        ),
        book=BookBasic(
            id=review.book.id,
            title=review.book.title,
            title_ko=review.book.title_ko,
            author_name=review.book.author.name,
            cover_image_url=review.book.cover_image_url
        ),
        rating=review.rating,
        title=review.title,
        content=review.content,
        spoiler=review.spoiler,
        likes_count=review.likes_count,
        is_published=review.is_published,
        user_has_liked=False,
        created_at=review.created_at,
        updated_at=review.updated_at
    )


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(
    review_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """리뷰 삭제"""
    review = db.query(BookReview).filter(
        BookReview.id == review_id,
        BookReview.user_id == current_user.id
    ).first()

    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    db.delete(review)
    db.commit()

    return None


@router.post("/{review_id}/like", status_code=status.HTTP_201_CREATED)
async def like_review(
    review_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """리뷰 좋아요"""
    review = db.query(BookReview).filter(BookReview.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    # Check if already liked
    existing = db.query(ReviewLike).filter(
        ReviewLike.user_id == current_user.id,
        ReviewLike.review_id == review_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Already liked")

    # Create like
    like = ReviewLike(user_id=current_user.id, review_id=review_id)
    db.add(like)

    # Update count
    review.likes_count += 1

    db.commit()

    return {"message": "Review liked"}


@router.delete("/{review_id}/like", status_code=status.HTTP_204_NO_CONTENT)
async def unlike_review(
    review_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """리뷰 좋아요 취소"""
    like = db.query(ReviewLike).filter(
        ReviewLike.user_id == current_user.id,
        ReviewLike.review_id == review_id
    ).first()

    if not like:
        raise HTTPException(status_code=404, detail="Like not found")

    # Update count
    review = db.query(BookReview).filter(BookReview.id == review_id).first()
    if review and review.likes_count > 0:
        review.likes_count -= 1

    db.delete(like)
    db.commit()

    return None


@router.get("/book/{book_id}/stats")
async def get_book_review_stats(
    book_id: int,
    db: Session = Depends(get_db)
):
    """책의 리뷰 통계"""
    stats = db.query(
        func.count(BookReview.id).label('total_reviews'),
        func.avg(BookReview.rating).label('average_rating')
    ).filter(
        BookReview.book_id == book_id,
        BookReview.is_published == True
    ).first()

    return {
        "total_reviews": stats.total_reviews or 0,
        "average_rating": round(float(stats.average_rating), 2) if stats.average_rating else 0.0
    }
