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

class ComparisonMetric(BaseModel):
    current: Decimal
    previous: Decimal
    difference: Decimal
    percentage_change: Decimal | None

class MonthlyComparisonResponse(BaseModel):
    month: int
    year: int
    previous_month: int
    previous_year: int

    received_income: ComparisonMetric
    expenses: ComparisonMetric
    actual_balance: ComparisonMetric