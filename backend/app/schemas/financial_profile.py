from decimal import Decimal

from pydantic import BaseModel, Field


class CategorizationRuleSeed(BaseModel):
    keyword: str = Field(
        min_length=1,
        max_length=100
    )

    category_name: str = Field(
        min_length=1,
        max_length=100
    )


class RecurringIncomeRuleSeed(BaseModel):
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


class FinancialProfileSeed(BaseModel):
    categories: list[str] = Field(
        default_factory=list
    )

    categorization_rules: list[
        CategorizationRuleSeed
    ] = Field(
        default_factory=list
    )

    recurring_income_rules: list[
        RecurringIncomeRuleSeed
    ] = Field(
        default_factory=list
    )

class FinancialProfileInitializationResult(BaseModel):
    categories_created: int
    categorization_rules_created: int
    recurring_income_rules_created: int