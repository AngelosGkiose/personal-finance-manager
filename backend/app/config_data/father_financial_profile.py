from decimal import Decimal

from app.schemas.financial_profile import (
    CategorizationRuleSeed,
    FinancialProfileSeed,
    RecurringIncomeRuleSeed,
)


FATHER_FINANCIAL_PROFILE = FinancialProfileSeed(
    categories=[
        # εδώ αργότερα θα μπουν
        # τα categories από το πραγματικό history
    ],

    categorization_rules=[
        # εδώ αργότερα:
        # SHELL -> Fuel
        # SKLAVENITIS -> Supermarket
        # κτλ.
    ],

    recurring_income_rules=[
        RecurringIncomeRuleSeed(
            name="Payroll",
            expected_amount=Decimal("2448.52"),
            expected_day=30,
            transaction_keyword="PAYROLL"
        ),

        RecurringIncomeRuleSeed(
            name="EFKA Pension",
            expected_amount=Decimal("393.81"),
            expected_day=24,
            transaction_keyword="ΣΥΝΤ.Ε.Φ.Κ.Α."
        ),
    ]
)