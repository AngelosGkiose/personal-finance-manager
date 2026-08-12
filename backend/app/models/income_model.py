from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import Enum as SQLEnum
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
    )
    id = Column(Integer, primary_key=True,index=True)
    amount = Column(Numeric(12, 2),nullable=False)
    source = Column(String(255),nullable=False)
    status = Column(SQLEnum(IncomeStatus), nullable=False,default=IncomeStatus.EXPECTED)
    expected_date = Column(Date,nullable=False)
    received_date = Column(Date,nullable=True)
    user_id = Column(Integer,ForeignKey('users.id'),nullable=False)
    created_at= Column(DateTime(timezone=True),nullable=False,default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True),nullable=False,default=lambda: datetime.now(timezone.utc),onupdate=lambda: datetime.now(timezone.utc))

    user = relationship(
        "UserModel",
        back_populates="incomes"
    )