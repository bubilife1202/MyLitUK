from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class AuthorBase(BaseModel):
    name: str
    name_ko: Optional[str] = None
    bio: Optional[str] = None
    bio_ko: Optional[str] = None
    birth_date: Optional[date] = None
    nationality: str = "UK"
    photo_url: Optional[str] = None
    website_url: Optional[str] = None

class AuthorCreate(AuthorBase):
    pass

class AuthorUpdate(BaseModel):
    name: Optional[str] = None
    name_ko: Optional[str] = None
    bio: Optional[str] = None
    bio_ko: Optional[str] = None
    birth_date: Optional[date] = None
    photo_url: Optional[str] = None
    website_url: Optional[str] = None

class AuthorResponse(AuthorBase):
    id: int
    created_at: Optional[datetime] = None
    is_followed: bool = False  # Will be set based on current user

    class Config:
        from_attributes = True

class AuthorList(BaseModel):
    items: list[AuthorResponse]
    total: int
    page: int
    size: int
