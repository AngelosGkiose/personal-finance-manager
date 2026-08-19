from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import Enum as SQLEnum, String, Date, DateTime, UniqueConstraint, CheckConstraint, ForeignKey
from sqlalchemy import Column, Integer, Numeric
from sqlalchemy.orm import relationship

from app.database.database import Base


class BankTransactionDirection(str, Enum):
    INCOMING="incoming"
    OUTGOING="outgoing"

class BankTransactionModel(Base):
    __tablename__ = "bank_transactions"

    __table_args__ = (
        CheckConstraint(
            "amount > 0",
            name="check_bank_transaction_amount_positive"
        ),
        UniqueConstraint(
            "user_id",
            "provider",
            "external_transaction_id",
            name="uq_bank_transaction_user_provider_external_id"
        )
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    external_transaction_id = Column(
        String(255),
        nullable=False
    )

    amount = Column(
        Numeric(12, 2),
        nullable=False
    )

    direction = Column(
        SQLEnum(BankTransactionDirection),
        nullable=False
    )

    description = Column(
        String(255),
        nullable=False
    )

    transaction_date = Column(
        Date,
        nullable=False
    )

    currency = Column(
        String(3),
        nullable=False,
        default="EUR"
    )

    provider = Column(
        String(50),
        nullable=False
    )

    processed_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    user = relationship(
        "UserModel",
        back_populates="bank_transactions")

    expense = relationship(
        "ExpenseModel",
        back_populates="bank_transaction",
        uselist=False
    )