"""
UK 문학 뉴스 및 이벤트 피드 서비스
"""
import feedparser
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

    Returns:
        이벤트 리스트
    """
    events = []

    # British Council Literature 이벤트 (RSS가 있다면)
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Eventful API (무료, 제한적)
            # 또는 직접 크롤링 대신 RSS 사용
            pass
    except Exception as e:
        print(f"Error fetching events: {e}")

    # 샘플 이벤트 (실제로는 크롤링이나 API 사용)
    events.extend([
        {
            'name': 'London Book Fair 2025',
            'description': 'The global marketplace for rights negotiation and the sale and distribution of content.',
            'location': 'London',
            'date': '2025-04-01',
            'url': 'https://www.londonbookfair.co.uk/',
            'category': 'Book Fair'
        },
        {
            'name': 'Edinburgh International Book Festival',
            'description': 'Annual book festival and cultural gathering in Edinburgh.',
            'location': 'Edinburgh',
            'date': '2025-08-09',
            'url': 'https://www.edbookfest.co.uk/',
            'category': 'Festival'
        },
        {
            'name': 'Cheltenham Literature Festival',
            'description': 'One of the oldest and most prestigious literature festivals in the UK.',
            'location': 'Cheltenham',
            'date': '2025-10-03',
            'url': 'https://www.cheltenhamfestivals.com/literature',
            'category': 'Festival'
        },
        {
            'name': 'Hay Festival',
            'description': 'Annual literature festival in Hay-on-Wye, Wales.',
            'location': 'Hay-on-Wye',
            'date': '2025-05-22',
            'url': 'https://www.hayfestival.com/',
            'category': 'Festival'
        },
        {
            'name': 'Oxford Literary Festival',
            'description': 'Week-long celebration of books and writing.',
            'location': 'Oxford',
            'date': '2025-03-22',
            'url': 'https://oxfordliteraryfestival.org/',
            'category': 'Festival'
        }
    ])

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
