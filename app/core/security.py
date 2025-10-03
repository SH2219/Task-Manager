# app/core/security.py
from __future__ import annotations
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from passlib.context import CryptContext
from jose import jwt, JWTError

from app.core.config import settings

# Password hashing (bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Expose algorithm constant (used elsewhere)
ALGORITHM = settings.JWT_ALGORITHM


def get_password_hash(password: str) -> str:
    """Hash a plaintext password for storage."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against the stored hash."""
    if not hashed_password:
        return False
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(subject: str | int, expires_delta: Optional[timedelta] = None, **extra_claims: Any) -> str:
    """
    Create a signed JWT.

    - subject: usually the user id (int) or unique string. We stringify it when encoding.
    - expires_delta: optional timedelta for expiry (defaults to settings.ACCESS_TOKEN_EXPIRE_MINUTES).
    - extra_claims: any other claims to include in the token payload.
    """
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    now = datetime.utcnow()
    expire = now + expires_delta

    payload: Dict[str, Any] = {
        "sub": str(subject),
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
        **extra_claims,
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)
    return token


def decode_access_token(token: str) -> Dict[str, Any]:
    """
    Decode and validate a JWT. Returns the payload dict.
    Raises jose.JWTError (or subclasses) on invalid/expired tokens.
    """
    # jose.jwt.decode will raise JWTError on invalid signature / expired
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
    return payload


def get_subject_from_token(token: str) -> Optional[str]:
    """
    Convenience: safely return the 'sub' claim from a token, or None if invalid.
    """
    try:
        payload = decode_access_token(token)
        return payload.get("sub")
    except JWTError:
        return None
