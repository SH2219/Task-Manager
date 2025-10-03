# app/schemas/project.py
from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class ProjectCreate(BaseModel):
    name: str
    visibility: Optional[str] = "private"
    
class ProjectUpdate(BaseModel):
    name: Optional[str]
    visibility: Optional[str]

class ProjectRead(BaseModel):
    id: int
    name: str
    owner_id: Optional[int]
    visibility: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
