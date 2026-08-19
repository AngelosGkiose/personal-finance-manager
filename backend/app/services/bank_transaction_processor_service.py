from datetime import datetime, timezone

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.expense_model import ExpenseModel
from app.models.user_model import UserModel
from app.repositories.bank_transaction_repository import (
    get_unprocessed_outgoing_transactions,
)
from app.schemas.bank_transaction import (
    BankTransactionProcessingResult,
)
from app.services.categorization_service import (
    find_category_for_transaction_service,
)


def process_outgoing_bank_transactions_service(
    db: Session,
    current_user: UserModel
) -> BankTransactionProcessingResult:

    transactions = get_unprocessed_outgoing_transactions(
        db=db,
        user_id=current_user.id
    )

    processed = 0

    try:
        for transaction in transactions:
            category = find_category_for_transaction_service(
                description=transaction.description,
                current_user=current_user,
                db=db
            )

            expense = ExpenseModel(
                amount=transaction.amount,
                description=transaction.description,
                expense_date=transaction.transaction_date,
                category_id=category.id,
                user_id=current_user.id,
                bank_transaction_id=transaction.id
            )

            db.add(expense)
            db.flush()

            transaction.processed_at = datetime.now(
                timezone.utc
            )

            processed += 1

        db.commit()

    except SQLAlchemyError:
        db.rollback()
        raise

    return BankTransactionProcessingResult(
        found=len(transactions),
        processed=processed
    )