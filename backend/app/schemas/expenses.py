from datetime import date, datetime

from pydantic import Field, BaseModel

from decimal import Decimal


class ExpenseCreate(BaseModel):
    amount:Decimal=Field(gt=0,max_digits=12,decimal_places=2)
    description:str=Field(min_length=0,max_length=255)
    expense_date:date
    category_id:int=Field(gt=0)


class ExpenseResponse(BaseModel):
    id:int
    amount:Decimal=Field(gt=0,max_digits=12,decimal_places=2)
    description:str
    expense_date:date
    category_id:int=Field(gt=0)
    created_at:datetime
    updated_at:datetime

    model_config = {
        "from_attributes": True
    }

class ExpenseUpdate(BaseModel):
    amount:Decimal=Field(gt=0,max_digits=12,decimal_places=2)
    description:str=Field(min_length=0,max_length=255)
    expense_date:date
    category_id:int=Field(gt=0)

