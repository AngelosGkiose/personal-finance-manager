from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.models.obligation_model import ObligationModel
from app.models.user_model import UserModel
from app.repositories.category_repository import get_category_by_id
from app.repositories.obligation_repository import create_obligation_repo


def  create_obligation_service(request,current_user:UserModel,db:Session):
    category=get_category_by_id(db,request.category_id,current_user.id)
    if category is  None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Category not found")
    new_obligation = ObligationModel(title=request.title,amount=request.amount,due_date=request.due_date,category_id=category.id,user_id=current_user.id,)
    return create_obligation_repo(db,new_obligation)