"""
샘플 데이터 추가 스크립트
간단한 MVP를 위한 기본 데이터를 생성합니다.
"""
import sys
from datetime import datetime, date, timedelta
from sqlalchemy.orm import Session
from app.core.database import engine, Base, SessionLocal
from app.models.user import User
from app.models.author import Author
from app.models.book import Book
from app.models.event import Event, EventKeyword
from app.models.literary_award import LiteraryAward, AwardAnnouncement
from app.core.security import get_password_hash

def create_tables():
    """테이블 생성"""
    print("📊 테이블 생성 중...")
    Base.metadata.create_all(bind=engine)
    print("✅ 테이블 생성 완료")

def seed_authors(db: Session):
    """영국 작가 샘플 데이터"""
    print("\n✍️ 작가 데이터 추가 중...")

    authors = [
        {
            "name": "Zadie Smith",
            "name_ko": "제이디 스미스",
            "bio": "British novelist, essayist and short-story writer. Known for White Teeth, On Beauty, and NW.",
            "bio_ko": "영국의 소설가이자 수필가. 화이트 티스, 온 뷰티, NW 등으로 유명합니다.",
            "birth_date": date(1975, 10, 25),
            "nationality": "British",
            "website_url": "https://en.wikipedia.org/wiki/Zadie_Smith"
        },
        {
            "name": "Kazuo Ishiguro",
            "name_ko": "가즈오 이시구로",
            "bio": "Nobel Prize-winning British novelist. Author of The Remains of the Day and Never Let Me Go.",
            "bio_ko": "노벨문학상 수상 영국 작가. 남아있는 나날, 나를 보내지 마 등의 작품으로 유명합니다.",
            "birth_date": date(1954, 11, 8),
            "nationality": "British",
            "website_url": "https://en.wikipedia.org/wiki/Kazuo_Ishiguro"
        },
        {
            "name": "Ian McEwan",
            "name_ko": "이언 매큐언",
            "bio": "British novelist and screenwriter. Known for Atonement, Amsterdam, and Saturday.",
            "bio_ko": "영국의 소설가. 속죄, 암스테르담, 토요일 등으로 유명합니다.",
            "birth_date": date(1948, 6, 21),
            "nationality": "British",
            "website_url": "https://en.wikipedia.org/wiki/Ian_McEwan"
        },
        {
            "name": "Hilary Mantel",
            "name_ko": "힐러리 맨텔",
            "bio": "British writer who won the Booker Prize twice for Wolf Hall and Bring Up the Bodies.",
            "bio_ko": "울프 홀과 브링 업 더 보디스로 두 번의 부커상을 수상한 영국 작가입니다.",
            "birth_date": date(1952, 7, 6),
            "nationality": "British",
            "website_url": "https://en.wikipedia.org/wiki/Hilary_Mantel"
        },
        {
            "name": "Bernardine Evaristo",
            "name_ko": "버나딘 에바리스토",
            "bio": "British author and academic. First Black woman to win the Booker Prize with Girl, Woman, Other.",
            "bio_ko": "걸, 우먼, 아더로 부커상을 수상한 최초의 흑인 여성 작가입니다.",
            "birth_date": date(1959, 5, 28),
            "nationality": "British",
            "website_url": "https://en.wikipedia.org/wiki/Bernardine_Evaristo"
        }
    ]

    for author_data in authors:
        author = Author(**author_data)
        db.add(author)

    db.commit()
    print(f"✅ {len(authors)}명의 작가 추가 완료")

