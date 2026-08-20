from datetime import date
from decimal import Decimal

from app.models.bank_transaction_model import (
    BankTransactionModel,
    BankTransactionDirection,
)
from app.models.expense_model import ExpenseModel
from app.models.income_model import IncomeModel, IncomeStatus
from app.models.user_model import UserModel
from app.repositories.category_repository import get_category_by_name
from app.schemas.bank_transaction import BankTransactionImport
from app.schemas.recurring_income_rule import RecurringIncomeRuleCreate
from app.services.bank_automation_service import (
    run_bank_automation_service,
)
from app.services.categorization_service import (
    create_categorization_rule_service,
)
from app.services.recurring_income_rule_service import (
    create_recurring_income_rule_service,
)


class FakeBankAutomationProvider:

    def get_transactions(self):
        return [
            BankTransactionImport(
                external_transaction_id="automation_001",
                provider="fake_bank",
                amount=Decimal("65.00"),
                direction=BankTransactionDirection.OUTGOING,
                description="SHELL KIFISIAS",
                transaction_date=date(2026, 7, 10),
                value_date=date(2026, 7, 10),
                currency="EUR"
            ),

            BankTransactionImport(
                external_transaction_id="automation_002",
                provider="fake_bank",
                amount=Decimal("84.50"),
                direction=BankTransactionDirection.OUTGOING,
                description="SKLAVENITIS",
                transaction_date=date(2026, 7, 15),
                value_date=date(2026, 7, 15),
                currency="EUR"
            ),

            BankTransactionImport(
                external_transaction_id="automation_003",
                provider="fake_bank",
                amount=Decimal("2448.52"),
                direction=BankTransactionDirection.INCOMING,
                description="PAYROLL 07.2026",
                transaction_date=date(2026, 7, 30),
                value_date=date(2026, 7, 30),
                currency="EUR"
            ),

            BankTransactionImport(
                external_transaction_id="automation_004",
                provider="fake_bank",
                amount=Decimal("393.81"),
                direction=BankTransactionDirection.INCOMING,
                description="ΣΥΝΤ.Ε.Φ.Κ.Α. - ΣΥΝΤ",
                transaction_date=date(2026, 7, 24),
                value_date=date(2026, 7, 24),
                currency="EUR"
            ),

            BankTransactionImport(
                external_transaction_id="automation_005",
                provider="fake_bank",
                amount=Decimal("200.00"),
                direction=BankTransactionDirection.INCOMING,
                description="BONUS JULY",
                transaction_date=date(2026, 7, 25),
                value_date=date(2026, 7, 25),
                currency="EUR"
            ),
        ]


