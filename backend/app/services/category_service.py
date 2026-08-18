from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.models.category_model import CategoryModel
from app.models.user_model import UserModel
from app.repositories.category_repository import get_category_by_name, add_category, get_categories_by_user_id, \
    update_category_repo, get_category_by_id, delete_category_repo
from app.schemas.categories import CategoryCreate, CategoryUpdate

DEFAULT_CATEGORIES = [
    ("Other Expenses", True),
    ("Supermarket", False),
    ("Fuel", False),
    ("Electricity", False),
    ("Water", False),
    ("Telecom", False),
]

def create_category_service(data:CategoryCreate,current_user:UserModel,db:Session):
    existing_category=get_category_by_name(data.name,current_user.id,db)
    if existing_category is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Category already exists")
    new_category=CategoryModel(name=data.name,user_id=current_user.id)
    return add_category(db,new_category)

def get_categories_service(current_user:UserModel,db:Session):
    return get_categories_by_user_id(db,current_user.id)

def update_category_service(category_id:int,data:CategoryUpdate,current_user:UserModel,db:Session):
    category=get_category_by_id(db,category_id,current_user.id)
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Category not found")
    existing_category=get_category_by_name(data.name,current_user.id,db)
    if (existing_category is not None
            and existing_category.id != category.id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Category already exists")
    category.name=data.name
    return update_category_repo(db,category)

def delete_category_service(category_id:int,current_user:UserModel,db:Session):
    category=get_category_by_id(db,category_id,current_user.id)
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Category not found")
    delete_category_repo(db,category)

def create_default_categories_for_user(
    user_id: int,
    db: Session
):
    categories = []

    for name, is_system in DEFAULT_CATEGORIES:
        category = CategoryModel(
            name=name,
            is_system=is_system,
            user_id=user_id
        )

        db.add(category)
        categories.append(category)

    db.flush()

    return categories