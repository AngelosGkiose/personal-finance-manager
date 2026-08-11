from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.models.expense_model import ExpenseModel
from app.models.user_model import UserModel
from app.repositories.category_repository import get_category_by_id
from app.repositories.expense_repository import add_expense
from app.schemas.expenses import ExpenseCreate


def create_expense_service(request:ExpenseCreate,current_user:UserModel,db:Session):
    category=get_category_by_id(db,request.category_id,current_user.id)
    if category is  None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Category not Found")
    expense=ExpenseModel(amount=request.amount,
                         description=request.description,expense_date=request.expense_date,
                         category_id=category.id,user_id=current_user.id)
    return add_expense(db,expense)
