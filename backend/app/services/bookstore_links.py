"""
영국 서점 링크 생성 서비스
"""
from urllib.parse import quote
from typing import Dict, Optional


def generate_bookstore_links(title: str, author: str, isbn: Optional[str] = None) -> Dict[str, str]:
    """
    책 제목, 저자, ISBN을 기반으로 영국 주요 서점 링크 생성

    Args:
        title: 책 제목
        author: 저자명
        isbn: ISBN (선택사항)

    Returns:
        서점별 링크 딕셔너리
    """
    links = {}

    # Waterstones (UK 최대 서점 체인)
    if isbn:
        # ISBN으로 직접 링크
        links['waterstones'] = f"https://www.waterstones.com/book/{isbn}"
    else:
        # 제목+저자로 검색
        search_query = quote(f"{title} {author}")
        links['waterstones'] = f"https://www.waterstones.com/books/search/term/{search_query}"

    # Bookshop.org (독립 서점 지원 플랫폼)
    if isbn:
        links['bookshop'] = f"https://uk.bookshop.org/books/{isbn}"
    else:
        search_query = quote(f"{title} {author}")
        links['bookshop'] = f"https://uk.bookshop.org/search?keywords={search_query}"

    # Foyles (런던 유명 서점)
    search_query = quote(f"{title} {author}")
    links['foyles'] = f"https://www.foyles.co.uk/all?term={search_query}"

    # Blackwell's (옥스포드/캠브리지 서점)
    search_query = quote(title)
    links['blackwells'] = f"https://blackwells.co.uk/bookshop/search/title/{search_query}/author/{quote(author)}"

    # WHSmith (UK 전국 체인)
    search_query = quote(f"{title} {author}")
    links['whsmith'] = f"https://www.whsmith.co.uk/search?w={search_query}"

    # Amazon UK (참고용)
    if isbn:
        links['amazon_uk'] = f"https://www.amazon.co.uk/dp/{isbn}"
    else:
        search_query = quote(f"{title} {author}")
        links['amazon_uk'] = f"https://www.amazon.co.uk/s?k={search_query}"

    return links


def get_primary_uk_links(title: str, author: str, isbn: Optional[str] = None) -> Dict[str, str]:
    """
    주요 3개 영국 서점 링크만 반환 (홈페이지 표시용)

    Returns:
        Waterstones, Bookshop.org, Foyles 링크
    """
    all_links = generate_bookstore_links(title, author, isbn)
    return {
        'waterstones': all_links['waterstones'],
        'bookshop': all_links['bookshop'],
        'foyles': all_links['foyles']
    }
