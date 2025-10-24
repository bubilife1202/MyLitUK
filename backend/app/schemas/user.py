from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    full_name: Optional[str] = None
    preferred_language: str = Field(default="en", pattern="^(en|ko)$")

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    preferred_language: Optional[str] = Field(None, pattern="^(en|ko)$")
    notification_in_app: Optional[bool] = None
    notification_browser_push: Optional[bool] = None

class UserResponse(UserBase):
    id: int
    notification_in_app: bool
    notification_browser_push: bool
    last_visit: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True

# Auth Schemas
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: Optional[int] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
