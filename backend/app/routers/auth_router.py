

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from app.dependencies.auth import get_current_user
from app.models.user_model import UserModel
from app.schemas.users import UserResponse, UserCreate, LoginResponse, UserLogin
from app.services.auth_service import register_user_service, login_user_service
from app.dependencies.db import get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register",response_model=UserResponse,status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db:Session = Depends(get_db)):
    return register_user_service(user, db)


@router.post("/login",response_model=LoginResponse,status_code=status.HTTP_200_OK)
def login(login_data:UserLogin, db:Session = Depends(get_db)):
    access_token=login_user_service(login_data, db)
    return {"access_token":access_token,"token_type":"bearer"}


@router.get("/me",response_model=UserResponse,status_code=status.HTTP_200_OK)
def get_me(current_user: UserModel = Depends(get_current_user)):
    return current_user
