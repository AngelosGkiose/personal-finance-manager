from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette import status

from app.models.user_model import UserModel
from app.repositories import user_repository
from app.schemas.users import UserCreate, UserLogin
from app.security.security import hash_password, verify_password, create_access_token
from app.services.category_service import create_default_categories_for_user


def register_user_service(
    user_data: UserCreate,
    db: Session
):
    existing_user = user_repository.get_user_by_email(
        db,
        user_data.email
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    new_user = UserModel(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hash_password(user_data.password)
    )

    try:
        user_repository.add_user(
            db,
            new_user
        )

        create_default_categories_for_user(
            user_id=new_user.id,
            db=db
        )

        db.commit()
        db.refresh(new_user)

        return new_user

    except SQLAlchemyError:
        db.rollback()
        raise


def authenticate_user(email:str, password:str,db:Session):
    user = user_repository.get_user_by_email(db,email)
    if user is None:
        return None
    if not verify_password(password,user.hashed_password):
        return None
    return user


def login_user_service(login_data:UserLogin,db:Session):
    user=authenticate_user(login_data.email,login_data.password,db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect email or password")
    access_token=create_access_token(data={"sub":str(user.id)})
    return access_token