def test_bank_automation_processes_complete_monthly_flow(
    db_session,
    test_user,
    test_user_data
):
    current_user = (
        db_session.query(UserModel)
        .filter(
            UserModel.email == test_user_data["email"]
        )
        .first()
    )

    assert current_user is not None

    # -------------------------------------------------
    # Get default categories
    # -------------------------------------------------

    fuel_category = get_category_by_name(
        "Fuel",
        current_user.id,
        db_session
    )

    supermarket_category = get_category_by_name(
        "Supermarket",
        current_user.id,
        db_session
    )

    assert fuel_category is not None
    assert supermarket_category is not None

    # -------------------------------------------------
    # Create expense categorization rules
    # -------------------------------------------------

    create_categorization_rule_service(
        keyword="SHELL",
        category_id=fuel_category.id,
        current_user=current_user,
        db=db_session
    )

    create_categorization_rule_service(
        keyword="SKLAVENITIS",
        category_id=supermarket_category.id,
        current_user=current_user,
        db=db_session
    )

    # -------------------------------------------------
    # Create recurring income rules
    # -------------------------------------------------

    create_recurring_income_rule_service(
        RecurringIncomeRuleCreate(
            name="Payroll",
            expected_amount=Decimal("2448.52"),
            expected_day=30,
            transaction_keyword="PAYROLL"
        ),
        current_user,
        db_session
    )

    create_recurring_income_rule_service(
        RecurringIncomeRuleCreate(
            name="EFKA Pension",
            expected_amount=Decimal("393.81"),
            expected_day=24,
            transaction_keyword="ΣΥΝΤ.Ε.Φ.Κ.Α."
        ),
        current_user,
        db_session
    )

    provider = FakeBankAutomationProvider()

    # -------------------------------------------------
    # Run complete automation
    # -------------------------------------------------

    result = run_bank_automation_service(
        db=db_session,
        current_user=current_user,
        provider=provider,
        run_date=date(2026, 7, 1)
    )

    # 2 recurring rules produced 2 EXPECTED incomes
    assert result.generated_expected_incomes == 2

    # Fake bank returned 5 transactions
    assert result.transactions_received == 5
    assert result.transactions_created == 5
    assert result.transactions_skipped == 0

    # 2 charges
    assert result.outgoing_found == 2
    assert result.outgoing_processed == 2

    # 3 credits
    assert result.incoming_found == 3
    assert result.incoming_processed == 3

    # -------------------------------------------------
    # Verify Expenses
    # -------------------------------------------------

    expenses = (
        db_session.query(ExpenseModel)
        .filter(
            ExpenseModel.user_id == current_user.id
        )
        .all()
    )

    assert len(expenses) == 2

    expenses_by_description = {
        expense.description: expense
        for expense in expenses
    }

    shell_expense = expenses_by_description[
        "SHELL KIFISIAS"
    ]

    assert shell_expense.amount == Decimal("65.00")
    assert shell_expense.category_id == fuel_category.id
    assert shell_expense.bank_transaction_id is not None

    sklavenitis_expense = expenses_by_description[
        "SKLAVENITIS"
    ]

    assert sklavenitis_expense.amount == Decimal("84.50")
    assert (
        sklavenitis_expense.category_id
        == supermarket_category.id
    )
    assert sklavenitis_expense.bank_transaction_id is not None

    # -------------------------------------------------
    # Verify Incomes
    # -------------------------------------------------

    incomes = (
        db_session.query(IncomeModel)
        .filter(
            IncomeModel.user_id == current_user.id
        )
        .all()
    )

    assert len(incomes) == 3

    incomes_by_source = {
        income.source: income
        for income in incomes
    }

    payroll = incomes_by_source["Payroll"]

    assert payroll.amount == Decimal("2448.52")
    assert payroll.status == IncomeStatus.RECEIVED
    assert payroll.received_date == date(2026, 7, 30)
    assert payroll.recurring_income_rule_id is not None
    assert payroll.bank_transaction_id is not None

    efka = incomes_by_source["EFKA Pension"]

    assert efka.amount == Decimal("393.81")
    assert efka.status == IncomeStatus.RECEIVED
    assert efka.received_date == date(2026, 7, 24)
    assert efka.recurring_income_rule_id is not None
    assert efka.bank_transaction_id is not None

    bonus = incomes_by_source["BONUS JULY"]

    assert bonus.amount == Decimal("200.00")
    assert bonus.status == IncomeStatus.RECEIVED
    assert bonus.expected_date is None
    assert bonus.received_date == date(2026, 7, 25)
    assert bonus.recurring_income_rule_id is None
    assert bonus.bank_transaction_id is not None

    # -------------------------------------------------
    # Verify totals
    # -------------------------------------------------

    total_expenses = sum(
        (
            expense.amount
            for expense in expenses
        ),
        Decimal("0.00")
    )

    assert total_expenses == Decimal("149.50")

    total_income = sum(
        (
            income.amount
            for income in incomes
            if income.status == IncomeStatus.RECEIVED
        ),
        Decimal("0.00")
    )

    assert total_income == Decimal("3042.33")

    # -------------------------------------------------
    # All bank transactions must be processed
    # -------------------------------------------------

    bank_transactions = (
        db_session.query(BankTransactionModel)
        .filter(
            BankTransactionModel.user_id == current_user.id
        )
        .all()
    )

    assert len(bank_transactions) == 5

    assert all(
        transaction.processed_at is not None
        for transaction in bank_transactions
    )

    # -------------------------------------------------
    # Run automation again
    # -------------------------------------------------

    second_result = run_bank_automation_service(
        db=db_session,
        current_user=current_user,
        provider=provider,
        run_date=date(2026, 7, 1)
    )

    # Expected incomes already exist
    assert second_result.generated_expected_incomes == 0

    # Provider still returns 5,
    # but all are already stored
    assert second_result.transactions_received == 5
    assert second_result.transactions_created == 0
    assert second_result.transactions_skipped == 5

    # Nothing left to process
    assert second_result.outgoing_found == 0
    assert second_result.outgoing_processed == 0

    assert second_result.incoming_found == 0
    assert second_result.incoming_processed == 0

    # -------------------------------------------------
    # Verify no duplicates
    # -------------------------------------------------

    expenses_after_second_run = (
        db_session.query(ExpenseModel)
        .filter(
            ExpenseModel.user_id == current_user.id
        )
        .all()
    )

    incomes_after_second_run = (
        db_session.query(IncomeModel)
        .filter(
            IncomeModel.user_id == current_user.id
        )
        .all()
    )

    transactions_after_second_run = (
        db_session.query(BankTransactionModel)
        .filter(
            BankTransactionModel.user_id == current_user.id
        )
        .all()
    )

    assert len(expenses_after_second_run) == 2
    assert len(incomes_after_second_run) == 3
    assert len(transactions_after_second_run) == 5