# app/services/project_service.py
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.repositories.project_repo import project_repo
from app.repositories.user_repo import user_repo
from app.models.project import Project




class ProjectService:
    async def create_project(self, db: AsyncSession, owner_id: int, name: str, visibility: Optional[str] = "private") -> Project:
        """
        Create a project and optionally log activity.
        Validates owner exists.
        """
        owner = await user_repo.get(db, owner_id)
        if not owner:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Owner user not found")
        
        project_obj = {"name": name, "owner_id": owner_id, "visibility": visibility}
        created = await project_repo.create(db, project_obj)
        
       
        await db.commit()
        await db.refresh(created)
        return created
    
    
    async def get_project(self, db: AsyncSession, project_id: int) -> Optional[Project]:
        project = await project_repo.get(db, project_id)
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
        return project
    
    async def list_projects_for_owner(self, db: AsyncSession, owner_id: int, skip: int = 0, limit: int = 50) -> List[Project]:
        return await project_repo.list_for_owner(db, owner_id, skip=skip, limit=limit)
    
    async def update_project(self, db: AsyncSession, project_id: int, patch: dict, requester_id: Optional[int] = None) -> Project:
        """
        Update project fields. Optionally check that requester is owner.
        """
        project = await project_repo.get(db, project_id)
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
        
         # permission check: only owner can update (simple policy)
        if requester_id is not None and project.owner_id != requester_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed to update project")

        updated = await project_repo.update_by_id(db, project_id, patch)
        if updated is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update project")

        await db.commit()
        await db.refresh(updated)
        return updated
    
    
    async def delete_project(self, db: AsyncSession, project_id: int, requester_id: Optional[int] = None) -> None:
        """
        Delete a project (hard delete). Could be changed to soft delete by adding an 'is_deleted' column.
        Only owner allowed by default.
        """
        project = await project_repo.get(db, project_id)
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

        if requester_id is not None and project.owner_id != requester_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed to delete project")
        
         # For safety you might want to archive rather than hard delete.
        await project_repo.delete_by_id(db, project_id)
        
        await db.commit()
        
        
project_service = ProjectService()
