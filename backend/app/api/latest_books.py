from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.author import Author
from app.services.google_books import (
    fetch_recent_books_by_author,
    fetch_recent_books_multiple_authors,
    search_books_by_title
)

router = APIRouter(prefix="/api/latest-books", tags=["Latest Books"])


@router.get("/by-authors")
async def get_latest_books_by_authors(
    author_ids: str = Query(..., description="Comma-separated author IDs (e.g., '1,2,3')"),
    months: int = Query(6, ge=1, le=24, description="최근 몇 개월 이내"),
    books_per_author: int = Query(3, ge=1, le=10, description="작가당 책 수"),
    db: Session = Depends(get_db)
):
    """
    선택한 작가들의 최신 출간 도서 가져오기 (Google Books API)

    - 실시간으로 Google Books에서 최신 정보 가져옴
    - 6개월 이내 신간만 필터링
    - 선택한 작가들의 책만 표시
    """
    # Author IDs 파싱
    try:
        author_id_list = [int(id.strip()) for id in author_ids.split(',')]
    except:
        return {
            "items": [],
            "total": 0,
            "message": "Invalid author_ids format"
        }

    # DB에서 작가 정보 가져오기
    authors = db.query(Author).filter(Author.id.in_(author_id_list)).all()

    if not authors:
        # 작가 데이터가 없으면 기본 작가들로 대체
        default_authors = [
            "Sally Rooney", "Zadie Smith", "Kazuo Ishiguro",
            "Ian McEwan", "Max Porter", "Samantha Harvey",
            "Philip Hoare", "Virginia Woolf", "J.K. Rowling"
        ]
        books = await fetch_recent_books_multiple_authors(
            author_names=default_authors,
            months=months,
            books_per_author=books_per_author
        )
        return {
            "items": books,
            "total": len(books),
            "authors_searched": default_authors,
            "months": months,
            "source": "Google Books API (기본 작가)",
            "note": "DB에 작가 데이터가 없어 기본 작가들로 검색했습니다"
        }

    # 작가 이름 리스트 생성
    author_names = [author.name for author in authors]

    # Google Books API에서 최신 책 가져오기
    books = await fetch_recent_books_multiple_authors(
        author_names=author_names,
        months=months,
        books_per_author=books_per_author
    )

    return {
        "items": books,
        "total": len(books),
        "authors_searched": author_names,
        "months": months,
        "source": "Google Books API (실시간)"
    }


@router.get("/by-custom-authors")
async def get_latest_books_by_custom_authors(
    author_names: str = Query(..., description="Comma-separated author names (e.g., 'Sally Rooney,Ian McEwan')"),
    months: int = Query(6, ge=1, le=24),
    books_per_author: int = Query(3, ge=1, le=10)
):
    """
    커스텀 작가들의 최신 출간 도서 가져오기

    - 사용자가 직접 입력한 작가 이름으로 검색
    - Google Books API 사용
    """
    # 작가 이름 파싱
    author_name_list = [name.strip() for name in author_names.split(',') if name.strip()]

    if not author_name_list:
        return {
            "items": [],
            "total": 0,
            "message": "No author names provided"
        }

    # Google Books API에서 최신 책 가져오기
    books = await fetch_recent_books_multiple_authors(
        author_names=author_name_list,
        months=months,
        books_per_author=books_per_author
    )

    return {
        "items": books,
        "total": len(books),
        "authors_searched": author_name_list,
        "months": months,
        "source": "Google Books API (실시간)"
    }


@router.get("/recent")
async def get_recent_books(
    months: int = Query(6, ge=1, le=24),
    max_results: int = Query(20, ge=1, le=40)
):
    """
    최신 영국 문학 도서 가져오기 (작가 선택 없이)

    - 주요 영국 작가들의 최신 책
    """
    # 주요 영국 작가 리스트
    popular_uk_authors = [
        "Sally Rooney",
        "Ian McEwan",
        "Zadie Smith",
        "Kazuo Ishiguro",
        "Hilary Mantel",
        "Jojo Moyes",
        "David Nicholls",
        "Matt Haig"
    ]

    books = await fetch_recent_books_multiple_authors(
        author_names=popular_uk_authors,
        months=months,
        books_per_author=2
    )

    # max_results 제한
    books = books[:max_results]

    return {
        "items": books,
        "total": len(books),
        "months": months,
        "source": "Google Books API (실시간)"
    }


@router.get("/search")
async def search_books(
    q: str = Query(..., description="검색어 (제목)"),
    max_results: int = Query(10, ge=1, le=20)
):
    """
    제목으로 책 검색

    - Google Books API 사용
    """
    books = await search_books_by_title(title=q, max_results=max_results)

    return {
        "items": books,
        "total": len(books),
        "query": q,
        "source": "Google Books API"
    }
