from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from starlette import status

from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db
from app.models.user_model import UserModel
from app.schemas.obligations import ObligationResponse, ObligationCreate, ObligationUpdate, ObligationPayment, \
    ObligationFilterStatus
from app.services.obligation_service import create_obligation_service, get_obligations_service, \
    get_obligation_by_id_service, update_obligation_service, delete_obligation_service, pay_obligation_service

router=APIRouter(prefix="/obligations",tags=["obligations"])

@router.post("/",response_model=ObligationResponse,status_code=status.HTTP_201_CREATED)
def create_obligation(request:ObligationCreate,current_user:UserModel=Depends(get_current_user),db:Session=Depends(get_db)):
    return create_obligation_service(request,current_user,db)

@router.get("/",response_model=list[ObligationResponse],status_code=status.HTTP_200_OK)
def get_obligations(month: int | None = Query(default=None, ge=1, le=12),year: int | None = Query(default=None, gt=0),
                    obligation_status: ObligationFilterStatus | None = Query(default=None, alias="status"),category_id: int | None = Query(default=None, gt=0),
                    current_user:UserModel=Depends(get_current_user),db:Session=Depends(get_db)):
    return get_obligations_service(month,year,obligation_status,category_id,current_user,db)


@router.get("/{obligation_id}",response_model=ObligationResponse,status_code=status.HTTP_200_OK)
def get_obligation_by_id(obligation_id:int,current_user:UserModel=Depends(get_current_user),db:Session=Depends(get_db)):
    return get_obligation_by_id_service(obligation_id,current_user,db)


@router.patch("/{obligation_id}",response_model=ObligationResponse,status_code=status.HTTP_200_OK)
def update_obligation(obligation_id:int,request:ObligationUpdate,current_user:UserModel=Depends(get_current_user),db:Session=Depends(get_db)):
    return update_obligation_service(obligation_id,request,current_user,db)

@router.delete("/{obligation_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_obligation(obligation_id:int,current_user:UserModel=Depends(get_current_user),db:Session=Depends(get_db)):
    return delete_obligation_service(obligation_id,current_user,db)

@router.patch("/{obligation_id}/pay",response_model=ObligationResponse,status_code=status.HTTP_200_OK)
def pay_obligation(obligation_id:int,request:ObligationPayment,current_user:UserModel=Depends(get_current_user),db:Session=Depends(get_db)):
    return pay_obligation_service(obligation_id,request,current_user,db)