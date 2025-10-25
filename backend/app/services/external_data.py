"""
외부 API에서 실제 UK 문학 데이터 가져오기
"""
import httpx
from typing import List, Dict, Optional

# 유명한 UK 작가 목록
UK_AUTHORS = [
    "J.K. Rowling",
    "Zadie Smith",
    "Kazuo Ishiguro",
    "Ian McEwan",
    "Hilary Mantel",
    "Salman Rushdie",
    "Bernardine Evaristo",
    "Margaret Atwood",
    "Jeanette Winterson",
    "Ali Smith"
]

async def fetch_author_from_openlibrary(author_name: str) -> Optional[Dict]:
    """Open Library API에서 작가 정보 가져오기"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # 작가 검색
            response = await client.get(
                f"https://openlibrary.org/search/authors.json",
                params={"q": author_name}
            )

            if response.status_code == 200:
                data = response.json()
                if data.get("docs") and len(data["docs"]) > 0:
                    author_data = data["docs"][0]

                    # 작가 상세 정보 가져오기
                    author_key = author_data.get("key")
                    if author_key:
                        detail_response = await client.get(f"https://openlibrary.org{author_key}.json")
                        if detail_response.status_code == 200:
                            detail_data = detail_response.json()

                            bio = detail_data.get("bio")
                            if isinstance(bio, dict):
                                bio = bio.get("value", "")
                            elif not bio:
                                bio = f"Renowned British author known for exceptional literary works."

                            return {
                                "name": author_data.get("name", author_name),
                                "bio": bio[:500] if bio else f"Acclaimed British author.",
                                "birth_date": detail_data.get("birth_date"),
                                "top_work": author_data.get("top_work"),
                                "work_count": author_data.get("work_count", 0)
                            }

            return None
    except Exception as e:
        print(f"Error fetching author {author_name}: {e}")
        return None


async def fetch_books_from_openlibrary(author_name: str, limit: int = 5) -> List[Dict]:
    """Open Library API에서 작가의 책 정보 가져오기"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"https://openlibrary.org/search.json",
                params={
                    "author": author_name,
                    "limit": limit,
                    "language": "eng"
                }
            )

            if response.status_code == 200:
                data = response.json()
                books = []

                for doc in data.get("docs", [])[:limit]:
                    book = {
                        "title": doc.get("title", "Unknown Title"),
                        "author_name": author_name,
                        "isbn": doc.get("isbn", [None])[0] if doc.get("isbn") else None,
                        "publish_year": doc.get("first_publish_year"),
                        "description": doc.get("first_sentence", [""])[0] if doc.get("first_sentence") else "",
                        "cover_id": doc.get("cover_i"),
                        "publisher": doc.get("publisher", [None])[0] if doc.get("publisher") else None,
                        "page_count": doc.get("number_of_pages_median")
                    }

                    # 표지 이미지 URL 생성
                    if book["cover_id"]:
                        book["cover_url"] = f"https://covers.openlibrary.org/b/id/{book['cover_id']}-L.jpg"

                    books.append(book)

                return books

            return []
    except Exception as e:
        print(f"Error fetching books for {author_name}: {e}")
        return []


async def fetch_uk_literature_data() -> Dict:
    """UK 문학 데이터 일괄 가져오기"""
    authors_data = []
    all_books = []

    for author_name in UK_AUTHORS[:5]:  # 처음 5명만
        # 작가 정보 가져오기
        author_info = await fetch_author_from_openlibrary(author_name)
        if author_info:
            authors_data.append(author_info)

            # 작가의 책 가져오기
            books = await fetch_books_from_openlibrary(author_name, limit=3)
            all_books.extend(books)

    return {
        "authors": authors_data,
        "books": all_books
    }
