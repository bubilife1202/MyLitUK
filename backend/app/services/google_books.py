"""
책 정보 가져오기 서비스 (Open Library API + Google Books API)
Open Library API를 메인으로 사용하고, Google Books API는 백업으로 사용
"""
import httpx
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import asyncio


async def fetch_recent_books_by_author_openlibrary(author_name: str, months: int = 6, max_results: int = 10) -> List[Dict]:
    """
    Open Library API를 사용하여 작가별 최신 출간 도서 가져오기

    Args:
        author_name: 작가 이름
        months: 최근 몇 개월 이내 (기본 6개월)
        max_results: 최대 결과 수

    Returns:
        책 정보 리스트
    """
    books = []

    # 날짜 계산
    today = datetime.now()
    cutoff_date = today - timedelta(days=months * 30)

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            # Open Library Search API
            url = "https://openlibrary.org/search.json"
            params = {
                'author': author_name,
                'sort': 'new',
                'limit': max_results * 2,  # 필터링을 위해 더 많이 가져오기
                'fields': 'key,title,author_name,first_publish_year,publish_date,isbn,publisher,cover_i,subject'
            }

            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            if 'docs' not in data:
                return []

            for doc in data['docs']:
                # 출간일 확인
                publish_date = doc.get('publish_date')
                first_publish_year = doc.get('first_publish_year')

                # 날짜 파싱 및 필터링
                if publish_date and isinstance(publish_date, list):
                    # 가장 최근 출간일 사용
                    publish_date = publish_date[0] if publish_date else None

                # 연도 기반 필터링
                if first_publish_year:
                    try:
                        if first_publish_year < cutoff_date.year:
                            continue
                    except:
                        pass

                # ISBN 추출
                isbn_list = doc.get('isbn', [])
                isbn = isbn_list[0] if isbn_list else None

                # 책 정보 구성
                book_info = {
                    'title': doc.get('title', ''),
                    'author_name': ', '.join(doc.get('author_name', [author_name])),
                    'isbn': isbn,
                    'publication_date': str(first_publish_year) if first_publish_year else '',
                    'publisher': ', '.join(doc.get('publisher', []))[:100] if doc.get('publisher') else '',
                    'description': ', '.join(doc.get('subject', []))[:500] if doc.get('subject') else '',
                    'cover_image_url': f"https://covers.openlibrary.org/b/id/{doc.get('cover_i')}-M.jpg" if doc.get('cover_i') else '',
                    'page_count': None,
                    'categories': doc.get('subject', [])[:5] if doc.get('subject') else [],
                    'preview_link': f"https://openlibrary.org{doc.get('key')}" if doc.get('key') else '',
                    'info_link': f"https://openlibrary.org{doc.get('key')}" if doc.get('key') else ''
                }

                books.append(book_info)

                if len(books) >= max_results:
                    break

    except Exception as e:
        print(f"Error fetching books from Open Library for {author_name}: {e}")

    return books


async def fetch_recent_books_by_author(author_name: str, months: int = 6, max_results: int = 10) -> List[Dict]:
    """
    작가별 최신 출간 도서 가져오기 (Google Books API)

    Args:
        author_name: 작가 이름
        months: 최근 몇 개월 이내 (기본 6개월)
        max_results: 최대 결과 수

    Returns:
        책 정보 리스트
    """
    books = []

    # 날짜 계산 (현재로부터 N개월 전)
    today = datetime.now()
    cutoff_date = today - timedelta(days=months * 30)
    cutoff_year = cutoff_date.year

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            # Google Books API 쿼리
            # 최근 출간 도서만, 작가별로 필터링
            url = "https://www.googleapis.com/books/v1/volumes"
            params = {
                'q': f'inauthor:"{author_name}"',
                'orderBy': 'newest',  # 최신순
                'maxResults': max_results,
                'langRestrict': 'en',  # 영어 책만
                'printType': 'books'  # 책만 (잡지 제외)
            }

            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            if 'items' not in data:
                return []

            for item in data['items']:
                volume_info = item.get('volumeInfo', {})

                # 출간일 확인
                published_date = volume_info.get('publishedDate', '')
                if not published_date:
                    continue

                # 날짜 파싱 (YYYY, YYYY-MM, YYYY-MM-DD 형식 모두 처리)
                # 6개월 이내만 엄격하게 필터링
                try:
                    pub_date = None
                    if len(published_date) == 4:  # YYYY
                        # 연도만 있는 경우 해당 연도 1월 1일로 가정
                        pub_date = datetime.strptime(f"{published_date}-01-01", '%Y-%m-%d')
                    elif len(published_date) == 7:  # YYYY-MM
                        # 월까지만 있는 경우 해당 월 1일로 가정
                        pub_date = datetime.strptime(f"{published_date}-01", '%Y-%m-%d')
                    else:  # YYYY-MM-DD
                        pub_date = datetime.strptime(published_date[:10], '%Y-%m-%d')

                    # 6개월 이내만 허용
                    if pub_date < cutoff_date:
                        continue
                except Exception as e:
                    # 날짜 파싱 실패하면 건너뛰기
                    continue

                # ISBN 추출
                isbn = None
                isbn_13 = None
                industry_identifiers = volume_info.get('industryIdentifiers', [])
                for identifier in industry_identifiers:
                    if identifier.get('type') == 'ISBN_13':
                        isbn_13 = identifier.get('identifier')
                    elif identifier.get('type') == 'ISBN_10':
                        isbn = identifier.get('identifier')

                # ISBN_13 우선, 없으면 ISBN_10
                final_isbn = isbn_13 or isbn

                # 책 정보 구성
                book_info = {
                    'title': volume_info.get('title', ''),
                    'author_name': ', '.join(volume_info.get('authors', [author_name])),
                    'isbn': final_isbn,
                    'publication_date': published_date,
                    'publisher': volume_info.get('publisher', ''),
                    'description': volume_info.get('description', '')[:500] if volume_info.get('description') else '',
                    'cover_image_url': volume_info.get('imageLinks', {}).get('thumbnail', ''),
                    'page_count': volume_info.get('pageCount'),
                    'categories': volume_info.get('categories', []),
                    'preview_link': volume_info.get('previewLink', ''),
                    'info_link': volume_info.get('infoLink', '')
                }

                books.append(book_info)

    except Exception as e:
        print(f"Error fetching books for {author_name}: {e}")

    return books


