from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class BookBase(BaseModel):
    title: str
    title_ko: Optional[str] = None
    author_id: int
    isbn: Optional[str] = None
    publication_date: Optional[date] = None
    publisher: Optional[str] = None
    genre: Optional[str] = None
    description: Optional[str] = None
    description_ko: Optional[str] = None
    cover_image_url: Optional[str] = None
    amazon_url: Optional[str] = None
    waterstones_url: Optional[str] = None

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: int
    author_name: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class BookList(BaseModel):
    items: list[BookResponse]
    total: int
    page: int
    size: int
