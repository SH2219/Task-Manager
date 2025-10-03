# app/repositories/project_repo.py
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from app.models.project import Project

from app.repositories.base import BaseRepository

class ProjectRepository(BaseRepository[Project]):
    def __init__(self):
        super().__init__(Project)

    async def list_for_owner(self, db: AsyncSession, owner_id: int, skip: int = 0, limit: int = 100) -> List[Project]:
        q = await db.execute(select(Project).where(Project.owner_id == owner_id).offset(skip).limit(limit))
        return q.scalars().all()

    async def update_by_id(self, db: AsyncSession, project_id: int, patch: dict) -> Optional[Project]:
        # simple update using ORM object
        project = await self.get(db, project_id)
        if project is None:
            return None
        for k, v in patch.items():
            setattr(project, k, v)
        db.add(project)
        await db.commit()
        await db.refresh(project)
        return project

    async def delete_by_id(self, db: AsyncSession, project_id: int) -> None:
        await db.execute(delete(Project).where(Project.id == project_id))
        await db.commit()

project_repo = ProjectRepository()
