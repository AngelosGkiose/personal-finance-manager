from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.models.obligation_model import ObligationModel, ObligationStatus
from app.models.user_model import UserModel
from app.repositories.category_repository import get_category_by_id
from app.repositories.obligation_repository import create_obligation_repo, get_obligations_repo, \
    get_obligation_by_id_repo, update_obligation_repo
from app.schemas.obligations import ObligationUpdate


def  create_obligation_service(request,current_user:UserModel,db:Session):
    category=get_category_by_id(db,request.category_id,current_user.id)
    if category is  None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Category not found")
    new_obligation = ObligationModel(title=request.title,amount=request.amount,due_date=request.due_date,category_id=category.id,user_id=current_user.id,)
    return create_obligation_repo(db,new_obligation)

def get_obligations_service(current_user:UserModel,db:Session):
    return get_obligations_repo(db,current_user.id)

def get_obligation_by_id_service(obligation_id,current_user:UserModel,db:Session):
    obligation= get_obligation_by_id_repo(db, obligation_id, current_user.id)
    if obligation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Obligation not found")
    return obligation


def update_obligation_service(obligation_id:int,request:ObligationUpdate,current_user:UserModel,db:Session):
    obligation = get_obligation_by_id_repo(db, obligation_id, current_user.id)
    if obligation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Obligation not found")
    if obligation.status==ObligationStatus.PAID:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Obligation cannot be modified")
    update_data = request.model_dump(exclude_unset=True)

    if "category_id" in update_data:
        category = get_category_by_id(db, update_data["category_id"], current_user.id)

        if category is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    for field, value in update_data.items():
        setattr(obligation, field, value)

    return update_obligation_repo(db, obligation)