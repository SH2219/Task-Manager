# app/repositories/base.py
from typing import Generic, Type, TypeVar, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import DeclarativeMeta

ModelType = TypeVar("ModelType", bound=DeclarativeMeta)


class BaseRepository(Generic[ModelType]):
    def  __init__(self, model: Type[ModelType]):
        self.model = model
        
        
    async def get(self, db:AsyncSession, id:int)-> Optional[ModelType]:
        result = await db.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()

    
    async def list(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> List[ModelType]:
        result = await db.execute(select(self.model).offset(skip).limit(limit))
        return result.scalars().all()
    
    async def create(self, db: AsyncSession, obj_in: dict) -> ModelType:
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def update(self, db: AsyncSession, db_obj: ModelType, obj_in: dict) -> ModelType:
        for field, value in obj_in.item():
            setattr(db_obj, field, value)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def delete(self, db: AsyncSession, id: int) -> None:
        await db.execute(delete(self.model).where(self.model.id == id))
        await db.commit()