def seed_books(db: Session):
    """책 샘플 데이터"""
    print("\n📚 책 데이터 추가 중...")

    # 작가 ID 가져오기
    zadie = db.query(Author).filter(Author.name == "Zadie Smith").first()
    kazuo = db.query(Author).filter(Author.name == "Kazuo Ishiguro").first()

    books = [
        {
            "title": "White Teeth",
            "title_ko": "화이트 티스",
            "author_id": zadie.id if zadie else None,
            "description": "A story of three families in London spanning multiple generations.",
            "description_ko": "런던의 세 가족이 여러 세대에 걸쳐 펼쳐지는 이야기입니다.",
            "publication_date": date(2000, 1, 1),
            "genre": "Fiction",
            "isbn": "9780375703867",
            "amazon_url": "https://www.amazon.co.uk/White-Teeth-Zadie-Smith/dp/0140276335"
        },
        {
            "title": "Never Let Me Go",
            "title_ko": "나를 보내지 마",
            "author_id": kazuo.id if kazuo else None,
            "description": "A dystopian science fiction novel about human clones.",
            "description_ko": "인간 복제에 관한 디스토피아 SF 소설입니다.",
            "publication_date": date(2005, 4, 5),
            "genre": "Fiction",
            "isbn": "9781400078776",
            "amazon_url": "https://www.amazon.co.uk/Never-Let-Me-Go-Ishiguro/dp/0571224148"
        },
        {
            "title": "The Fraud",
            "title_ko": "사기꾼",
            "author_id": zadie.id if zadie else None,
            "description": "A historical novel set in Victorian England.",
            "description_ko": "빅토리아 시대 영국을 배경으로 한 역사 소설입니다.",
            "publication_date": date(2023, 9, 5),
            "genre": "Historical Fiction",
            "isbn": "9780593316481",
            "amazon_url": "https://www.amazon.co.uk/Fraud-Zadie-Smith/dp/0241337003"
        }
    ]

    for book_data in books:
        if book_data['author_id']:
            book = Book(**book_data)
            db.add(book)

    db.commit()
    print(f"✅ {len(books)}권의 책 추가 완료")

def seed_events(db: Session):
    """문학 행사 샘플 데이터"""
    print("\n🎭 행사 데이터 추가 중...")

    # 다가오는 날짜 설정
    today = date.today()
    next_month = today + timedelta(days=30)
    next_year = today + timedelta(days=180)

    events = [
        {
            "name": "Hay Festival",
            "name_ko": "헤이 페스티벌",
            "type": "festival",
            "is_annual": True,
            "description": "Annual literature festival held in Hay-on-Wye, Wales.",
            "description_ko": "웨일스 헤이온와이에서 열리는 연례 문학 축제입니다.",
            "venue": "Hay-on-Wye",
            "venue_ko": "헤이온와이",
            "city": "Hay-on-Wye",
            "region": "Wales",
            "start_date": date(2025, 5, 22),
            "end_date": date(2025, 6, 1),
            "website_url": "https://www.hayfestival.com/",
            "ticket_open_date": datetime(2025, 3, 1, 10, 0, 0)
        },
        {
            "name": "Edinburgh International Book Festival",
            "name_ko": "에든버러 국제 도서 축제",
            "type": "festival",
            "is_annual": True,
            "description": "World's largest public celebration of the written word.",
            "description_ko": "세계 최대의 문학 축제입니다.",
            "venue": "Charlotte Square Gardens",
            "venue_ko": "샬럿 스퀘어 가든",
            "city": "Edinburgh",
            "region": "Scotland",
            "start_date": date(2025, 8, 9),
            "end_date": date(2025, 8, 25),
            "website_url": "https://www.edbookfest.co.uk/",
            "ticket_open_date": datetime(2025, 6, 1, 10, 0, 0)
        },
        {
            "name": "London Book Fair",
            "name_ko": "런던 북 페어",
            "type": "festival",
            "is_annual": True,
            "description": "International book publishing trade fair.",
            "description_ko": "국제 출판 무역 박람회입니다.",
            "venue": "Olympia London",
            "venue_ko": "올림피아 런던",
            "city": "London",
            "region": "London",
            "start_date": date(2025, 4, 8),
            "end_date": date(2025, 4, 10),
            "website_url": "https://www.londonbookfair.co.uk/",
            "ticket_open_date": datetime(2025, 2, 1, 10, 0, 0)
        }
    ]

    for event_data in events:
        event = Event(**event_data)
        db.add(event)
        db.flush()

        # 키워드 추가
        keywords = ["Literature", "Fiction", "Poetry"]
        for kw in keywords:
            keyword = EventKeyword(event_id=event.id, keyword=kw)
            db.add(keyword)

    db.commit()
    print(f"✅ {len(events)}개의 행사 추가 완료")

