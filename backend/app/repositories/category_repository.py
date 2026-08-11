from sqlalchemy.orm import Session

from app.models.category_model import CategoryModel



def get_category_by_name(category_name:str,current_user_id:int,db:Session):
    return db.query(CategoryModel).filter(CategoryModel.name == category_name,CategoryModel.user_id==current_user_id).first()

def add_category(db:Session,new_category:CategoryModel,):
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

def get_categories_by_user_id(db:Session,user_id:int):
    return db.query(CategoryModel).filter(CategoryModel.user_id == user_id).all()

def get_category_by_id(db:Session,category_id:int,current_user_id:int):
    return db.query(CategoryModel).filter(CategoryModel.id == category_id,CategoryModel.user_id==current_user_id).first()


def update_category_repo(db:Session,category:CategoryModel):
    db.commit()
    db.refresh(category)
    return category

def delete_category_repo(db:Session,category:CategoryModel):
    db.delete(category)
    db.commit()
