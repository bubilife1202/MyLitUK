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
    """영국 작가 샘플 데이터 (50명 이상)"""
    print("\n✍️ 작가 데이터 추가 중...")

    authors = [
        # 현대 작가
        {"name": "Sally Rooney", "name_ko": "샐리 루니", "bio": "Irish author known for Normal People and Conversations with Friends.", "bio_ko": "노멀 피플, 대화하는 사람들로 유명한 아일랜드 작가입니다.", "birth_date": date(1991, 2, 20), "nationality": "Irish"},
        {"name": "Zadie Smith", "name_ko": "제이디 스미스", "bio": "British novelist, essayist and short-story writer. Known for White Teeth, On Beauty, and NW.", "bio_ko": "영국의 소설가이자 수필가. 화이트 티스, 온 뷰티, NW 등으로 유명합니다.", "birth_date": date(1975, 10, 25), "nationality": "British"},
        {"name": "Kazuo Ishiguro", "name_ko": "가즈오 이시구로", "bio": "Nobel Prize-winning British novelist. Author of The Remains of the Day and Never Let Me Go.", "bio_ko": "노벨문학상 수상 영국 작가. 남아있는 나날, 나를 보내지 마 등의 작품으로 유명합니다.", "birth_date": date(1954, 11, 8), "nationality": "British"},
        {"name": "Ian McEwan", "name_ko": "이언 매큐언", "bio": "British novelist and screenwriter. Known for Atonement, Amsterdam, and Saturday.", "bio_ko": "영국의 소설가. 속죄, 암스테르담, 토요일 등으로 유명합니다.", "birth_date": date(1948, 6, 21), "nationality": "British"},
        {"name": "Hilary Mantel", "name_ko": "힐러리 맨텔", "bio": "British writer who won the Booker Prize twice for Wolf Hall and Bring Up the Bodies.", "bio_ko": "울프 홀과 브링 업 더 보디스로 두 번의 부커상을 수상한 영국 작가입니다.", "birth_date": date(1952, 7, 6), "nationality": "British"},
        {"name": "Bernardine Evaristo", "name_ko": "버나딘 에바리스토", "bio": "British author and academic. First Black woman to win the Booker Prize with Girl, Woman, Other.", "bio_ko": "걸, 우먼, 아더로 부커상을 수상한 최초의 흑인 여성 작가입니다.", "birth_date": date(1959, 5, 28), "nationality": "British"},
        {"name": "Ali Smith", "name_ko": "앨리 스미스", "bio": "Scottish author known for Seasonal Quartet and How to Be Both.", "bio_ko": "계절 4부작과 둘 다 되는 법으로 유명한 스코틀랜드 작가입니다.", "birth_date": date(1962, 8, 24), "nationality": "British"},
        {"name": "Jojo Moyes", "name_ko": "조조 모예스", "bio": "British novelist known for Me Before You and The Giver of Stars.", "bio_ko": "미 비포 유, 별을 주는 사람으로 유명한 영국 소설가입니다.", "birth_date": date(1969, 8, 4), "nationality": "British"},
        {"name": "David Nicholls", "name_ko": "데이비드 니콜스", "bio": "British novelist and screenwriter, author of One Day and Us.", "bio_ko": "원 데이, 어스로 유명한 영국 소설가이자 각본가입니다.", "birth_date": date(1966, 11, 30), "nationality": "British"},
        {"name": "Matt Haig", "name_ko": "매트 헤이그", "bio": "British author known for The Midnight Library and How to Stop Time.", "bio_ko": "미드나잇 라이브러리, 시간을 멈추는 법으로 유명한 영국 작가입니다.", "birth_date": date(1975, 7, 3), "nationality": "British"},

        # 고전 작가
        {"name": "J.K. Rowling", "name_ko": "J.K. 롤링", "bio": "British author, creator of the Harry Potter series.", "bio_ko": "해리 포터 시리즈를 창조한 영국 작가입니다.", "birth_date": date(1965, 7, 31), "nationality": "British"},
        {"name": "George Orwell", "name_ko": "조지 오웰", "bio": "British novelist and essayist. Author of 1984 and Animal Farm.", "bio_ko": "1984와 동물농장의 저자인 영국 소설가이자 수필가입니다.", "birth_date": date(1903, 6, 25), "nationality": "British"},
        {"name": "Virginia Woolf", "name_ko": "버지니아 울프", "bio": "British modernist writer. Known for Mrs Dalloway and To the Lighthouse.", "bio_ko": "댈러웨이 부인, 등대로로 유명한 영국 모더니스트 작가입니다.", "birth_date": date(1882, 1, 25), "nationality": "British"},
        {"name": "Jane Austen", "name_ko": "제인 오스틴", "bio": "English novelist known for Pride and Prejudice and Emma.", "bio_ko": "오만과 편견, 엠마로 유명한 영국 소설가입니다.", "birth_date": date(1775, 12, 16), "nationality": "British"},
        {"name": "Charles Dickens", "name_ko": "찰스 디킨스", "bio": "Victorian novelist. Author of Great Expectations and A Tale of Two Cities.", "bio_ko": "위대한 유산, 두 도시 이야기의 저자인 빅토리아 시대 소설가입니다.", "birth_date": date(1812, 2, 7), "nationality": "British"},

        # 추가 현대 작가들
        {"name": "Graham Swift", "name_ko": "그레이엄 스위프트", "bio": "British author who won the Booker Prize for Last Orders.", "bio_ko": "라스트 오더스로 부커상을 수상한 영국 작가입니다.", "birth_date": date(1949, 5, 4), "nationality": "British"},
        {"name": "Julian Barnes", "name_ko": "줄리언 반스", "bio": "British author known for The Sense of an Ending and Flaubert's Parrot.", "bio_ko": "예감은 틀리지 않는다, 플로베르의 앵무새로 유명한 영국 작가입니다.", "birth_date": date(1946, 1, 19), "nationality": "British"},
        {"name": "Martin Amis", "name_ko": "마틴 에이미스", "bio": "British novelist known for Money and London Fields.", "bio_ko": "머니, 런던 필즈로 유명한 영국 소설가입니다.", "birth_date": date(1949, 8, 25), "nationality": "British"},
        {"name": "Angela Carter", "name_ko": "앤젤라 카터", "bio": "British novelist known for The Bloody Chamber and Nights at the Circus.", "bio_ko": "피의 방, 서커스의 밤으로 유명한 영국 소설가입니다.", "birth_date": date(1940, 5, 7), "nationality": "British"},
        {"name": "Pat Barker", "name_ko": "팻 바커", "bio": "British writer known for the Regeneration Trilogy.", "bio_ko": "재생 3부작으로 유명한 영국 작가입니다.", "birth_date": date(1943, 5, 8), "nationality": "British"},
        {"name": "Sarah Waters", "name_ko": "세라 워터스", "bio": "Welsh novelist known for Fingersmith and The Night Watch.", "bio_ko": "핑거스미스, 나잇 워치로 유명한 웨일스 소설가입니다.", "birth_date": date(1966, 7, 21), "nationality": "British"},
        {"name": "Nick Hornby", "name_ko": "닉 혼비", "bio": "British writer known for High Fidelity and About a Boy.", "bio_ko": "하이 피델리티, 어바웃 어 보이로 유명한 영국 작가입니다.", "birth_date": date(1957, 4, 17), "nationality": "British"},
        {"name": "Helen Fielding", "name_ko": "헬렌 필딩", "bio": "British novelist known for Bridget Jones's Diary.", "bio_ko": "브리짓 존스의 일기로 유명한 영국 소설가입니다.", "birth_date": date(1958, 2, 19), "nationality": "British"},
        {"name": "Jeanette Winterson", "name_ko": "자넷 윈터슨", "bio": "British author known for Oranges Are Not the Only Fruit.", "bio_ko": "오렌지만이 과일은 아니다로 유명한 영국 작가입니다.", "birth_date": date(1959, 8, 27), "nationality": "British"},
        {"name": "Kate Atkinson", "name_ko": "케이트 앳킨슨", "bio": "British novelist known for Life After Life and Behind the Scenes at the Museum.", "bio_ko": "인생, 두 번째 기회, 박물관 뒤편의 비밀로 유명한 영국 소설가입니다.", "birth_date": date(1951, 12, 20), "nationality": "British"},

        # 스코틀랜드/아일랜드 작가들
        {"name": "Irvine Welsh", "name_ko": "어빈 웰시", "bio": "Scottish novelist known for Trainspotting.", "bio_ko": "트레인스포팅으로 유명한 스코틀랜드 소설가입니다.", "birth_date": date(1958, 9, 27), "nationality": "British"},
        {"name": "Roddy Doyle", "name_ko": "로디 도일", "bio": "Irish novelist known for The Commitments and Paddy Clarke Ha Ha Ha.", "bio_ko": "커미트먼트, 패디 클라크 하하하로 유명한 아일랜드 소설가입니다.", "birth_date": date(1958, 5, 8), "nationality": "Irish"},
        {"name": "Colm Tóibín", "name_ko": "콜름 토이빈", "bio": "Irish novelist known for Brooklyn and The Master.", "bio_ko": "브루클린, 마스터로 유명한 아일랜드 소설가입니다.", "birth_date": date(1955, 5, 30), "nationality": "Irish"},
        {"name": "Anne Enright", "name_ko": "앤 엔라이트", "bio": "Irish author who won the Booker Prize for The Gathering.", "bio_ko": "더 개더링으로 부커상을 수상한 아일랜드 작가입니다.", "birth_date": date(1962, 10, 11), "nationality": "Irish"},
        {"name": "Sebastian Barry", "name_ko": "세바스찬 배리", "bio": "Irish novelist and playwright known for Days Without End.", "bio_ko": "끝없는 나날들로 유명한 아일랜드 소설가이자 극작가입니다.", "birth_date": date(1955, 7, 5), "nationality": "Irish"},

        # 장르 소설가들
        {"name": "Neil Gaiman", "name_ko": "닐 게이먼", "bio": "British author of fantasy and graphic novels. Known for American Gods and Coraline.", "bio_ko": "아메리칸 갓즈, 코랄라인으로 유명한 영국 판타지 작가입니다.", "birth_date": date(1960, 11, 10), "nationality": "British"},
        {"name": "Philip Pullman", "name_ko": "필립 풀먼", "bio": "British author of the His Dark Materials trilogy.", "bio_ko": "황금 나침반 3부작의 저자인 영국 작가입니다.", "birth_date": date(1946, 10, 19), "nationality": "British"},
        {"name": "Terry Pratchett", "name_ko": "테리 프래쳇", "bio": "British author of the Discworld series.", "bio_ko": "디스크월드 시리즈의 저자인 영국 작가입니다.", "birth_date": date(1948, 4, 28), "nationality": "British"},
        {"name": "Douglas Adams", "name_ko": "더글러스 애덤스", "bio": "British author known for The Hitchhiker's Guide to the Galaxy.", "bio_ko": "은하수를 여행하는 히치하이커를 위한 안내서로 유명한 영국 작가입니다.", "birth_date": date(1952, 3, 11), "nationality": "British"},

        # 추가 베스트셀러 작가들
        {"name": "Lee Child", "name_ko": "리 차일드", "bio": "British author known for the Jack Reacher series.", "bio_ko": "잭 리처 시리즈로 유명한 영국 작가입니다.", "birth_date": date(1954, 10, 29), "nationality": "British"},
        {"name": "Robert Harris", "name_ko": "로버트 해리스", "bio": "British novelist known for Fatherland and The Ghost.", "bio_ko": "파더랜드, 고스트로 유명한 영국 소설가입니다.", "birth_date": date(1957, 3, 7), "nationality": "British"},
        {"name": "Ken Follett", "name_ko": "켄 폴릿", "bio": "British author known for The Pillars of the Earth.", "bio_ko": "대지의 기둥으로 유명한 영국 작가입니다.", "birth_date": date(1949, 6, 5), "nationality": "British"},
        {"name": "Ruth Rendell", "name_ko": "루스 렌델", "bio": "British crime writer and author of psychological thrillers.", "bio_ko": "범죄 소설과 심리 스릴러의 거장인 영국 작가입니다.", "birth_date": date(1930, 2, 17), "nationality": "British"},
        {"name": "P.D. James", "name_ko": "P.D. 제임스", "bio": "British crime writer known for the Adam Dalgliesh series.", "bio_ko": "아담 달글리시 시리즈로 유명한 영국 범죄 소설가입니다.", "birth_date": date(1920, 8, 3), "nationality": "British"},

        # 젊은 세대 작가들
        {"name": "Daisy Johnson", "name_ko": "데이지 존슨", "bio": "British novelist and short story writer, author of Everything Under.", "bio_ko": "모든 것은 아래에로 유명한 영국 소설가입니다.", "birth_date": date(1990, 1, 1), "nationality": "British"},
        {"name": "Candice Carty-Williams", "name_ko": "캔디스 카티-윌리엄스", "bio": "British author known for Queenie.", "bio_ko": "퀴니로 유명한 영국 작가입니다.", "birth_date": date(1989, 1, 1), "nationality": "British"},
        {"name": "Madeline Miller", "name_ko": "매들린 밀러", "bio": "American author of Circe and The Song of Achilles.", "bio_ko": "키르케, 아킬레우스의 노래로 유명한 작가입니다.", "birth_date": date(1978, 7, 24), "nationality": "American"},
        {"name": "Taylor Jenkins Reid", "name_ko": "테일러 젠킨스 리드", "bio": "American author known for Daisy Jones & The Six.", "bio_ko": "데이지 존스 앤 더 식스로 유명한 작가입니다.", "birth_date": date(1983, 12, 20), "nationality": "American"},
        {"name": "Brit Bennett", "name_ko": "브릿 베넷", "bio": "American author known for The Vanishing Half.", "bio_ko": "베니싱 하프로 유명한 작가입니다.", "birth_date": date(1990, 1, 1), "nationality": "American"},

        # 더 많은 영국 작가들
        {"name": "Monica Ali", "name_ko": "모니카 알리", "bio": "British writer known for Brick Lane.", "bio_ko": "브릭 레인으로 유명한 영국 작가입니다.", "birth_date": date(1967, 10, 20), "nationality": "British"},
        {"name": "Alan Hollinghurst", "name_ko": "앨런 홀링허스트", "bio": "British novelist who won the Booker Prize for The Line of Beauty.", "bio_ko": "아름다움의 선으로 부커상을 수상한 영국 소설가입니다.", "birth_date": date(1954, 5, 26), "nationality": "British"},
        {"name": "Salman Rushdie", "name_ko": "살만 루슈디", "bio": "British-Indian novelist known for Midnight's Children.", "bio_ko": "한밤의 아이들로 유명한 영국-인도 소설가입니다.", "birth_date": date(1947, 6, 19), "nationality": "British"},
        {"name": "Will Self", "name_ko": "윌 셀프", "bio": "British author and journalist known for experimental fiction.", "bio_ko": "실험적 소설로 유명한 영국 작가이자 저널리스트입니다.", "birth_date": date(1961, 9, 26), "nationality": "British"},
        {"name": "A.S. Byatt", "name_ko": "A.S. 바이어트", "bio": "British novelist who won the Booker Prize for Possession.", "bio_ko": "포제션으로 부커상을 수상한 영국 소설가입니다.", "birth_date": date(1936, 8, 24), "nationality": "British"},
        {"name": "Margaret Drabble", "name_ko": "마거릿 드래블", "bio": "British novelist known for The Millstone and The Radiant Way.", "bio_ko": "밀스톤, 빛나는 길로 유명한 영국 소설가입니다.", "birth_date": date(1939, 6, 5), "nationality": "British"}
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
