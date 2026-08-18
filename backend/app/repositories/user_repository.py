from sqlalchemy.orm import Session

from app.models.user_model import UserModel



def get_user_by_email(db:Session,email:str):
    return db.query(UserModel).filter(UserModel.email == email).first()

def add_user(db: Session, user: UserModel):
    db.add(user)
    db.flush()
    return user

def get_user_by_id(db:Session,user_id:int):
    return db.query(UserModel).filter(UserModel.id == user_id).first()