from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db
from app.models.user_model import UserModel
from app.schemas.income import IncomeResponse, IncomeCreate
from app.services.income_service import create_income_service

router = APIRouter(prefix="/incomes", tags=["incomes"])

@router.post("/",response_model=IncomeResponse,status_code=status.HTTP_201_CREATED)
def create_income(request:IncomeCreate,current_user:UserModel=Depends(get_current_user),db:Session=Depends(get_db)):
    return create_income_service(request,current_user,db)