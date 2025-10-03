# app/api/v1/routers/projects_router.py
from typing import List
from fastapi import APIRouter, Depends, Path, Body, Query, status

from app.api.deps import get_db_dep, get_current_user
from app.services.project_service import project_service
from app.schemas.project import ProjectCreate, ProjectRead, ProjectUpdate

router = APIRouter()


@router.post("/", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
async def create_project(payload: ProjectCreate, db=Depends(get_db_dep), current_user=Depends(get_current_user)):
    project = await project_service.create_project(db=db, owner_id=current_user.id, name=payload.name, visibility=payload.visibility)
    return project


@router.get("/", response_model=List[ProjectRead])
async def list_projects(skip: int = Query(0), limit: int = Query(50), db=Depends(get_db_dep), current_user=Depends(get_current_user)):
    projects = await project_service.list_projects_for_owner(db=db, owner_id=current_user.id, skip=skip, limit=limit)
    return projects


@router.get("/{project_id}", response_model=ProjectRead)
async def get_project(project_id: int = Path(...), db=Depends(get_db_dep), current_user=Depends(get_current_user)):
    project = await project_service.get_project(db=db, project_id=project_id)
    return project


@router.patch("/{project_id}", response_model=ProjectRead)
async def update_project(project_id: int, payload: ProjectUpdate = Body(...), db=Depends(get_db_dep), current_user=Depends(get_current_user)):
    patch = payload.dict(exclude_unset=True)
    updated = await project_service.update_project(db=db, project_id=project_id, patch=patch, requester_id=current_user.id)
    return updated


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(project_id: int, db=Depends(get_db_dep), current_user=Depends(get_current_user)):
    await project_service.delete_project(db=db, project_id=project_id, requester_id=current_user.id)
    return {}
