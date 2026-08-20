from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import Enum as SQLEnum, UniqueConstraint
from sqlalchemy import Column, Integer, Numeric, String, Date, ForeignKey, DateTime, CheckConstraint
from sqlalchemy.orm import relationship

from app.database.database import Base

class IncomeStatus(str, Enum):
    EXPECTED = "expected"
    RECEIVED = "received"

class IncomeModel(Base):
    __tablename__ = "incomes"
    __table_args__ = (
        CheckConstraint(
            "amount > 0",
            name="ck_incomes_amount_positive"
        ),
        UniqueConstraint(
            "recurring_income_rule_id",
            "expected_date",
            name="uq_income_recurring_rule_expected_date"
        )
    )
    id = Column(Integer, primary_key=True,index=True)
    amount = Column(Numeric(12, 2),nullable=False)
    source = Column(String(255),nullable=False)
    status = Column(SQLEnum(IncomeStatus), nullable=False,default=IncomeStatus.EXPECTED)
    expected_date = Column(Date,nullable=True)
    received_date = Column(Date,nullable=True)
    bank_transaction_id = Column(
        Integer,
        ForeignKey("bank_transactions.id"),
        nullable=True,
        unique=True
    )
    user_id = Column(Integer,ForeignKey('users.id'),nullable=False)
    recurring_income_rule_id = Column(
        Integer,
        ForeignKey(
            "recurring_income_rules.id",
            ondelete="SET NULL"
        ),
        nullable=True
    )
    created_at= Column(DateTime(timezone=True),nullable=False,default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True),nullable=False,default=lambda: datetime.now(timezone.utc),onupdate=lambda: datetime.now(timezone.utc))

    user = relationship(
        "UserModel",
        back_populates="incomes"
    )
    recurring_income_rule = relationship(
        "RecurringIncomeRuleModel",
        back_populates="incomes"
    )
    bank_transaction = relationship(
        "BankTransactionModel",
        back_populates="income"
    )