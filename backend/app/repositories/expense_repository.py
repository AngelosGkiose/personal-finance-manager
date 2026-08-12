from sqlalchemy.orm import Session
from datetime import date

from app.models.expense_model import ExpenseModel



def add_expense(db:Session,expense:ExpenseModel):
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


def get_expenses_repo(db:Session,current_user_id:int,month:int|None,year:int|None,category_id:int|None):
    query=db.query(ExpenseModel).filter(ExpenseModel.user_id==current_user_id)
    if month is not None and year is not None:
        start_date=date(year,month,1)
        if month==12:
            end_date=date(year+1,1,1)
        else:
            end_date=date(year,month+1,1)
        query=query.filter(ExpenseModel.expense_date>=start_date,ExpenseModel.expense_date<end_date)
    if category_id is not None:
        query=query.filter(ExpenseModel.category_id==category_id)
    return query.order_by(ExpenseModel.expense_date.desc()).all()



def get_expense_by_id_repo(db:Session,expense_id:int,current_user_id:int):
    return db.query(ExpenseModel).filter(ExpenseModel.user_id == current_user_id,ExpenseModel.id == expense_id).first()

def update_expense_repo(db:Session,expense:ExpenseModel):
    db.commit()
    db.refresh(expense)
    return expense

def delete_expense_repo(db:Session,expense:ExpenseModel):
    db.delete(expense)
    db.commit()