from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional, List

class EventKeywordResponse(BaseModel):
    id: int
    keyword: str

    class Config:
        from_attributes = True

class EventBase(BaseModel):
    name: str
    name_ko: Optional[str] = None
    type: Optional[str] = None
    is_annual: bool = False
    description: Optional[str] = None
    description_ko: Optional[str] = None
    venue: Optional[str] = None
    venue_ko: Optional[str] = None
    city: Optional[str] = None
    region: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    ticket_url: Optional[str] = None
    ticket_open_date: Optional[datetime] = None
    website_url: Optional[str] = None
    image_url: Optional[str] = None

class EventCreate(EventBase):
    pass

class EventUpdate(EventBase):
    name: Optional[str] = None

class EventResponse(EventBase):
    id: int
    created_at: datetime
    keywords: List[EventKeywordResponse] = []
    is_followed: bool = False

    class Config:
        from_attributes = True

class EventList(BaseModel):
    items: List[EventResponse]
    total: int
    page: int
    size: int
