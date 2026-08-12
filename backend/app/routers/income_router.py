from winreg import QueryInfoKey

from fastapi import APIRouter, Depends,Query
from sqlalchemy.orm import Session
from starlette import status

from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db
from app.models.income_model import IncomeStatus
from app.models.user_model import UserModel
from app.schemas.income import IncomeResponse, IncomeCreate, IncomeReceive, IncomeUpdate
from app.services.income_service import create_income_service, get_incomes_service, get_income_by_id_service, \
    update_income_received_service, update_income_service, delete_income_service

router = APIRouter(prefix="/incomes", tags=["incomes"])

@router.post("/",response_model=IncomeResponse,status_code=status.HTTP_201_CREATED)
def create_income(request:IncomeCreate,current_user:UserModel=Depends(get_current_user),db:Session=Depends(get_db)):
    return create_income_service(request,current_user,db)

@router.get("/",response_model=list[IncomeResponse],status_code=status.HTTP_200_OK)
def get_incomes(month:int|None=Query(deafult=None,gt=0,le=12),year:int|None=Query(default=None,gt=0),
                income_status:IncomeStatus|None=Query(default=None,alias="status"),
                current_user:UserModel=Depends(get_current_user),db:Session=Depends(get_db)):
    return get_incomes_service(month,year,income_status,current_user,db)


@router.get("/{income_id}",response_model=IncomeResponse,status_code=status.HTTP_200_OK)
def get_income_by_id(income_id:int,current_user:UserModel=Depends(get_current_user),db:Session=Depends(get_db)):
    return get_income_by_id_service(income_id,current_user,db)

@router.patch("/{income_id}/receive",response_model=IncomeResponse,status_code=status.HTTP_200_OK)
def update_income_received(income_id:int,request:IncomeReceive,current_user:UserModel=Depends(get_current_user),db:Session=Depends(get_db)):
    return update_income_received_service(income_id,request,current_user,db)

@router.put("/{income_id}",response_model=IncomeResponse,status_code=status.HTTP_200_OK)
def update_income(income_id:int,request:IncomeUpdate,current_user:UserModel=Depends(get_current_user),db:Session=Depends(get_db)):
    return update_income_service(income_id,request,current_user,db)

@router.delete("/{income_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_income(income_id:int,current_user:UserModel=Depends(get_current_user),db:Session=Depends(get_db)):
    return delete_income_service(income_id,current_user,db)
