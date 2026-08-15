from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.models.user_model import UserModel
from app.repositories.dashboard_repository import get_monthly_dashboard_totals
from app.schemas.dashboard import MonthlyOverviewResponse


def get_monthly_dashboard_service(
    month: int | None,
    year: int | None,
    current_user: UserModel,
    db: Session
):
    if (month is None) != (year is None):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Month and year must be provided together"
        )

    if month is None and year is None:
        today = datetime.now(ZoneInfo("Europe/Athens")).date()
        resolved_month = today.month
        resolved_year = today.year
    else:
        resolved_month = month
        resolved_year = year

    totals = get_monthly_dashboard_totals(
        db,
        current_user.id,
        resolved_month,
        resolved_year
    )

    received_income = totals["received_income"]
    expected_income = totals["expected_income"]
    expenses = totals["expenses"]
    pending_obligations = totals["pending_obligations"]

    actual_balance = received_income - expenses

    projected_balance = (
        received_income
        + expected_income
        - expenses
        - pending_obligations
    )

    return MonthlyOverviewResponse(
        month=resolved_month,
        year=resolved_year,
        received_income=received_income,
        expected_income=expected_income,
        expenses=expenses,
        pending_obligations=pending_obligations,
        actual_balance=actual_balance,
        projected_balance=projected_balance
    )