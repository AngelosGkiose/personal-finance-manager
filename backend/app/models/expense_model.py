from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship

from app.database.database import Base
from sqlalchemy import Numeric


class ExpenseModel(Base):
    __tablename__ = 'expenses'
    __table_args__ = (
        CheckConstraint(
            "amount > 0",
            name="ck_expenses_amount_positive"
        ),
    )
    id=Column(Integer,primary_key=True,index=True)
    amount=Column(Numeric(12, 2),nullable=False)
    description=Column(String(255),nullable=False)
    expense_date=Column(Date,nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc))
    bank_transaction_id = Column(
        Integer,
        ForeignKey("bank_transactions.id"),
        nullable=True,
        unique=True
    )
    user_id = Column(Integer,ForeignKey('users.id'),nullable=False)
    category_id = Column(Integer,ForeignKey('categories.id'),nullable=False)

    user=relationship("UserModel",back_populates="expenses")
    category=relationship("CategoryModel",back_populates="expenses")
    obligations = relationship("ObligationModel", back_populates="expense",uselist=False)
    bank_transaction = relationship(
        "BankTransactionModel",
        back_populates="expense"
    )


