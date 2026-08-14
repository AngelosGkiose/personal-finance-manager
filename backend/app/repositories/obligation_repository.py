from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.expense_model import ExpenseModel
from app.models.obligation_model import ObligationModel


def create_obligation_repo(db:Session,new_obligation:ObligationModel):
    db.add(new_obligation)
    db.commit()
    db.refresh(new_obligation)
    return new_obligation

def get_obligations_repo(db:Session, current_user_id:int):
    return db.query(ObligationModel).filter(ObligationModel.user_id == current_user_id).order_by(ObligationModel.due_date.asc()).all()

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