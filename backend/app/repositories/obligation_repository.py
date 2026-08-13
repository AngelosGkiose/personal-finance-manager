from sqlalchemy.orm import Session

from app.models.obligation_model import ObligationModel


def create_obligation_repo(db:Session,new_obligation:ObligationModel):
    db.add(new_obligation)
    db.commit()
    db.refresh(new_obligation)
    return new_obligation