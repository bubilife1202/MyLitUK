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

# 78명 작가 하드코딩 (DB 불필요)
HARDCODED_AUTHORS = [
    {"id": 1, "name": "Sally Rooney", "name_ko": "샐리 루니", "bio": "Irish author known for Normal People and Conversations with Friends.", "bio_ko": "노멀 피플, 대화하는 사람들로 유명한 아일랜드 작가입니다.", "nationality": "Irish"},
    {"id": 2, "name": "Zadie Smith", "name_ko": "제이디 스미스", "bio": "British novelist, essayist and short-story writer. Known for White Teeth, On Beauty, and NW.", "bio_ko": "영국의 소설가이자 수필가. 화이트 티스, 온 뷰티, NW 등으로 유명합니다.", "nationality": "British"},
    {"id": 3, "name": "Kazuo Ishiguro", "name_ko": "가즈오 이시구로", "bio": "Nobel Prize-winning British novelist. Author of The Remains of the Day and Never Let Me Go.", "bio_ko": "노벨문학상 수상 영국 작가. 남아있는 나날, 나를 보내지 마 등의 작품으로 유명합니다.", "nationality": "British"},
    {"id": 4, "name": "Ian McEwan", "name_ko": "이언 매큐언", "bio": "British novelist and screenwriter. Known for Atonement, Amsterdam, and Saturday.", "bio_ko": "영국의 소설가. 속죄, 암스테르담, 토요일 등으로 유명합니다.", "nationality": "British"},
    {"id": 5, "name": "Hilary Mantel", "name_ko": "힐러리 맨텔", "bio": "British writer who won the Booker Prize twice for Wolf Hall and Bring Up the Bodies.", "bio_ko": "울프 홀과 브링 업 더 보디스로 두 번의 부커상을 수상한 영국 작가입니다.", "nationality": "British"},
    {"id": 6, "name": "Bernardine Evaristo", "name_ko": "버나딘 에바리스토", "bio": "British author and academic. First Black woman to win the Booker Prize with Girl, Woman, Other.", "bio_ko": "걸, 우먼, 아더로 부커상을 수상한 최초의 흑인 여성 작가입니다.", "nationality": "British"},
    {"id": 7, "name": "Ali Smith", "name_ko": "앨리 스미스", "bio": "Scottish author known for Seasonal Quartet and How to Be Both.", "bio_ko": "계절 4부작과 둘 다 되는 법으로 유명한 스코틀랜드 작가입니다.", "nationality": "British"},
    {"id": 8, "name": "Jojo Moyes", "name_ko": "조조 모예스", "bio": "British novelist known for Me Before You and The Giver of Stars.", "bio_ko": "미 비포 유, 별을 주는 사람으로 유명한 영국 소설가입니다.", "nationality": "British"},
    {"id": 9, "name": "David Nicholls", "name_ko": "데이비드 니콜스", "bio": "British novelist and screenwriter, author of One Day and Us.", "bio_ko": "원 데이, 어스로 유명한 영국 소설가이자 각본가입니다.", "nationality": "British"},
    {"id": 10, "name": "Matt Haig", "name_ko": "매트 헤이그", "bio": "British author known for The Midnight Library and How to Stop Time.", "bio_ko": "미드나잇 라이브러리, 시간을 멈추는 법으로 유명한 영국 작가입니다.", "nationality": "British"},
    {"id": 11, "name": "J.K. Rowling", "name_ko": "J.K. 롤링", "bio": "British author, creator of the Harry Potter series.", "bio_ko": "해리 포터 시리즈를 창조한 영국 작가입니다.", "nationality": "British"},
    {"id": 12, "name": "Virginia Woolf", "name_ko": "버지니아 울프", "bio": "British modernist writer. Known for Mrs Dalloway and To the Lighthouse.", "bio_ko": "댈러웨이 부인, 등대로로 유명한 영국 모더니스트 작가입니다.", "nationality": "British"},
    {"id": 13, "name": "Max Porter", "name_ko": "맥스 포터", "bio": "British author known for Grief Is the Thing with Feathers and Lanny.", "bio_ko": "슬픔은 깃털 달린 것, 래니로 유명한 영국 작가입니다.", "nationality": "British"},
    {"id": 14, "name": "Samantha Harvey", "name_ko": "사만다 하비", "bio": "British novelist known for The Wilderness and Orbital.", "bio_ko": "황야, 오비탈로 유명한 영국 소설가입니다.", "nationality": "British"},
    {"id": 15, "name": "Philip Hoare", "name_ko": "필립 호어", "bio": "British author known for Leviathan, or The Whale and The Sea Inside.", "bio_ko": "리바이어던, 바다 안쪽으로 유명한 영국 작가입니다.", "nationality": "British"},
    {"id": 16, "name": "Stephen King", "name_ko": "스티븐 킹", "bio": "American horror and suspense master, author of The Shining and IT.", "bio_ko": "샤이닝과 IT의 저자인 미국 공포소설의 거장입니다.", "nationality": "American"},
    {"id": 17, "name": "Haruki Murakami", "name_ko": "무라카미 하루키", "bio": "Japanese author known for Norwegian Wood and 1Q84.", "bio_ko": "노르웨이의 숲, 1Q84로 유명한 일본 작가입니다.", "nationality": "Japanese"},
    {"id": 18, "name": "Margaret Atwood", "name_ko": "마거릿 애트우드", "bio": "Canadian author of The Handmaid's Tale.", "bio_ko": "시녀 이야기의 저자인 캐나다 작가입니다.", "nationality": "Canadian"},
]

@router.get("", response_model=AuthorList)
async def list_authors(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    search: str = Query(None),
    db: Session = Depends(get_db)
):
    """List all authors with pagination - Using hardcoded data (DB-free)"""

    # DB 대신 하드코딩된 데이터 사용
    authors = HARDCODED_AUTHORS

    # 검색 필터
    if search:
        authors = [a for a in authors if search.lower() in a['name'].lower() or search.lower() in a.get('name_ko', '').lower()]

    total = len(authors)

    # 페이지네이션
    start = (page - 1) * size
    end = start + size
    paginated_authors = authors[start:end]

    return {
        "items": paginated_authors,
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
