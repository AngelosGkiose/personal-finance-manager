from sqlalchemy.orm import Session

from app.models.income_model import IncomeModel
from app.models.user_model import UserModel
from app.repositories.income_repository import create_income_repo
from app.schemas.income import IncomeCreate


def create_income_service(request:IncomeCreate,current_user:UserModel,db:Session):
    new_income = IncomeModel(amount=request.amount,source=request.source,expected_date=request.expected_date,user_id=current_user.id)

    return create_income_repo(db,new_income)