from datetime import date
from decimal import Decimal

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.category_model import CategoryModel
from app.models.expense_model import ExpenseModel
from app.models.income_model import IncomeModel, IncomeStatus
from app.models.obligation_model import ObligationModel, ObligationStatus


def get_monthly_dashboard_totals(db: Session,current_user_id: int,month: int,year: int):
    first_day=date(year,month,1)
    if month==12:
        next_month=date(year+1,1,1)
    else:
        next_month=date(year,month+1,1)
    received_income=db.query(func.sum(IncomeModel.amount)).filter(IncomeModel.user_id==current_user_id,IncomeModel.status==IncomeStatus.RECEIVED,IncomeModel.received_date<next_month, IncomeModel.received_date >= first_day).scalar()
    expected_income=db.query(func.sum(IncomeModel.amount)).filter(IncomeModel.user_id==current_user_id,IncomeModel.status==IncomeStatus.EXPECTED,IncomeModel.expected_date >= first_day,IncomeModel.expected_date < next_month).scalar()
    expenses=db.query(func.sum(ExpenseModel.amount)).filter(ExpenseModel.user_id==current_user_id,ExpenseModel.expense_date<next_month,ExpenseModel.expense_date >= first_day).scalar()
    pending_obligations=db.query(func.sum(ObligationModel.amount)).filter(ObligationModel.user_id==current_user_id,ObligationModel.status==ObligationStatus.PENDING,ObligationModel.due_date>=first_day,ObligationModel.due_date<next_month).scalar()
    return {
        "received_income": received_income or Decimal("0.00"),
        "expected_income": expected_income or Decimal("0.00"),
        "expenses": expenses or Decimal("0.00"),
        "pending_obligations": pending_obligations or Decimal("0.00")
    }

def get_expenses_history(db: Session,current_user_id: int,start_date: date,end_date: date):
    year = func.extract("year", ExpenseModel.expense_date).label("year")
    month = func.extract("month", ExpenseModel.expense_date).label("month")
    total = func.sum(ExpenseModel.amount).label("total")
    return db.query(year,month,total).filter(ExpenseModel.user_id == current_user_id,ExpenseModel.expense_date >= start_date,
        ExpenseModel.expense_date < end_date
    ).group_by(
        year,
        month
    ).all()
def get_received_income_history(
    db: Session,
    current_user_id: int,
    start_date: date,
    end_date: date
):
    year = func.extract("year", IncomeModel.received_date).label("year")
    month = func.extract("month", IncomeModel.received_date).label("month")
    total = func.sum(IncomeModel.amount).label("total")

    return db.query(
        year,
        month,
        total
    ).filter(
        IncomeModel.user_id == current_user_id,
        IncomeModel.status == IncomeStatus.RECEIVED,
        IncomeModel.received_date >= start_date,
        IncomeModel.received_date < end_date
    ).group_by(
        year,
        month
    ).all()

def get_expected_income_history(
    db: Session,
    current_user_id: int,
    start_date: date,
    end_date: date
):
    year = func.extract("year", IncomeModel.expected_date).label("year")
    month = func.extract("month", IncomeModel.expected_date).label("month")
    total = func.sum(IncomeModel.amount).label("total")

    return db.query(
        year,
        month,
        total
    ).filter(
        IncomeModel.user_id == current_user_id,
        IncomeModel.status == IncomeStatus.EXPECTED,
        IncomeModel.expected_date >= start_date,
        IncomeModel.expected_date < end_date
    ).group_by(
        year,
        month
    ).all()

def get_pending_obligations_history(
    db: Session,
    current_user_id: int,
    start_date: date,
    end_date: date
):
    year = func.extract("year", ObligationModel.due_date).label("year")
    month = func.extract("month", ObligationModel.due_date).label("month")
    total = func.sum(ObligationModel.amount).label("total")

    return db.query(
        year,
        month,
        total
    ).filter(
        ObligationModel.user_id == current_user_id,
        ObligationModel.status == ObligationStatus.PENDING,
        ObligationModel.due_date >= start_date,
        ObligationModel.due_date < end_date
    ).group_by(
        year,
        month
    ).all()


def get_monthly_comparison_totals(
    db: Session,
    current_user_id: int,
    current_month: int,
    current_year: int,
    previous_month: int,
    previous_year: int
):
    current_totals = get_monthly_dashboard_totals(
        db,
        current_user_id,
        current_month,
        current_year
    )

    previous_totals = get_monthly_dashboard_totals(
        db,
        current_user_id,
        previous_month,
        previous_year
    )

    return {
        "current": current_totals,
        "previous": previous_totals
    }
def get_expenses_by_category_repo(db:Session, current_user_id:int, month:int, year:int):
    first_day=date(year,month,1)
    if month == 12:
        next_month = date(year + 1, 1, 1)
    else:
        next_month = date(year, month + 1, 1)
    total = func.sum(ExpenseModel.amount).label("total")

    return db.query(
        CategoryModel.id.label("category_id"),
        CategoryModel.name.label("category_name"),
        total
    ).join(
        CategoryModel,
        ExpenseModel.category_id == CategoryModel.id
    ).filter(
        ExpenseModel.user_id == current_user_id,
        ExpenseModel.expense_date >= first_day,
        ExpenseModel.expense_date < next_month
    ).group_by(
        CategoryModel.id,
        CategoryModel.name
    ).order_by(
        total.desc()
    ).all()

