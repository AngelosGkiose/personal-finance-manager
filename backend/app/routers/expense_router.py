from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db
from app.models.user_model import UserModel
from app.schemas.expenses import ExpenseResponse, ExpenseCreate
from app.services.expense_service import create_expense_service

router = APIRouter(prefix="/expenses",tags=["expenses"])

@router.post("/",response_model=ExpenseResponse,status_code=status.HTTP_201_CREATED)
def create_expense(request: ExpenseCreate,current_user:UserModel=Depends(get_current_user),db:Session=Depends(get_db)):
    return create_expense_service(request,current_user,db)