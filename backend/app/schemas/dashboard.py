from datetime import date
from decimal import Decimal

from pydantic import BaseModel


class MonthlyOverviewResponse(BaseModel):
    month: int
    year: int
    received_income: Decimal
    expected_income: Decimal
    expenses: Decimal
    pending_obligations: Decimal
    monthly_balance: Decimal
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
    monthly_balance: ComparisonMetric


class CategoryExpenseResponse(BaseModel):
    category_id: int
    category_name: str
    amount: Decimal
    percentage: Decimal

class ExpensesByCategoryResponse(BaseModel):
    month: int
    year: int
    total_expenses: Decimal
    categories: list[CategoryExpenseResponse]

class CategoryExpenseComparison(BaseModel):

    category_id: int
    category_name: str
    current: Decimal
    previous: Decimal
    difference: Decimal
    percentage_change: Decimal | None

class ExpensesByCategoryComparisonResponse(BaseModel):

    month: int
    year: int
    previous_month: int
    previous_year: int
    categories: list[CategoryExpenseComparison]


class TopExpenseCategoryResponse(BaseModel):
    month: int
    year: int
    category_id: int | None
    category_name: str | None
    amount: Decimal
    percentage: Decimal

class UpcomingObligationResponse(BaseModel):
    id: int
    title: str
    amount: Decimal
    due_date: date
    category_id: int
    category_name: str
    days_until_due: int

class UpcomingObligationsResponse(BaseModel):
    days: int
    total_amount: Decimal
    obligations: list[UpcomingObligationResponse]


class OverdueObligationResponse(BaseModel):
    id: int
    title: str
    amount: Decimal
    due_date: date
    category_id: int
    category_name: str
    days_overdue: int

class OverdueObligationsResponse(BaseModel):
    count: int
    total_amount: Decimal
    obligations: list[OverdueObligationResponse]