# app/schemas/tag.py
from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class TagCreate(BaseModel):
    name: str
    
class TagRead(BaseModel):
    id: int
    name: str
    created_at: Optional[datetime]

    class Config:
        orm_mode = True