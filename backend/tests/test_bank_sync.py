from app.integrations.banking.fake_bank_provider import FakeBankProvider
from app.models.bank_transaction_model import BankTransactionModel
from app.models.user_model import UserModel
from app.services.bank_sync_service import sync_bank_transactions_service


def test_bank_sync_imports_transactions_and_skips_duplicates(
    db_session,
    test_user,
    test_user_data
):
    current_user = (
        db_session.query(UserModel)
        .filter(UserModel.email == test_user_data["email"])
        .first()
    )

    assert current_user is not None

    provider = FakeBankProvider()

    # First sync
    first_result = sync_bank_transactions_service(
        db=db_session,
        current_user=current_user,
        provider=provider
    )

    assert first_result.received == 3
    assert first_result.created == 3
    assert first_result.skipped == 0

    transactions = (
        db_session.query(BankTransactionModel)
        .filter(BankTransactionModel.user_id == current_user.id)
        .all()
    )

    assert len(transactions) == 3

    external_ids = {
        transaction.external_transaction_id
        for transaction in transactions
    }

    assert external_ids == {
        "tx_001",
        "tx_002",
        "tx_003"
    }

    assert all(
        transaction.processed_at is None
        for transaction in transactions
    )

    # Second sync
    second_result = sync_bank_transactions_service(
        db=db_session,
        current_user=current_user,
        provider=provider
    )

    assert second_result.received == 3
    assert second_result.created == 0
    assert second_result.skipped == 3

    transactions_after_second_sync = (
        db_session.query(BankTransactionModel)
        .filter(BankTransactionModel.user_id == current_user.id)
        .all()
    )

    assert len(transactions_after_second_sync) == 3