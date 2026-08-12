from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.models.expense_model import ExpenseModel
from app.models.user_model import UserModel
from app.repositories.category_repository import get_category_by_id
from app.repositories.expense_repository import add_expense, get_expenses_repo, get_expense_by_id_repo, \
    delete_expense_repo, update_expense_repo
from app.schemas.expenses import ExpenseCreate, ExpenseUpdate


def create_expense_service(request:ExpenseCreate,current_user:UserModel,db:Session):
    category=get_category_by_id(db,request.category_id,current_user.id)
    if category is  None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Category not Found")
    expense=ExpenseModel(amount=request.amount,
                         description=request.description,expense_date=request.expense_date,
                         category_id=category.id,user_id=current_user.id)
    return add_expense(db,expense)

def get_expenses_service(current_user:UserModel,db:Session):
    return get_expenses_repo(db,current_user.id)

def get_expense_by_id_service(expense_id:int,current_user:UserModel,db:Session):
    expense=get_expense_by_id_repo(db,expense_id,current_user.id)
    if expense is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Expense not Found")
    return expense

def update_expense_service(expense_id:int,request:ExpenseUpdate,current_user:UserModel,db:Session):
    expense=get_expense_by_id_repo(db,expense_id,current_user.id)
    if expense is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Expense not Found")
    category=get_category_by_id(db,request.category_id,current_user.id)
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Category not Found")
    expense.amount = request.amount
    expense.description = request.description
    expense.expense_date = request.expense_date
    expense.category_id = category.id

    return update_expense_repo(db, expense)

def delete_expense_service(expense_id:int,current_user:UserModel,db:Session):
    expense=get_expense_by_id_repo(db,expense_id,current_user.id)
    if expense is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Expense not Found")
    return delete_expense_repo(db,expense)