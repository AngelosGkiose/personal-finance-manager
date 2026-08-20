
from datetime import date,datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from app.models.income_model import IncomeStatus


class IncomeCreate(BaseModel):
    amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    source:str=Field(min_length=1,max_length=255)
    expected_date: date | None = None

class IncomeResponse(BaseModel):
    id:int
    amount:Decimal
    source:str
    status:IncomeStatus
    expected_date:date|None
    received_date: date | None
    created_at: datetime
    updated_at:datetime

    model_config = {
        "from_attributes": True
    }

class IncomeReceive(BaseModel):
    received_date: date

class IncomeUpdate(BaseModel):
    amount: Decimal = Field(gt=0,max_digits=12, decimal_places=2)
    source: str = Field(min_length=1,max_length=255)

    expected_date: date | None = None


