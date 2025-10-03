# app/services/user_service.py
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.repositories.user_repo import user_repo
from app.models.user import User
from app.core.security import get_password_hash, verify_password

class UserService:
    async def create_user(self, db:AsyncSession, email:str, password:str, name:Optional[str] = None)->User:
        # Check if user already exists
        existing = await user_repo.get_by_email(db, email)
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        
        hashed = get_password_hash(password)
        user_obj = {"email":email, "password_hash":hashed, "name":name}
           # Use repository create which commits and refreshes
        created = await user_repo.create(db, user_obj)
        return created
    
    async def authenticate_user(self, db:AsyncSession, email:str, password:str)->Optional[User]:
        user = await user.repo.get_by_email(db,email)
        if not user:
            return None
        if not verify_password(password, user.password_hash or ""):
            return None
        return user
    
    async def get_by_id(self, db: AsyncSession, user_id: int) -> Optional[User]:
        return await user_repo.get(db, user_id)       
    
    # singleton instance (optional)
user_service = UserService()