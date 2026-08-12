from sqlalchemy.orm import Session

from app.models.expense_model import ExpenseModel



def add_expense(db:Session,expense:ExpenseModel):
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


def get_expenses_repo(db:Session,current_user_id:int):
    return db.query(ExpenseModel).filter(ExpenseModel.user_id == current_user_id).all()

def get_expense_by_id_repo(db:Session,expense_id:int,current_user_id:int):
    return db.query(ExpenseModel).filter(ExpenseModel.user_id == current_user_id,ExpenseModel.id == expense_id).first()

def update_expense_repo(db:Session,expense:ExpenseModel):
    db.commit()
    db.refresh(expense)
    return expense

def delete_expense_repo(db:Session,expense:ExpenseModel):
    db.delete(expense)
    db.commit()