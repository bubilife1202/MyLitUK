from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class AwardNomineeResponse(BaseModel):
    id: int
    book_id: int
    is_winner: bool

    class Config:
        from_attributes = True

class AwardAnnouncementResponse(BaseModel):
    id: int
    year: int
    stage: str
    announcement_date: Optional[datetime] = None
    announced: bool
    nominees: List[AwardNomineeResponse] = []

    class Config:
        from_attributes = True

class AwardBase(BaseModel):
    name: str
    name_ko: Optional[str] = None
    description: Optional[str] = None
    description_ko: Optional[str] = None
    category: Optional[str] = None
    annual_cycle: int = 1
    website_url: Optional[str] = None

class AwardCreate(AwardBase):
    pass

class AwardUpdate(AwardBase):
    name: Optional[str] = None

class AwardResponse(AwardBase):
    id: int
    created_at: datetime
    announcements: List[AwardAnnouncementResponse] = []
    is_followed: bool = False

    class Config:
        from_attributes = True

class AwardList(BaseModel):
    items: List[AwardResponse]
    total: int
    page: int
    size: int
