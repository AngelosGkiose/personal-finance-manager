from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from starlette import status

from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db
from app.models.user_model import UserModel
from app.schemas.dashboard import MonthlyOverviewResponse, MonthlyComparisonResponse, ExpensesByCategoryResponse, \
    ExpensesByCategoryComparisonResponse, TopExpenseCategoryResponse, UpcomingObligationsResponse
from app.services.dashboard_service import get_monthly_dashboard_service, get_monthly_history_service, \
    get_monthly_comparison_service, get_expenses_by_category_service, get_expenses_by_category_comparison_service, \
    get_top_expense_category_service, get_upcoming_obligations_service

router=APIRouter(prefix="/dashboard",tags=["dashboard"])


@router.get("/monthly",response_model=MonthlyOverviewResponse,status_code=status.HTTP_200_OK)
def get_monthly_overview(month: int | None = Query(default=None, ge=1, le=12),
    year: int | None = Query(default=None, gt=0),current_user:UserModel=Depends(get_current_user),db:Session=Depends(get_db)):
    return get_monthly_dashboard_service(month,year,current_user,db)

@router.get("/history",response_model=list[MonthlyOverviewResponse],status_code=status.HTTP_200_OK)
def get_monthly_history(months: int =Query( ge=1, le=24),current_user:UserModel=Depends(get_current_user),db:Session=Depends(get_db)):
    return get_monthly_history_service(months,current_user,db)

@router.get("/comparison",response_model=MonthlyComparisonResponse,status_code=status.HTTP_200_OK)
def get_monthly_comparison(month: int | None = Query(default=None, ge=1, le=12),year: int | None = Query(default=None, gt=0),
                           current_user: UserModel = Depends(get_current_user),db: Session = Depends(get_db)):
    return get_monthly_comparison_service(month,year, current_user,db)

@router.get("/expenses-by-category",response_model=ExpensesByCategoryResponse,status_code=status.HTTP_200_OK)
def get_expenses_by_category(month: int | None = Query(default=None, ge=1, le=12),year: int | None = Query(default=None, gt=0),current_user:UserModel = Depends(get_current_user),db:Session = Depends(get_db)):
    return get_expenses_by_category_service(month,year,current_user,db)

@router.get("/expenses-by-category/comparison",response_model=ExpensesByCategoryComparisonResponse,status_code=status.HTTP_200_OK)
def get_expenses_by_category_comparison(month: int | None = Query(default=None, ge=1, le=12), year: int | None = Query(default=None, gt=0),current_user: UserModel = Depends(get_current_user),db: Session = Depends(get_db)):
    return get_expenses_by_category_comparison_service(month,year,current_user,db)

@router.get("/top-expense-category",response_model=TopExpenseCategoryResponse,status_code=status.HTTP_200_OK)
def get_top_expense_category(month: int | None = Query(default=None, ge=1, le=12),year: int | None = Query(default=None, gt=0),
                             current_user: UserModel = Depends(get_current_user),db: Session = Depends(get_db)):
    return get_top_expense_category_service(month,year,current_user,db)

@router.get("/upcoming-obligations",response_model=UpcomingObligationsResponse,status_code=status.HTTP_200_OK)
def get_upcoming_obligations(days: int = Query(default=7, ge=1, le=30),current_user: UserModel = Depends(get_current_user),db: Session = Depends(get_db)):
    return get_upcoming_obligations_service(days,current_user,db)