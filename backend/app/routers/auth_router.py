from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from app.schemas.users import UserResponse, UserCreate
from app.services.auth_service import register_user
from app.dependencies.db import get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register",response_model=UserResponse,status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db:Session = Depends(get_db)):
    return register_user(user, db)