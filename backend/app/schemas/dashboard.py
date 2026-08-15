from decimal import Decimal

from pydantic import BaseModel


class MonthlyOverviewResponse(BaseModel):
    month: int
    year: int
    received_income: Decimal
    expected_income: Decimal
    expenses: Decimal
    pending_obligations: Decimal
    actual_balance: Decimal
    projected_balance: Decimal