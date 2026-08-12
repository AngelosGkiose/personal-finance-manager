from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import current_user

from app.models.income_model import IncomeModel



def create_income_repo(db:Session,new_income:IncomeModel):
    db.add(new_income)
    db.commit()
    db.refresh(new_income)
    return new_income

def get_incomes_repo(db:Session,current_user_id:int):
    return db.query(IncomeModel).filter(IncomeModel.user_id == current_user_id).all()


def get_income_by_id_repo(db:Session,income_id:int,current_user_id:int):
    return db.query(IncomeModel).filter(IncomeModel.user_id == current_user_id,IncomeModel.id == income_id).first()


def update_income_repo(db:Session,income:IncomeModel):
    db.commit()
    db.refresh(income)
    return income