from datetime import datetime, timezone

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.expense_model import ExpenseModel
from app.models.income_model import IncomeModel, IncomeStatus
from app.models.user_model import UserModel
from app.repositories.bank_transaction_repository import (
    get_unprocessed_outgoing_transactions, get_unprocessed_incoming_transactions,
)
from app.repositories.income_repository import get_expected_income_by_recurring_rule_for_month
from app.repositories.recurring_income_rule_repository import get_active_recurring_income_rules
from app.schemas.bank_transaction import (
    BankTransactionProcessingResult,
)
from app.services.categorization_service import (
    find_category_for_transaction_service, normalize_transaction_text,
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

def process_incoming_bank_transactions_service(
    db: Session,
    current_user: UserModel
) -> BankTransactionProcessingResult:

    transactions = get_unprocessed_incoming_transactions(
        db,
        current_user.id
    )

    recurring_rules = get_active_recurring_income_rules(
        db,
        current_user.id
    )

    processed = 0

    try:
        for transaction in transactions:

            normalized_description = normalize_transaction_text(
                transaction.description
            )

            matching_rule = None

            for rule in recurring_rules:
                if not rule.transaction_keyword:
                    continue

                normalized_keyword = normalize_transaction_text(
                    rule.transaction_keyword
                )

                if normalized_keyword in normalized_description:
                    matching_rule = rule
                    break

            expected_income = None

            if matching_rule:
                expected_income = (
                    get_expected_income_by_recurring_rule_for_month(
                        db,
                        current_user.id,
                        matching_rule.id,
                        transaction.transaction_date.year,
                        transaction.transaction_date.month
                    )
                )

            if expected_income:
                expected_income.amount = transaction.amount
                expected_income.status = IncomeStatus.RECEIVED
                expected_income.received_date = (
                    transaction.transaction_date
                )
                expected_income.bank_transaction_id = transaction.id

            else:
                income = IncomeModel(
                    amount=transaction.amount,
                    source=(
                        matching_rule.name
                        if matching_rule
                        else transaction.description
                    ),
                    status=IncomeStatus.RECEIVED,
                    expected_date=None,
                    received_date=transaction.transaction_date,
                    user_id=current_user.id,
                    recurring_income_rule_id=(
                        matching_rule.id
                        if matching_rule
                        else None
                    ),
                    bank_transaction_id=transaction.id
                )

                db.add(income)
                db.flush()

            transaction.processed_at = datetime.now(timezone.utc)

            processed += 1

        db.commit()

    except SQLAlchemyError:
        db.rollback()
        raise

    return BankTransactionProcessingResult(
        found=len(transactions),
        processed=processed
    )