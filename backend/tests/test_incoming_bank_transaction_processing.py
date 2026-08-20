from datetime import date
from decimal import Decimal

from app.models.bank_transaction_model import BankTransactionModel
from app.models.income_model import IncomeModel, IncomeStatus
from app.models.user_model import UserModel
from app.schemas.bank_transaction import BankTransactionImport
from app.schemas.recurring_income_rule import RecurringIncomeRuleCreate
from app.models.bank_transaction_model import BankTransactionDirection
from app.services.bank_sync_service import (
    sync_bank_transactions_service,
)
from app.services.bank_transaction_processor_service import (
    process_incoming_bank_transactions_service,
)
from app.services.recurring_income_rule_service import (
    create_recurring_income_rule_service,
    generate_expected_incomes_for_month_service,
)


class FakeIncomingBankProvider:

    def get_transactions(self):
        return [
            BankTransactionImport(
                external_transaction_id="incoming_001",
                provider="fake_bank",
                amount=Decimal("2448.52"),
                direction=BankTransactionDirection.INCOMING,
                description="PAYROLL 07.2026",
                transaction_date=date(2026, 7, 30),
                value_date=date(2026, 7, 30),
                currency="EUR"
            ),
            BankTransactionImport(
                external_transaction_id="incoming_002",
                provider="fake_bank",
                amount=Decimal("393.81"),
                direction=BankTransactionDirection.INCOMING,
                description="ΣΥΝΤ.Ε.Φ.Κ.Α. - ΣΥΝΤ",
                transaction_date=date(2026, 7, 24),
                value_date=date(2026, 7, 24),
                currency="EUR"
            ),
            BankTransactionImport(
                external_transaction_id="incoming_003",
                provider="fake_bank",
                amount=Decimal("200.00"),
                direction=BankTransactionDirection.INCOMING,
                description="BONUS JULY",
                transaction_date=date(2026, 7, 25),
                value_date=date(2026, 7, 25),
                currency="EUR"
            ),
        ]


def test_incoming_bank_transactions_update_expected_and_create_extra_income(
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

    payroll_rule = RecurringIncomeRuleCreate(
        name="Payroll",
        expected_amount=Decimal("2448.52"),
        expected_day=30,
        transaction_keyword="PAYROLL"
    )

    efka_rule = RecurringIncomeRuleCreate(
        name="EFKA Pension",
        expected_amount=Decimal("393.81"),
        expected_day=24,
        transaction_keyword="ΣΥΝΤ.Ε.Φ.Κ.Α."
    )

    create_recurring_income_rule_service(
        payroll_rule,
        current_user,
        db_session
    )

    create_recurring_income_rule_service(
        efka_rule,
        current_user,
        db_session
    )

    generated = generate_expected_incomes_for_month_service(
        year=2026,
        month=7,
        current_user=current_user,
        db=db_session
    )

    assert len(generated) == 2

    provider = FakeIncomingBankProvider()

    sync_result = sync_bank_transactions_service(
        db=db_session,
        current_user=current_user,
        provider=provider
    )

    assert sync_result.received == 3
    assert sync_result.created == 3
    assert sync_result.skipped == 0

    processing_result = (
        process_incoming_bank_transactions_service(
            db=db_session,
            current_user=current_user
        )
    )

    assert processing_result.found == 3
    assert processing_result.processed == 3

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

    payroll_income = incomes_by_source["Payroll"]

    assert payroll_income.amount == Decimal("2448.52")
    assert payroll_income.status == IncomeStatus.RECEIVED
    assert payroll_income.received_date == date(2026, 7, 30)
    assert payroll_income.bank_transaction_id is not None
    assert payroll_income.recurring_income_rule_id is not None

    efka_income = incomes_by_source["EFKA Pension"]

    assert efka_income.amount == Decimal("393.81")
    assert efka_income.status == IncomeStatus.RECEIVED
    assert efka_income.received_date == date(2026, 7, 24)
    assert efka_income.bank_transaction_id is not None
    assert efka_income.recurring_income_rule_id is not None

    bonus_income = incomes_by_source["BONUS JULY"]

    assert bonus_income.amount == Decimal("200.00")
    assert bonus_income.status == IncomeStatus.RECEIVED
    assert bonus_income.received_date == date(2026, 7, 25)
    assert bonus_income.recurring_income_rule_id is None
    assert bonus_income.bank_transaction_id is not None

    total_received = sum(
        (
            income.amount
            for income in incomes
            if income.status == IncomeStatus.RECEIVED
        ),
        Decimal("0.00")
    )

    assert total_received == Decimal("3042.33")

    bank_transactions = (
        db_session.query(BankTransactionModel)
        .filter(
            BankTransactionModel.user_id == current_user.id
        )
        .all()
    )

    assert len(bank_transactions) == 3

    assert all(
        transaction.processed_at is not None
        for transaction in bank_transactions
    )

    second_processing = (
        process_incoming_bank_transactions_service(
            db=db_session,
            current_user=current_user
        )
    )

    assert second_processing.found == 0
    assert second_processing.processed == 0

    incomes_after_second_processing = (
        db_session.query(IncomeModel)
        .filter(
            IncomeModel.user_id == current_user.id
        )
        .all()
    )

    assert len(incomes_after_second_processing) == 3