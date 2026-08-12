from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db
from app.models.user_model import UserModel
from app.schemas.expenses import ExpenseResponse, ExpenseCreate, ExpenseUpdate
from app.services.expense_service import create_expense_service, get_expenses_service, get_expense_by_id_service, \
    delete_expense_service, update_expense_service

router = APIRouter(prefix="/expenses",tags=["expenses"])

@router.post("/",response_model=ExpenseResponse,status_code=status.HTTP_201_CREATED)
def create_expense(request: ExpenseCreate,current_user:UserModel=Depends(get_current_user),db:Session=Depends(get_db)):
    return create_expense_service(request,current_user,db)


@router.get("/",response_model=list[ExpenseResponse],status_code=status.HTTP_200_OK)
def get_expenses(current_user:UserModel=Depends(get_current_user),db:Session=Depends(get_db)):
    return get_expenses_service(current_user,db)

@router.get("/{expense_id}",response_model=ExpenseResponse,status_code=status.HTTP_200_OK)
def get_expense_by_id(expense_id:int,current_user:UserModel=Depends(get_current_user),db:Session=Depends(get_db)):
    return get_expense_by_id_service(expense_id,current_user,db)

@router.delete("/{expense_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(expense_id:int,current_user:UserModel=Depends(get_current_user),db:Session=Depends(get_db)):
    delete_expense_service(expense_id,current_user,db)

@router.put("/{expense_id}",response_model=ExpenseResponse,status_code=status.HTTP_200_OK)
def update_expense(expense_id:int,request:ExpenseUpdate,current_user:UserModel=Depends(get_current_user),db:Session=Depends(get_db)):
    return update_expense_service(expense_id,request,current_user,db)