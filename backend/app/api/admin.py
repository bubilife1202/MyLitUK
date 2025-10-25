from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.author import Author
from app.models.book import Book
from app.services.external_data import fetch_uk_literature_data
from app.core.security import get_password_hash
from app.models.user import User
import subprocess
import os
from datetime import datetime

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


@router.post("/fetch-real-data")
async def fetch_real_literature_data(db: Session = Depends(get_db)):
    """Open Library API에서 실제 UK 문학 데이터 가져오기"""
    try:
        # 외부 API에서 데이터 가져오기
        data = await fetch_uk_literature_data()

        authors_added = 0
        books_added = 0

        # 작가 데이터 저장
        for author_data in data["authors"]:
            # 이미 존재하는지 확인
            existing = db.query(Author).filter(Author.name == author_data["name"]).first()
            if not existing:
                author = Author(
                    name=author_data["name"],
                    bio=author_data["bio"],
                    nationality="British",
                    website=f"https://openlibrary.org/search/authors?q={author_data['name'].replace(' ', '+')}",
                    is_active=True
                )
                db.add(author)
                authors_added += 1

        db.commit()

        # 책 데이터 저장
        for book_data in data["books"]:
            # 작가 찾기
            author = db.query(Author).filter(Author.name == book_data["author_name"]).first()
            if author:
                # 이미 존재하는지 확인
                existing_book = db.query(Book).filter(
                    Book.title == book_data["title"],
                    Book.author_id == author.id
                ).first()

                if not existing_book:
                    book = Book(
                        title=book_data["title"],
                        author_id=author.id,
                        isbn=book_data.get("isbn"),
                        description=book_data.get("description") or f"A notable work by {book_data['author_name']}",
                        publication_year=book_data.get("publish_year"),
                        publisher=book_data.get("publisher"),
                        page_count=book_data.get("page_count"),
                        cover_image_url=book_data.get("cover_url"),
                        language="English"
                    )
                    db.add(book)
                    books_added += 1

        # 데모 사용자 추가 (없으면)
        demo_user = db.query(User).filter(User.email == "demo@mylituk.com").first()
        if not demo_user:
            demo_user = User(
                email="demo@mylituk.com",
                username="demo",
                password_hash=get_password_hash("demo1234"),
                full_name="Demo User",
                preferred_language="en",
                is_active=True
            )
            db.add(demo_user)

        db.commit()

        return {
            "message": "Real UK literature data fetched successfully",
            "authors_added": authors_added,
            "books_added": books_added,
            "total_authors": len(data["authors"]),
            "total_books": len(data["books"])
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching real data: {str(e)}"
        )
