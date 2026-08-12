from sqlalchemy.orm import Session

from app.models.income_model import IncomeModel


def create_income_repo(db:Session,new_income:IncomeModel):
    db.add(new_income)
    db.commit()
    db.refresh(new_income)
    return new_income