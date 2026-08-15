from datetime import date
from decimal import Decimal

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.expense_model import ExpenseModel
from app.models.income_model import IncomeModel, IncomeStatus
from app.models.obligation_model import ObligationModel, ObligationStatus


def get_monthly_dashboard_totals(
    db: Session,
    current_user_id: int,
    month: int,
    year: int
):
    first_day = date(year, month, 1)

    if month == 12:
        next_month = date(year + 1, 1, 1)
    else:
        next_month = date(year, month + 1, 1)

    received_income = db.query(
        func.sum(IncomeModel.amount)
    ).filter(
        IncomeModel.user_id == current_user_id,
        IncomeModel.status == IncomeStatus.RECEIVED,
        IncomeModel.received_date >= first_day,
        IncomeModel.received_date < next_month
    ).scalar()

    expected_income = db.query(
        func.sum(IncomeModel.amount)
    ).filter(
        IncomeModel.user_id == current_user_id,
        IncomeModel.status == IncomeStatus.EXPECTED,
        IncomeModel.expected_date >= first_day,
        IncomeModel.expected_date < next_month
    ).scalar()

    expenses = db.query(
        func.sum(ExpenseModel.amount)
    ).filter(
        ExpenseModel.user_id == current_user_id,
        ExpenseModel.expense_date >= first_day,
        ExpenseModel.expense_date < next_month
    ).scalar()

    pending_obligations = db.query(
        func.sum(ObligationModel.amount)
    ).filter(
        ObligationModel.user_id == current_user_id,
        ObligationModel.status == ObligationStatus.PENDING,
        ObligationModel.due_date >= first_day,
        ObligationModel.due_date < next_month
    ).scalar()

    return {
        "received_income": received_income or Decimal("0.00"),
        "expected_income": expected_income or Decimal("0.00"),
        "expenses": expenses or Decimal("0.00"),
        "pending_obligations": pending_obligations or Decimal("0.00")
    }