from datetime import date

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.expense_model import ExpenseModel
from app.models.obligation_model import ObligationModel, ObligationStatus
from app.schemas.obligations import ObligationFilterStatus


def create_obligation_repo(db:Session,new_obligation:ObligationModel):
    db.add(new_obligation)
    db.commit()
    db.refresh(new_obligation)
    return new_obligation

def get_obligations_repo(db:Session, current_user_id:int,month:int,year:int,obligation_status:ObligationFilterStatus,category_id:int):
    query=db.query(ObligationModel).filter(ObligationModel.user_id==current_user_id)
    if category_id is not None:
        query=query.filter(ObligationModel.category_id==category_id)
    if month is not None and year is not None:
        first_day = date(year, month, 1)
        if month == 12:
            next_month = date(year + 1, 1, 1)
        else:
            next_month = date(year, month + 1, 1)
        query = query.filter(ObligationModel.due_date >= first_day,ObligationModel.due_date < next_month)

    if obligation_status == ObligationFilterStatus.PAID:
        query = query.filter(ObligationModel.status == ObligationStatus.PAID)

    elif obligation_status == ObligationFilterStatus.PENDING:
        query = query.filter(ObligationModel.status == ObligationStatus.PENDING,ObligationModel.due_date >= date.today())

    elif obligation_status == ObligationFilterStatus.OVERDUE:
        query = query.filter( ObligationModel.status == ObligationStatus.PENDING,ObligationModel.due_date < date.today())
        
    return query.order_by(ObligationModel.due_date.asc()).all()

def get_obligation_by_id_repo(db:Session,obligation_id:int, current_user_id:int):
    return db.query(ObligationModel).filter(ObligationModel.user_id == current_user_id,ObligationModel.id==obligation_id).first()

def update_obligation_repo(db:Session,new_obligation:ObligationModel):
    db.commit()
    db.refresh(new_obligation)
    return new_obligation

def delete_obligation_repo(db:Session,obligation:ObligationModel):
    db.delete(obligation)
    db.commit()

def pay_obligation_repo(db: Session, obligation: ObligationModel, expense: ExpenseModel):
    try:
        db.add(expense)
        db.flush()

        obligation.expense_id = expense.id

        db.commit()

        db.refresh(obligation)

        return obligation

    except SQLAlchemyError:
        db.rollback()
        raise