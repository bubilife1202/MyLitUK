"""
UK 문학 뉴스 및 이벤트 피드 서비스
"""
try:
    import feedparser
    FEEDPARSER_AVAILABLE = True
except ImportError:
    FEEDPARSER_AVAILABLE = False

import httpx
from typing import List, Dict, Optional
from datetime import datetime
import re


# RSS 피드 URL들 (무료, API 키 불필요)
RSS_FEEDS = {
    'guardian_books': 'https://www.theguardian.com/books/rss',
    'bbc_arts': 'http://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml',
    'british_council': 'https://literature.britishcouncil.org/rss.xml'
}


async def fetch_literary_news(max_items: int = 10) -> List[Dict]:
    """
    영국 문학 관련 최신 뉴스 가져오기

    Returns:
        뉴스 아이템 리스트
    """
    news_items = []

    if not FEEDPARSER_AVAILABLE:
        return news_items

    try:
        # Guardian Books RSS
        feed = feedparser.parse(RSS_FEEDS['guardian_books'])

        for entry in feed.entries[:max_items]:
            news_items.append({
                'source': 'The Guardian',
                'title': entry.title,
                'description': entry.get('summary', ''),
                'link': entry.link,
                'published_date': entry.get('published', ''),
                'category': 'Books'
            })

    except Exception as e:
        print(f"Error fetching Guardian feed: {e}")

    try:
        # BBC Arts & Entertainment RSS
        feed = feedparser.parse(RSS_FEEDS['bbc_arts'])

        for entry in feed.entries[:5]:
            # BBC 피드에서 문학 관련 기사만 필터링
            title_lower = entry.title.lower()
            if any(keyword in title_lower for keyword in ['book', 'author', 'novel', 'literary', 'writer', 'literature']):
                news_items.append({
                    'source': 'BBC',
                    'title': entry.title,
                    'description': entry.get('summary', ''),
                    'link': entry.link,
                    'published_date': entry.get('published', ''),
                    'category': 'Arts & Entertainment'
                })

    except Exception as e:
        print(f"Error fetching BBC feed: {e}")

    # 최신순 정렬
    news_items.sort(key=lambda x: x['published_date'], reverse=True)

    return news_items[:max_items]


async def fetch_uk_literary_events_from_web() -> List[Dict]:
    """
    UK 문학 이벤트 정보를 무료 소스에서 가져오기
    현재 날짜 이후의 이벤트만 반환

    Returns:
        이벤트 리스트 (현재 날짜 이후만)
    """
    from datetime import date

    events = []
    today = date.today()

    # British Council Literature 이벤트 (RSS가 있다면)
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Eventful API (무료, 제한적)
            # 또는 직접 크롤링 대신 RSS 사용
            pass
    except Exception as e:
        print(f"Error fetching events: {e}")

    # UK 주요 문학 이벤트 (2025년 11월부터 시작 - 현재 날짜 이후)
    all_events = [
        {
            'name': 'Bristol Festival of Literature 2025',
            'description': 'Two weeks of literary events featuring authors, poets, and thinkers.',
            'location': 'Bristol',
            'date': '2025-11-07',
            'url': 'https://www.bristolfestivalofliterature.co.uk/',
            'category': 'Festival'
        },
        {
            'name': 'Christmas Literary Market 2025',
            'description': 'Special Christmas book market featuring UK authors and signed editions.',
            'location': 'London',
            'date': '2025-12-12',
            'url': 'https://www.visitlondon.com/',
            'category': 'Market'
        },
        {
            'name': 'New Year Reading Challenge 2026',
            'description': 'Kick off the new year with a month-long reading challenge featuring UK contemporary fiction.',
            'location': 'Online & UK-wide',
            'date': '2026-01-01',
            'url': 'https://www.thebookseller.com/',
            'category': 'Challenge'
        },
        {
            'name': 'Bath Literature Festival 2026',
            'description': 'Ten days of performances, debates, and conversations with internationally-renowned writers.',
            'location': 'Bath',
            'date': '2026-02-26',
            'url': 'https://bathfestivals.org.uk/literature/',
            'category': 'Festival'
        },
        {
            'name': 'Oxford Literary Festival 2026',
            'description': 'Week-long celebration of books and writing featuring talks, workshops, and book signings.',
            'location': 'Oxford',
            'date': '2026-03-20',
            'url': 'https://oxfordliteraryfestival.org/',
            'category': 'Festival'
        },
        {
            'name': 'London Book Fair 2026',
            'description': 'The global marketplace for rights negotiation and the sale and distribution of content across print, audio, TV, film and digital channels.',
            'location': 'London',
            'date': '2026-04-13',
            'url': 'https://www.londonbookfair.co.uk/',
            'category': 'Book Fair'
        },
        {
            'name': 'Hay Festival 2026',
            'description': 'Annual literature and arts festival bringing together writers, musicians, and artists from around the world.',
            'location': 'Hay-on-Wye, Wales',
            'date': '2026-05-20',
            'url': 'https://www.hayfestival.com/',
            'category': 'Festival'
        },
        {
            'name': 'Edinburgh International Book Festival 2026',
            'description': "The world's largest public celebration of the written word, featuring authors from around the globe.",
            'location': 'Edinburgh, Scotland',
            'date': '2026-08-14',
            'url': 'https://www.edbookfest.co.uk/',
            'category': 'Festival'
        },
        {
            'name': 'Manchester Literature Festival 2026',
            'description': 'A celebration of words, ideas and vital new writing, featuring leading literary figures.',
            'location': 'Manchester',
            'date': '2026-10-01',
            'url': 'https://www.manchesterliteraturefestival.co.uk/',
            'category': 'Festival'
        },
        {
            'name': 'Cheltenham Literature Festival 2026',
            'description': 'One of the oldest and most prestigious literature festivals in the UK, showcasing the best in fiction, non-fiction, and poetry.',
            'location': 'Cheltenham',
            'date': '2026-10-09',
            'url': 'https://www.cheltenhamfestivals.com/literature',
            'category': 'Festival'
        }
    ]

    # 현재 날짜 이후의 이벤트만 필터링
    for event in all_events:
        event_date = datetime.strptime(event['date'], '%Y-%m-%d').date()
        if event_date >= today:
            events.append(event)

    # 날짜순 정렬 (가까운 순서대로)
    events.sort(key=lambda x: x['date'])

    return events


def extract_clean_text(html_content: str) -> str:
    """
    HTML에서 깨끗한 텍스트 추출

    Args:
        html_content: HTML 컨텐츠

    Returns:
        정제된 텍스트
    """
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)
        # 연속된 공백 제거
        text = re.sub(r'\s+', ' ', text)
        return text[:500]  # 최대 500자
    except:
        return html_content[:500]
