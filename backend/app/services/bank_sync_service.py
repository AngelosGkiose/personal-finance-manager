from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.bank_transaction_model import BankTransactionModel
from app.models.user_model import UserModel
from app.repositories.bank_transaction_repository import (
    get_bank_transaction_by_external_id,
    add_bank_transaction,
)
from app.schemas.bank_transaction import BankSyncResult


def sync_bank_transactions_service(
    db: Session,
    current_user: UserModel,
    provider
) -> BankSyncResult:

    transactions = provider.get_transactions()

    created = 0
    skipped = 0

    try:
        for transaction in transactions:

            existing_transaction = get_bank_transaction_by_external_id(
                db=db,
                user_id=current_user.id,
                provider=transaction.provider,
                external_transaction_id=transaction.external_transaction_id
            )

            if existing_transaction:
                skipped += 1
                continue

            bank_transaction = BankTransactionModel(
                external_transaction_id=transaction.external_transaction_id,
                provider=transaction.provider,
                amount=transaction.amount,
                direction=transaction.direction,
                description=transaction.description,
                transaction_date=transaction.transaction_date,
                value_date=transaction.value_date,
                currency=transaction.currency,
                user_id=current_user.id
            )

            add_bank_transaction(
                db=db,
                bank_transaction=bank_transaction
            )

            created += 1

        db.commit()

    except SQLAlchemyError:
        db.rollback()
        raise

    return BankSyncResult(
        received=len(transactions),
        created=created,
        skipped=skipped
    )