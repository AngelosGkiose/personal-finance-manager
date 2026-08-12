from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.models.income_model import IncomeModel, IncomeStatus
from app.models.user_model import UserModel
from app.repositories.income_repository import create_income_repo, get_incomes_repo, get_income_by_id_repo, \
    update_income_repo, delete_income_repo
from app.schemas.income import IncomeCreate, IncomeReceive, IncomeUpdate


def create_income_service(request:IncomeCreate,current_user:UserModel,db:Session):
    new_income = IncomeModel(amount=request.amount,source=request.source,expected_date=request.expected_date,user_id=current_user.id)

    return create_income_repo(db,new_income)


def get_incomes_service(current_user:UserModel,db:Session):
    return get_incomes_repo(db,current_user.id)

def get_income_by_id_service(income_id:int,current_user:UserModel,db:Session):
   income=get_income_by_id_repo(db,income_id,current_user.id)
   if income is None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Income not found")
   return income

def update_income_received_service(income_id:int,request:IncomeReceive,current_user:UserModel,db:Session):
    income=get_income_by_id_repo(db,income_id,current_user.id)
    if income is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Income not found")
    if income.status==IncomeStatus.RECEIVED:
        return income
    income.status=IncomeStatus.RECEIVED
    income.received_date=request.received_date
    return update_income_repo(db,income)


def update_income_service(income_id:int,request:IncomeUpdate,current_user:UserModel,db:Session):
    income=get_income_by_id_repo(db,income_id,current_user.id)
    if income is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Income not found")
    if income.status==IncomeStatus.RECEIVED:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Received income cannot be modified")
    income.amount=request.amount
    income.source=request.source
    income.expected_date=request.expected_date
    return update_income_repo(db, income)

def delete_income_service(income_id:int,current_user:UserModel,db:Session):
    income=get_income_by_id_repo(db,income_id,current_user.id)
    if income is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Income not found")
    if income.status==IncomeStatus.RECEIVED:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Received income cannot be deleted")
    return delete_income_repo(db, income)