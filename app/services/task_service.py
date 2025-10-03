# app/services/task_service.py
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from fastapi import HTTPException, status

from app.models.task import Task, task_assignments, task_tags
from app.models.user import User
from app.models.tags import Tag

from app.repositories.task_repo import task_repo
from app.repositories.user_repo import user_repo


class TaskService:
    async def create_task(self, db: AsyncSession, creator_id: int, title: str, description: Optional[str] = None,  project_id: Optional[int] = None,
                          assignee_ids: Optional[List[int]] = None,
                          tag_ids: Optional[List[int]] = None,
                          **kwargs,) -> Task:
        """
        Create task and attach assignees & tags in a single transaction.
        """
        assignee_ids = assignee_ids or []
        tag_ids = tag_ids or []
        # create Task object (not yet committed)
        task_obj = Task(
            project_id=project_id,
            creator_id=creator_id,
            title=title,
            description=description or "",
            **{k: v for k, v in kwargs.items() if hasattr(Task, k)}
        )
        
        db.add(task_obj)
        await db.flush()  # assign task_obj.id
        
        # Attach assignees by inserting into association table
        if assignee_ids:
            #validate users exist
            q = await db.execute(select(User).where(User.id.in_(assignee_ids)))
            users = q.scalars().all()
            found_ids = {u.id for u in users}
            missing = set(assignee_ids) - found_ids
            if missing:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Assignees not found: {missing}")
            
              # Insert association rows
            for uid in assignee_ids:
                await db.execute(
                    task_assignments.insert().values(task_id=task_obj.id, user_id=uid)
                )
                
                    # Attach tags (if provided). Create tags if they don't exist? Here we expect tag ids.
                    
        if tag_ids:
            q= await db.execute(select(Tag).where(Tag.id.in_(tag_ids)))
            tags = q.scalars().all()
            found_ids = {t.id for t in tags}
            missing = set(tag_ids) - found_ids
            
            if missing:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Tags not found: {missing}")
            
            for tid in tag_ids:
                await db.execute(
                    task_tags.insert().values(task_id=task_obj.id, tag_id=tid)
                )
                
        await db.commit()
        await db.refresh(task_obj)
        return task_obj
    
    async def get_task(self, db:AsyncSession, task_id: int)-> Optional[Task]:
        return await task_repo.get(db, task_id)
    
    async def list_tasks(self, db:AsyncSession, skip:int=0, limit:int=100)-> List[Task]:
        return await task_repo.list(db, skip=skip, limit=limit)
    
    async def update_task(self, db: AsyncSession, task_id: int, patch: dict, expected_version: Optional[int] = None) -> Task:
        """
        Update with optimistic locking. `expected_version` is required for concurrency safety.
        """
        
        task = await task_repo.get(db, task_id)
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        
        if expected_version is not None:
            # attempt a conditional update
            stmt = (
                update(Task)
                .where(Task.id == task_id)
                .where(Task.version == expected_version)
                .values(**patch, version=Task.version + 1)
                .execution_options(synchronize_session="fetch")
                .returning(Task)
            )
            
            result = await db.execute(stmt)
            row = result.first()
            if not row:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Version conflict")
            await db.commit()
            updated = row[0]
            # SQLAlchemy may return a Row object — refresh to get ORM instance
            await db.refresh(updated)
            return updated
        else:
             # fallback: naive update (no optimistic locking)
            for k, v in patch.items():
                setattr(task, k, v)
            db.add(task)
            await db.commit()
            await db.refresh(task)
            return task
        
    async def assign_users(self, db: AsyncSession, task_id: int, user_ids: List[int], assigned_by: int) -> Task:
        """
        Replace / add assignment rows for given user_ids. Does validation.
        """
        
        # validate users
        q = await db.execute(select(User).where(User.id.in_(user_ids)))
        
        users = q.scalars().all()
        found_ids = {u.id for u in users}
        missing = set(user_ids) - found_ids
        if missing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User(s) not found: {missing}")

        # remove existing assignments for this task and add new ones (or you can add granular)
        await db.execute(task_assignments.delete().where(task_assignments.c.task_id == task_id))
        for uid in user_ids:
            await db.execute(
                task_assignments.insert().values(task_id=task_id, user_id=uid, assigned_by=assigned_by)
            )
            
            
        await db.commit()
        await db.refresh(task)
        return task
    
    
# singleton
task_service = TaskService()