def seed_awards(db: Session):
    """문학상 샘플 데이터"""
    print("\n🏆 문학상 데이터 추가 중...")

    awards = [
        {
            "name": "Booker Prize",
            "name_ko": "부커상",
            "description": "Leading literary award in the English-speaking world.",
            "description_ko": "영어권 최고의 문학상입니다.",
            "category": "Fiction",
            "annual_cycle": 1,
            "website_url": "https://thebookerprizes.com/"
        },
        {
            "name": "Women's Prize for Fiction",
            "name_ko": "여성문학상",
            "description": "Annual award for the best original novel written by a woman.",
            "description_ko": "여성 작가의 최고 소설에 수여되는 연례 문학상입니다.",
            "category": "Fiction",
            "annual_cycle": 1,
            "website_url": "https://www.womensprizeforfiction.co.uk/"
        },
        {
            "name": "Costa Book Awards",
            "name_ko": "코스타 문학상",
            "description": "Literary awards for books by authors based in the UK and Ireland.",
            "description_ko": "영국과 아일랜드 작가들의 책에 수여되는 문학상입니다.",
            "category": "Various",
            "annual_cycle": 1,
            "website_url": "https://costa.co.uk/"
        }
    ]

    for award_data in awards:
        award = LiteraryAward(**award_data)
        db.add(award)
        db.flush()

        # 2025년 발표 일정 추가
        stages = [
            {"stage": "longlist", "date": datetime(2025, 9, 3, 10, 0, 0)},
            {"stage": "shortlist", "date": datetime(2025, 10, 15, 10, 0, 0)},
            {"stage": "winner", "date": datetime(2025, 11, 19, 19, 0, 0)}
        ]

        for stage_data in stages:
            announcement = AwardAnnouncement(
                award_id=award.id,
                year=2025,
                stage=stage_data["stage"],
                announcement_date=stage_data["date"],
                announced=False
            )
            db.add(announcement)

    db.commit()
    print(f"✅ {len(awards)}개의 문학상 추가 완료")

def seed_demo_user(db: Session):
    """테스트용 사용자 생성"""
    print("\n👤 테스트 사용자 추가 중...")

    demo_user = User(
        email="demo@mylituk.com",
        username="demo",
        full_name="Demo User",
        password_hash=get_password_hash("demo1234"),
        preferred_language="ko"
    )
    db.add(demo_user)
    db.commit()

    print("✅ 테스트 사용자 추가 완료")
    print("   📧 이메일: demo@mylituk.com")
    print("   🔑 비밀번호: demo1234")

def main():
    print("🚀 MyLitUK MVP 샘플 데이터 추가 시작\n")
    print("=" * 50)

    # 테이블 생성
    create_tables()

    # DB 세션
    db = SessionLocal()

    try:
        # 데이터 추가
        seed_authors(db)
        seed_books(db)
        seed_events(db)
        seed_awards(db)
        seed_demo_user(db)

        print("\n" + "=" * 50)
        print("✅ 모든 샘플 데이터 추가 완료!")
        print("\n📊 추가된 데이터:")
        print(f"   - 작가: {db.query(Author).count()}명")
        print(f"   - 책: {db.query(Book).count()}권")
        print(f"   - 행사: {db.query(Event).count()}개")
        print(f"   - 문학상: {db.query(LiteraryAward).count()}개")
        print(f"   - 사용자: {db.query(User).count()}명")

        print("\n🎉 이제 서버를 실행하세요:")
        print("   cd backend")
        print("   uvicorn app.main:app --reload")

    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    main()