async def fetch_recent_books_multiple_authors(
    author_names: List[str],
    months: int = 6,
    books_per_author: int = 3
) -> List[Dict]:
    """
    여러 작가의 최신 도서 한번에 가져오기
    Open Library API를 우선 사용하고, 실패하면 Google Books API 사용

    Args:
        author_names: 작가 이름 리스트
        months: 최근 몇 개월
        books_per_author: 작가당 책 수

    Returns:
        모든 작가의 최신 책 리스트
    """
    async def fetch_with_fallback(author_name: str):
        """Open Library 먼저 시도, 실패하면 Google Books 시도"""
        # 1. Open Library 시도
        books = await fetch_recent_books_by_author_openlibrary(author_name, months, books_per_author)

        # 2. Open Library에서 충분한 책을 못 가져왔으면 Google Books 시도
        if len(books) < books_per_author:
            try:
                google_books = await fetch_recent_books_by_author(author_name, months, books_per_author)
                # Open Library 결과와 합치기 (중복 제거)
                existing_titles = {book['title'].lower() for book in books}
                for book in google_books:
                    if book['title'].lower() not in existing_titles:
                        books.append(book)
                        if len(books) >= books_per_author:
                            break
            except Exception as e:
                print(f"Google Books API also failed for {author_name}: {e}")

        return books

    tasks = []
    for author_name in author_names:
        task = fetch_with_fallback(author_name)
        tasks.append(task)

    # 병렬로 모든 작가의 책 가져오기
    results = await asyncio.gather(*tasks, return_exceptions=True)

    all_books = []
    for result in results:
        if isinstance(result, list):
            all_books.extend(result)

    # 출간일 기준 최신순 정렬
    all_books.sort(key=lambda x: x.get('publication_date', ''), reverse=True)

    return all_books


async def search_books_by_title(title: str, max_results: int = 5) -> List[Dict]:
    """
    제목으로 책 검색

    Args:
        title: 책 제목
        max_results: 최대 결과 수

    Returns:
        책 정보 리스트
    """
    books = []

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            url = "https://www.googleapis.com/books/v1/volumes"
            params = {
                'q': f'intitle:"{title}"',
                'maxResults': max_results,
                'langRestrict': 'en',
                'printType': 'books'
            }

            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            if 'items' not in data:
                return []

            for item in data['items']:
                volume_info = item.get('volumeInfo', {})

                # ISBN 추출
                isbn = None
                isbn_13 = None
                industry_identifiers = volume_info.get('industryIdentifiers', [])
                for identifier in industry_identifiers:
                    if identifier.get('type') == 'ISBN_13':
                        isbn_13 = identifier.get('identifier')
                    elif identifier.get('type') == 'ISBN_10':
                        isbn = identifier.get('identifier')

                final_isbn = isbn_13 or isbn

                book_info = {
                    'title': volume_info.get('title', ''),
                    'author_name': ', '.join(volume_info.get('authors', ['Unknown'])),
                    'isbn': final_isbn,
                    'publication_date': volume_info.get('publishedDate', ''),
                    'publisher': volume_info.get('publisher', ''),
                    'description': volume_info.get('description', '')[:500] if volume_info.get('description') else '',
                    'cover_image_url': volume_info.get('imageLinks', {}).get('thumbnail', ''),
                }

                books.append(book_info)

    except Exception as e:
        print(f"Error searching books by title '{title}': {e}")

    return books
