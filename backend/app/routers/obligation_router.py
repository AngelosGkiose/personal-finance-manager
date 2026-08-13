from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db
from app.models.user_model import UserModel
from app.schemas.obligations import ObligationResponse, ObligationCreate
from app.services.obligation_service import create_obligation_service, get_obligations_service, \
    get_obligation_by_id_service

router=APIRouter(prefix="/obligations",tags=["obligations"])

@router.post("/",response_model=ObligationResponse,status_code=status.HTTP_201_CREATED)
def create_obligation(request:ObligationCreate,current_user:UserModel=Depends(get_current_user),db:Session=Depends(get_db)):
    return create_obligation_service(request,current_user,db)

@router.get("/",response_model=list[ObligationResponse],status_code=status.HTTP_200_OK)
def get_obligations(current_user:UserModel=Depends(get_current_user),db:Session=Depends(get_db)):
    return get_obligations_service(current_user,db)


@router.get("/{obligation_id}",response_model=ObligationResponse,status_code=status.HTTP_200_OK)
def get_obligation_by_id(obligation_id:int,current_user:UserModel=Depends(get_current_user),db:Session=Depends(get_db)):
    return get_obligation_by_id_service(obligation_id,current_user,db)
