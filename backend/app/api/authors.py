from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from typing import Optional
from datetime import date
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.author import Author
from app.models.user import User
from app.models.follows import UserAuthorFollow
from app.models.reading import UserActivity
from app.schemas.author import AuthorResponse, AuthorList

router = APIRouter()

def seed_authors_if_empty(db: Session):
    """데이터가 없으면 기본 작가 추가"""
    count = db.query(Author).count()
    if count > 0:
        return  # 이미 데이터 있음

    print("📝 Auto-seeding authors...")
    basic_authors = [
        {"name": "Sally Rooney", "name_ko": "샐리 루니", "bio": "Irish author known for Normal People and Conversations with Friends.", "bio_ko": "노멀 피플, 대화하는 사람들로 유명한 아일랜드 작가입니다.", "birth_date": date(1991, 2, 20), "nationality": "Irish"},
        {"name": "Zadie Smith", "name_ko": "제이디 스미스", "bio": "British novelist, essayist and short-story writer. Known for White Teeth, On Beauty, and NW.", "bio_ko": "영국의 소설가이자 수필가. 화이트 티스, 온 뷰티, NW 등으로 유명합니다.", "birth_date": date(1975, 10, 25), "nationality": "British"},
        {"name": "Kazuo Ishiguro", "name_ko": "가즈오 이시구로", "bio": "Nobel Prize-winning British novelist. Author of The Remains of the Day and Never Let Me Go.", "bio_ko": "노벨문학상 수상 영국 작가. 남아있는 나날, 나를 보내지 마 등의 작품으로 유명합니다.", "birth_date": date(1954, 11, 8), "nationality": "British"},
        {"name": "Ian McEwan", "name_ko": "이언 매큐언", "bio": "British novelist and screenwriter. Known for Atonement, Amsterdam, and Saturday.", "bio_ko": "영국의 소설가. 속죄, 암스테르담, 토요일 등으로 유명합니다.", "birth_date": date(1948, 6, 21), "nationality": "British"},
        {"name": "Hilary Mantel", "name_ko": "힐러리 맨텔", "bio": "British writer who won the Booker Prize twice for Wolf Hall and Bring Up the Bodies.", "bio_ko": "울프 홀과 브링 업 더 보디스로 두 번의 부커상을 수상한 영국 작가입니다.", "birth_date": date(1952, 7, 6), "nationality": "British"},
        {"name": "Max Porter", "name_ko": "맥스 포터", "bio": "British author known for Grief Is the Thing with Feathers and Lanny.", "bio_ko": "슬픔은 깃털 달린 것, 래니로 유명한 영국 작가입니다.", "birth_date": date(1981, 1, 1), "nationality": "British"},
        {"name": "Samantha Harvey", "name_ko": "사만다 하비", "bio": "British novelist known for The Wilderness and Orbital.", "bio_ko": "황야, 오비탈로 유명한 영국 소설가입니다.", "birth_date": date(1975, 1, 1), "nationality": "British"},
        {"name": "Philip Hoare", "name_ko": "필립 호어", "bio": "British author known for Leviathan, or The Whale and The Sea Inside.", "bio_ko": "리바이어던, 바다 안쪽으로 유명한 영국 작가입니다.", "birth_date": date(1958, 1, 1), "nationality": "British"},
        {"name": "J.K. Rowling", "name_ko": "J.K. 롤링", "bio": "British author, creator of the Harry Potter series.", "bio_ko": "해리 포터 시리즈를 창조한 영국 작가입니다.", "birth_date": date(1965, 7, 31), "nationality": "British"},
        {"name": "Virginia Woolf", "name_ko": "버지니아 울프", "bio": "British modernist writer. Known for Mrs Dalloway and To the Lighthouse.", "bio_ko": "댈러웨이 부인, 등대로로 유명한 영국 모더니스트 작가입니다.", "birth_date": date(1882, 1, 25), "nationality": "British"},
    ]

    for author_data in basic_authors:
        author = Author(**author_data)
        db.add(author)

    db.commit()
    print(f"✅ Added {len(basic_authors)} authors")

@router.get("", response_model=AuthorList)
async def list_authors(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    search: str = Query(None),
    db: Session = Depends(get_db)
):
    """List all authors with pagination"""
    # 데이터 없으면 자동 생성
    seed_authors_if_empty(db)

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

    # Create activity
    activity = UserActivity(
        user_id=current_user.id,
        activity_type='followed_author',
        related_id=author_id,
        related_type='author'
    )
    db.add(activity)

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


@router.get("/following/me", response_model=AuthorList)
async def get_my_followed_authors(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """내가 팔로우한 작가 목록"""
    follows = db.query(UserAuthorFollow).options(
        joinedload(UserAuthorFollow.author)
    ).filter(UserAuthorFollow.user_id == current_user.id).all()

    authors = [follow.author for follow in follows]
    total = len(authors)

    return {
        "items": authors,
        "total": total,
        "page": 1,
        "size": total
    }


@router.get("/{author_id}/is-following")
async def check_if_following(
    author_id: int,
    current_user: Optional[User] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """작가를 팔로우하고 있는지 확인"""
    if not current_user:
        return {"is_following": False}

    follow = db.query(UserAuthorFollow).filter(
        UserAuthorFollow.user_id == current_user.id,
        UserAuthorFollow.author_id == author_id
    ).first()

    return {"is_following": follow is not None}
