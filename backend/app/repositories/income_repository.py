from datetime import date

from sqlalchemy import or_, and_
from sqlalchemy.orm import Session


from app.models.income_model import IncomeModel, IncomeStatus


def create_income_repo(db:Session,new_income:IncomeModel):
    db.add(new_income)
    db.commit()
    db.refresh(new_income)
    return new_income


def get_incomes_repo(db: Session, current_user_id: int, month: int | None, year: int | None, income_status: IncomeStatus | None):
    query = db.query(IncomeModel).filter(IncomeModel.user_id == current_user_id)

    if income_status is not None:
        query = query.filter(IncomeModel.status == income_status)
    if month is not None and year is not None:
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1)
        else:
            end_date = date(year, month + 1, 1)

        if income_status == IncomeStatus.EXPECTED:
            query = query.filter(IncomeModel.expected_date >= start_date, IncomeModel.expected_date < end_date)

        elif income_status == IncomeStatus.RECEIVED:
            query = query.filter(IncomeModel.received_date >= start_date, IncomeModel.received_date < end_date)
        else:
            query = query.filter(or_(and_(IncomeModel.status == IncomeStatus.EXPECTED, IncomeModel.expected_date >= start_date, IncomeModel.expected_date < end_date), and_(IncomeModel.status == IncomeStatus.RECEIVED, IncomeModel.received_date >= start_date, IncomeModel.received_date < end_date)))

    return query.order_by(IncomeModel.expected_date.desc()).all()


def get_income_by_id_repo(db:Session,income_id:int,current_user_id:int):
    return db.query(IncomeModel).filter(IncomeModel.user_id == current_user_id,IncomeModel.id == income_id).first()


def update_income_repo(db:Session,income:IncomeModel):
    db.commit()
    db.refresh(income)
    return income

def delete_income_repo(db:Session,income:IncomeModel):
    db.delete(income)
    db.commit()

def get_income_by_recurring_rule_and_expected_date(
    db: Session,
    current_user_id: int,
    recurring_income_rule_id: int,
    expected_date
):
    return (
        db.query(IncomeModel)
        .filter(
            IncomeModel.user_id == current_user_id,
            IncomeModel.recurring_income_rule_id
            == recurring_income_rule_id,
            IncomeModel.expected_date == expected_date
        )
        .first()
    )