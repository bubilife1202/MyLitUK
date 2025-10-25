from fastapi import APIRouter, Query
from typing import List, Dict
from app.services.news_feed import fetch_literary_news, fetch_uk_literary_events_from_web

router = APIRouter(prefix="/api/news", tags=["News & Events"])


@router.get("/literary")
async def get_literary_news(max_items: int = Query(10, ge=1, le=50)):
    """
    영국 문학 관련 최신 뉴스 가져오기 (무료 RSS 피드)

    Sources:
    - The Guardian Books
    - BBC Arts & Entertainment
    """
    news = await fetch_literary_news(max_items=max_items)
    return {
        "items": news,
        "total": len(news),
        "sources": ["The Guardian", "BBC"]
    }


@router.get("/events")
async def get_uk_events():
    """
    영국 주요 문학 이벤트 정보

    주요 이벤트:
    - London Book Fair
    - Edinburgh International Book Festival
    - Hay Festival
    - Cheltenham Literature Festival
    - Oxford Literary Festival
    """
    events = await fetch_uk_literary_events_from_web()
    return {
        "items": events,
        "total": len(events)
    }
