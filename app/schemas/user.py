# app/schemas/user.py
from typing import Optional
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    
class UserCreate(UserBase):
    password: str = Field(min_length=8)  # simple validation
    
class UserUpdate(BaseModel):
    name: Optional[str] = None
    timezone: Optional[str] = None

class UserRead(UserBase):
    id: int
    timezone: Optional[str] = "UTC"
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
