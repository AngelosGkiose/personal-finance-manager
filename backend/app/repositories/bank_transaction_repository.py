from sqlalchemy.orm import Session

from app.models.bank_transaction_model import BankTransactionModel, BankTransactionDirection


def get_bank_transaction_by_external_id(
    db: Session,
    user_id: int,
    provider: str,
    external_transaction_id: str
):
    return (
        db.query(BankTransactionModel)
        .filter(
            BankTransactionModel.user_id == user_id,
            BankTransactionModel.provider == provider,
            BankTransactionModel.external_transaction_id == external_transaction_id
        )
        .first()
    )


def add_bank_transaction(
    db: Session,
    bank_transaction: BankTransactionModel
):
    db.add(bank_transaction)
    db.flush()

    return bank_transaction

def get_unprocessed_outgoing_transactions(
    db: Session,
    user_id: int
):
    return (
        db.query(BankTransactionModel)
        .filter(
            BankTransactionModel.user_id == user_id,
            BankTransactionModel.direction == BankTransactionDirection.OUTGOING,
            BankTransactionModel.processed_at.is_(None)
        )
        .order_by(
            BankTransactionModel.transaction_date.asc(),
            BankTransactionModel.id.asc()
        )
        .all()
    )