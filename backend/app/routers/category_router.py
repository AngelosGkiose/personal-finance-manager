from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db
from app.models.user_model import UserModel
from app.schemas.categories import CategoryResponse, CategoryCreate, CategoryUpdate
from app.services.category_service import create_category_service, get_categories_service, update_category_service, \
    delete_category_service

router = APIRouter(prefix="/categories",tags=["Categories"])

@router.post("/",response_model=CategoryResponse,status_code=status.HTTP_201_CREATED)
def create_category(data:CategoryCreate,current_user:UserModel=Depends(get_current_user),db:Session=Depends(get_db)):
    return create_category_service(data,current_user,db)


@router.get("/",response_model=list[CategoryResponse],status_code=status.HTTP_200_OK)
def get_categories(current_user:UserModel=Depends(get_current_user),db:Session=Depends(get_db)):
    return get_categories_service(current_user,db)

@router.put("/{category_id}",response_model=CategoryResponse,status_code=status.HTTP_200_OK)
def update_category(category_id:int,data:CategoryUpdate,current_user:UserModel=Depends(get_current_user),db:Session=Depends(get_db)):
    return update_category_service(category_id,data,current_user,db)

@router.delete("/{category_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id:int,current_user:UserModel=Depends(get_current_user),db:Session=Depends(get_db)):
    delete_category_service(category_id,current_user,db)