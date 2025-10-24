from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class NotificationBase(BaseModel):
    type: str
    title: str
    message: str
    related_id: Optional[int] = None
    related_type: Optional[str] = None
    action_url: Optional[str] = None
    priority: str = "medium"

class NotificationCreate(NotificationBase):
    user_id: int

class NotificationResponse(NotificationBase):
    id: int
    user_id: int
    is_read: bool
    read_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True

class NotificationList(BaseModel):
    items: List[NotificationResponse]
    total: int
    unread_count: int
    page: int
    size: int

class NotificationStats(BaseModel):
    total: int
    unread: int
    today: int
    this_week: int
