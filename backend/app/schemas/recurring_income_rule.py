from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class RecurringIncomeRuleCreate(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=100
    )

    expected_amount: Decimal = Field(
        gt=0
    )

    expected_day: int = Field(
        ge=1,
        le=31
    )

    transaction_keyword: str | None = Field(
        default=None,
        max_length=100
    )


class RecurringIncomeRuleUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100
    )

    expected_amount: Decimal | None = Field(
        default=None,
        gt=0
    )

    expected_day: int | None = Field(
        default=None,
        ge=1,
        le=31
    )

    transaction_keyword: str | None = Field(
        default=None,
        max_length=100
    )

    is_active: bool | None = None


class RecurringIncomeRuleResponse(BaseModel):
    id: int
    name: str
    expected_amount: Decimal
    expected_day: int
    transaction_keyword: str | None
    is_active: bool
    created_at: datetime

    model_config = {
        "from_attributes": True
    }