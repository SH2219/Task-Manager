# app/schemas/task.py
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


from .user import UserRead
from .tag import TagRead
from .comment import CommentRead


# --- Create / Update DTOs ---
class TaskCreate(BaseModel):
    project_id: Optional[int] = None
    title: str
    description: Optional[str] = ""
    status: Optional[str] = "todo"
    priority: Optional[int] = 3
    due_at: Optional[datetime] = None
    start_at: Optional[datetime] = None
    estimated_minutes: Optional[int] = None
    parent_task_id: Optional[int] = None
    assignee_ids: Optional[List[int]] = Field(default_factory=list)
    tag_ids: Optional[List[int]] = Field(default_factory=list)


class TaskUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    status: Optional[str]
    priority: Optional[int]
    due_at: Optional[datetime]
    start_at: Optional[datetime]
    estimated_minutes: Optional[int]
    parent_task_id: Optional[int]
    version: Optional[int]  # for optimistic locking
    assignee_ids: Optional[List[int]]
    tag_ids: Optional[List[int]]

# --- Read DTO (nested), think: how much to return? ---


class TaskRead(BaseModel):
    id: int
    project_id: Optional[int]
    creator_id: Optional[int]
    title: str
    description: Optional[str]
    status: str
    priority: int
    due_at: Optional[datetime]
    start_at: Optional[datetime]
    estimated_minutes: Optional[int]
    parent_task_id: Optional[int]
    position: Optional[int]
    version: Optional[int]
    is_deleted: Optional[bool]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    # nested relations (optional: set to [] or None from your controllers)
    assignees: Optional[List[UserRead]] = []
    tags: Optional[List[TagRead]] = []
    comments: Optional[List[CommentRead]] = []

    class Config:
        orm_mode = True
