from datetime import datetime, date
from decimal import Decimal
from zoneinfo import ZoneInfo


from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.models.user_model import UserModel
from app.repositories.dashboard_repository import get_monthly_dashboard_totals, get_expenses_history, \
    get_pending_obligations_history, get_expected_income_history, get_received_income_history, \
    get_monthly_comparison_totals
from app.schemas.dashboard import MonthlyOverviewResponse, MonthlyComparisonResponse, ComparisonMetric


def shift_month(value: date, months: int) -> date:
    month_index = value.year * 12 + value.month - 1 + months

    year = month_index // 12
    month = month_index % 12 + 1

    return date(year, month, 1)


def rows_to_monthly_dict(rows):
    result = {}

    for row in rows:
        key = (
            int(row.year),
            int(row.month)
        )

        result[key] = row.total or Decimal("0.00")

    return result

def build_comparison_metric(
    current: Decimal,
    previous: Decimal
) -> ComparisonMetric:
    difference = current - previous

    if previous == Decimal("0.00"):
        percentage_change = None
    else:
        percentage_change = (
            (difference / previous) * Decimal("100")
        ).quantize(Decimal("0.01"))

    return ComparisonMetric(
        current=current,
        previous=previous,
        difference=difference,
        percentage_change=percentage_change
    )

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
        today=datetime.now(ZoneInfo("Europe/Athens")).date()
        month=today.month
        year=today.year
    totals = get_monthly_dashboard_totals(db,current_user.id,month,year)
    received_income=totals['received_income']
    expected_income=totals['expected_income']
    expenses= totals['expenses']
    pending_obligations=totals['pending_obligations']
    actual_balance=received_income-expenses
    projected_balance = (
            received_income
            + expected_income
            - expenses
            - pending_obligations
    )
    return MonthlyOverviewResponse(
        month=month,
        year=year,
        received_income=received_income,
        expected_income=expected_income,
        expenses=expenses,
        pending_obligations=pending_obligations,
        actual_balance=actual_balance,
        projected_balance=projected_balance
    )

def get_monthly_history_service(months:int,current_user: UserModel,db: Session):
    today=datetime.now(ZoneInfo("Europe/Athens")).date()
    current_month_start=date(today.year,today.month,1)
    start_date = shift_month(current_month_start,-(months - 1))
    end_date = shift_month(current_month_start,1)
    expenses_rows = get_expenses_history(db,current_user.id,start_date,end_date)
    received_income_rows = get_received_income_history(db,current_user.id,start_date,end_date)
    expected_income_rows = get_expected_income_history(db,current_user.id,start_date,end_date)
    pending_obligations_rows = get_pending_obligations_history(db,current_user.id,start_date,end_date)

    expenses = rows_to_monthly_dict(expenses_rows)
    received_income = rows_to_monthly_dict(received_income_rows)
    expected_income = rows_to_monthly_dict(expected_income_rows)
    pending_obligations = rows_to_monthly_dict(pending_obligations_rows)

    history = []
    for offset in range(months):
        selected_date = shift_month(
            current_month_start,
            -offset
        )
        key = (
            selected_date.year,
            selected_date.month
        )
        month_received_income = received_income.get(
            key,
            Decimal("0.00")
        )
        month_expected_income = expected_income.get(
            key,
            Decimal("0.00")
        )
        month_expenses = expenses.get(
            key,
            Decimal("0.00")
        )
        month_pending_obligations = pending_obligations.get(
            key,
            Decimal("0.00")
        )
        actual_balance = (
            month_received_income
            - month_expenses
        )
        projected_balance = (
            month_received_income
            + month_expected_income
            - month_expenses
            - month_pending_obligations
        )
        history.append(
            MonthlyOverviewResponse(
                month=selected_date.month,
                year=selected_date.year,
                received_income=month_received_income,
                expected_income=month_expected_income,
                expenses=month_expenses,
                pending_obligations=month_pending_obligations,
                actual_balance=actual_balance,
                projected_balance=projected_balance
            )
        )
    return history

def get_monthly_comparison_service(
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
        assert month is not None
        assert year is not None

        resolved_month = month
        resolved_year = year

    current_month_start = date(
        resolved_year,
        resolved_month,
        1
    )

    previous_month_date = shift_month(
        current_month_start,
        -1
    )

    totals = get_monthly_comparison_totals(
        db,
        current_user.id,
        resolved_month,
        resolved_year,
        previous_month_date.month,
        previous_month_date.year
    )

    current_totals = totals["current"]
    previous_totals = totals["previous"]

    current_actual_balance = (
        current_totals["received_income"]
        - current_totals["expenses"]
    )

    previous_actual_balance = (
        previous_totals["received_income"]
        - previous_totals["expenses"]
    )

    received_income_comparison = build_comparison_metric(
        current_totals["received_income"],
        previous_totals["received_income"]
    )

    expenses_comparison = build_comparison_metric(
        current_totals["expenses"],
        previous_totals["expenses"]
    )

    actual_balance_comparison = build_comparison_metric(
        current_actual_balance,
        previous_actual_balance
    )

    return MonthlyComparisonResponse(
        month=resolved_month,
        year=resolved_year,
        previous_month=previous_month_date.month,
        previous_year=previous_month_date.year,
        received_income=received_income_comparison,
        expenses=expenses_comparison,
        actual_balance=actual_balance_comparison
    )