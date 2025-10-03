# app/api/deps.py
from typing import AsyncGenerator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db  # get_db yields AsyncSession
from app.core.security import decode_access_token
from app.repositories.user_repo import user_repo

bearer_scheme = HTTPBearer(auto_error=False)


async def get_db_dep() -> AsyncGenerator[AsyncSession, None]:
    """
    DB session dependency — yields an AsyncSession.
    Use in routes: db = Depends(get_db_dep)
    """
    async for session in get_db():
        yield session


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db_dep),
):
    """
    Resolve the user from Authorization: Bearer <token>.
    Raises 401 if token missing/invalid or user not found.
    """
    if credentials is None or not credentials.credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    token = credentials.credentials
    try:
        payload = decode_access_token(token)
    except Exception:
        # decode_access_token should raise jose.JWTError or similar on invalid token
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

    sub = payload.get("sub")
    if sub is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token (missing sub)")

    # Prefer numeric user id in sub, fall back to email
    user = None
    try:
        user_id = int(sub)
        user = await user_repo.get(db, user_id)
    except (ValueError, TypeError):
        user = None

    if user is None and "email" in payload:
        user = await user_repo.get_by_email(db, payload["email"])

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return user
