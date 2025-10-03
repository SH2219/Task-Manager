# app/repositories/task_repo.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.task import Task
from app.repositories.base import BaseRepository

class TaskRepository(BaseRepository[Task]):
    def __init__(self):
        super().__init__(Task)
        
    async def get_by_owner(self, db: AsyncSession, owner_id: int):
        result = await db.execute(select(Task).where(Task.owner_id == owner_id))
        return result.scalars().all()
    
task_repo = TaskRepository()