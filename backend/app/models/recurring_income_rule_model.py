from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.orm import relationship

from app.database.database import Base


class RecurringIncomeRuleModel(Base):
    __tablename__ = "recurring_income_rules"

    __table_args__ = (
        CheckConstraint(
            "expected_amount > 0",
            name="check_recurring_income_expected_amount_positive"
        ),
        CheckConstraint(
            "expected_day >= 1 AND expected_day <= 31",
            name="check_recurring_income_expected_day"
        ),
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(100),
        nullable=False
    )

    expected_amount = Column(
        Numeric(12, 2),
        nullable=False
    )

    expected_day = Column(
        Integer,
        nullable=False
    )

    transaction_keyword = Column(
        String(100),
        nullable=True
    )

    is_active = Column(
        Boolean,
        nullable=False,
        default=True
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
        back_populates="recurring_income_rules"
    )

    incomes = relationship(
        "IncomeModel",
        back_populates="recurring_income_rule",
        passive_deletes=True
    )