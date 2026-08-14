from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from app.models.obligation_model import ObligationStatus


class ObligationCreate(BaseModel):
    title:str=Field(min_length=1,max_length=255)
    amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    due_date:date
    category_id:int=Field(gt=0)


class ObligationUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    amount: Decimal | None = Field(default=None, gt=0, max_digits=12, decimal_places=2)
    due_date: date | None = None
    category_id: int | None = Field(default=None, gt=0)


class ObligationPayment(BaseModel):
    paid_date: date


class ObligationResponse(BaseModel):
    id:int
    title:str
    amount:Decimal
    due_date:date
    status:ObligationStatus
    paid_date:date|None
    category_id:int
    expense_id: int | None
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }