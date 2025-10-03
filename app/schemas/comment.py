# app/schemas/comment.py
from typing import Optional  # Ensure Optional is imported
from datetime import datetime
from pydantic import BaseModel

class CommentCreate(BaseModel):
    body: str

class CommentRead(BaseModel):
    id: int
    task_id: Optional[int]
    user_id: Optional[int]  # Correct usage of Optional
    body: str
    created_at: Optional[datetime]
    edited_at: Optional[datetime]

    class Config:
        orm_mode = True