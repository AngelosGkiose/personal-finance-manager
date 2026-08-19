from decimal import Decimal

from app.integrations.banking.fake_bank_provider import FakeBankProvider
from app.models.bank_transaction_model import (
    BankTransactionModel,
    BankTransactionDirection,
)
from app.models.expense_model import ExpenseModel
from app.models.user_model import UserModel
from app.repositories.category_repository import get_category_by_name
from app.services.bank_sync_service import sync_bank_transactions_service
from app.services.bank_transaction_processor_service import (
    process_outgoing_bank_transactions_service,
)
from app.services.categorization_service import (
    create_categorization_rule_service,
)


def test_outgoing_bank_transactions_create_categorized_expenses(
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
        db=db_session,
        current_user_id=current_user.id,
        category_name="Fuel"
    )

    supermarket_category = get_category_by_name(
        db=db_session,
        current_user_id=current_user.id,
        category_name="Supermarket"
    )

    assert fuel_category is not None
    assert supermarket_category is not None

    # -------------------------------------------------
    # Create categorization rules
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
    # Import transactions from fake bank
    # -------------------------------------------------

    provider = FakeBankProvider()

    sync_result = sync_bank_transactions_service(
        db=db_session,
        current_user=current_user,
        provider=provider
    )

    assert sync_result.received == 3
    assert sync_result.created == 3
    assert sync_result.skipped == 0

    # -------------------------------------------------
    # Process OUTGOING transactions
    # -------------------------------------------------

    processing_result = process_outgoing_bank_transactions_service(
        db=db_session,
        current_user=current_user
    )

    assert processing_result.found == 2
    assert processing_result.processed == 2

    # -------------------------------------------------
    # Verify created expenses
    # -------------------------------------------------

    expenses = (
        db_session.query(ExpenseModel)
        .filter(
            ExpenseModel.user_id == current_user.id
        )
        .order_by(ExpenseModel.amount.asc())
        .all()
    )

    assert len(expenses) == 2

    expenses_by_description = {
        expense.description: expense
        for expense in expenses
    }

    shell_expense = expenses_by_description["SHELL KIFISIAS"]

    assert shell_expense.amount == Decimal("65.00")
    assert shell_expense.category_id == fuel_category.id
    assert shell_expense.bank_transaction_id is not None

    sklavenitis_expense = expenses_by_description["SKLAVENITIS"]

    assert sklavenitis_expense.amount == Decimal("84.50")
    assert sklavenitis_expense.category_id == supermarket_category.id
    assert sklavenitis_expense.bank_transaction_id is not None

    # -------------------------------------------------
    # Verify OUTGOING transactions are processed
    # -------------------------------------------------

    outgoing_transactions = (
        db_session.query(BankTransactionModel)
        .filter(
            BankTransactionModel.user_id == current_user.id,
            BankTransactionModel.direction
            == BankTransactionDirection.OUTGOING
        )
        .all()
    )

    assert len(outgoing_transactions) == 2

    assert all(
        transaction.processed_at is not None
        for transaction in outgoing_transactions
    )

    # -------------------------------------------------
    # Verify INCOMING transaction was NOT processed
    # -------------------------------------------------

    incoming_transaction = (
        db_session.query(BankTransactionModel)
        .filter(
            BankTransactionModel.user_id == current_user.id,
            BankTransactionModel.direction
            == BankTransactionDirection.INCOMING
        )
        .first()
    )

    assert incoming_transaction is not None
    assert incoming_transaction.description == "SALARY AUGUST"
    assert incoming_transaction.processed_at is None

    # -------------------------------------------------
    # Process again - must create no duplicates
    # -------------------------------------------------

    second_processing_result = (
        process_outgoing_bank_transactions_service(
            db=db_session,
            current_user=current_user
        )
    )

    assert second_processing_result.found == 0
    assert second_processing_result.processed == 0

    expenses_after_second_processing = (
        db_session.query(ExpenseModel)
        .filter(
            ExpenseModel.user_id == current_user.id
        )
        .all()
    )

    assert len(expenses_after_second_processing) == 2