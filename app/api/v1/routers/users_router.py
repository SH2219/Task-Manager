# app/api/v1/routers/users_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import get_db_dep, get_current_user
from app.services.user_service import user_service
from app.core.security import create_access_token
from app.schemas.user import UserCreate, UserRead

router = APIRouter()


@router.post("/signup", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def signup(payload: UserCreate, db=Depends(get_db_dep)):
    user = await user_service.create_user(db=db, email=payload.email, password=payload.password, name=payload.name)
    return user


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db_dep)):
    """
    OAuth2PasswordRequestForm expects 'username' and 'password' fields.
    We use username == email here.
    """
    user = await user_service.authenticate_user(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token(subject=str(user.id))
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserRead)
async def me(current_user=Depends(get_current_user)):
    return current_user
