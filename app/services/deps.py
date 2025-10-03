# app/api/deps.py
from typing import AsyncGenerator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession


from app.db.session import AsyncSessionLocal, get_db  # get_db yields AsyncSession
from app.core.security import decode_access_token
from app.repositories.user_repo import user_repo

bearer_scheme = HTTPBearer(auto_error=False)


async def get_db_dep() -> AsyncGenerator[AsyncSession, None]:
    """
    Simple wrapper around the session.get_db dependency. Keep this function for clarity/rename.
    """
    async for s in get_db():
        yield s
        

async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db_dep),
):
    
    """
    Dependency to retrieve the current user from the Authorization: Bearer <token> header.
    Raises 401 if invalid or user not found.
    """
    if credentials is None or not credentials.credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    token = credentials.credentials
    try:
        payload = decode_access_token(token)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

    sub = payload.get("sub")
    if sub is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token (missing sub)")

    # We stored subject as str(user_id) in token creation; convert if numeric
    try:
        user_id = int(sub)
    except (ValueError, TypeError):
        user_id = None

    user = None
    if user_id is not None:
        user = await user_repo.get(db, user_id)
        
    # Optionally, support sub being an email:
    if user is None and "email" in payload:
        user = await user_repo.get_by_email(db, payload["email"])

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return user