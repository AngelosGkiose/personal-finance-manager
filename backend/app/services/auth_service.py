from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.models.user_model import UserModel
from app.repositories import user_repository
from app.schemas.users import UserCreate
from app.security.security import hash_password


def register_user(user_data:UserCreate,db:Session):
    existing_user=user_repository.get_user_by_email(db,user_data.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Email already registered")
    new_user=UserModel(username=user_data.username,email=user_data.email,hashed_password=hash_password(user_data.password))
    return user_repository.add_user(db,new_user)
