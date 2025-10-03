# app/api/v1/routers/tasks_router.py
from typing import List
from fastapi import APIRouter, Depends, Query, Path, Body, status

from app.api.deps import get_db_dep, get_current_user
from app.services.task_service import task_service
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate

router = APIRouter()


@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(payload: TaskCreate, db=Depends(get_db_dep), current_user=Depends(get_current_user)):
    task = await task_service.create_task(
        db=db,
        creator_id=current_user.id,
        title=payload.title,
        description=payload.description,
        project_id=payload.project_id,
        assignee_ids=payload.assignee_ids,
        tag_ids=payload.tag_ids,
        priority=payload.priority,
        due_at=payload.due_at,
        start_at=payload.start_at,
        estimated_minutes=payload.estimated_minutes,
        parent_task_id=payload.parent_task_id,
    )
    return task


@router.get("/", response_model=List[TaskRead])
async def list_tasks(skip: int = Query(0), limit: int = Query(50), db=Depends(get_db_dep)):
    return await task_service.list_tasks(db=db, skip=skip, limit=limit)


@router.get("/{task_id}", response_model=TaskRead)
async def get_task(task_id: int = Path(...), db=Depends(get_db_dep)):
    task = await task_service.get_task(db=db, task_id=task_id)
    return task


@router.patch("/{task_id}", response_model=TaskRead)
async def patch_task(task_id: int, payload: TaskUpdate = Body(...), db=Depends(get_db_dep), current_user=Depends(get_current_user)):
    patch = payload.dict(exclude_unset=True)
    expected_version = patch.pop("version", None)
    updated = await task_service.update_task(db=db, task_id=task_id, patch=patch, expected_version=expected_version)
    return updated


@router.post("/{task_id}/assign", response_model=TaskRead)
async def assign(task_id: int, user_ids: list[int] = Body(...), db=Depends(get_db_dep), current_user=Depends(get_current_user)):
    updated = await task_service.assign_users(db=db, task_id=task_id, user_ids=user_ids, assigned_by=current_user.id)
    return updated
