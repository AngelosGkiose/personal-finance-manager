from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from starlette import status

from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db
from app.models.user_model import UserModel
from app.schemas.dashboard import MonthlyOverviewResponse
from app.services.dashboard_service import get_monthly_dashboard_service

router=APIRouter(prefix="/dashboard",tags=["dashboard"])


@router.get("/monthly",response_model=MonthlyOverviewResponse,status_code=status.HTTP_200_OK)
def get_monthly_overview(month: int | None = Query(default=None, ge=1, le=12),
    year: int | None = Query(default=None, gt=0),current_user:UserModel=Depends(get_current_user),db:Session=Depends(get_db)):
    return get_monthly_dashboard_service(month,year,current_user,db)