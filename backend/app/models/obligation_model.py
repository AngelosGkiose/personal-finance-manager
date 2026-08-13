from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import Enum as SQLEnum, CheckConstraint
from sqlalchemy import Column, Integer, Numeric, String, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.database.database import Base

class ObligationStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"

class ObligationModel(Base):
    __tablename__ = 'obligations'
    __table_args__ = (
        CheckConstraint(
            "amount > 0",
            name="ck_obligations_amount_positive"
        ),
    )
    id = Column(Integer, primary_key=True,index=True)
    title= Column(String(255),nullable=False)
    amount = Column(Numeric(12, 2),nullable=False)
    due_date = Column(Date,nullable=False)
    status = Column(SQLEnum(ObligationStatus),nullable=False)
    paid_date= Column(Date,nullable=True,default=None)
    category_id = Column(Integer,ForeignKey('categories.id'),nullable=False)
    user_id = Column(Integer,ForeignKey('users.id'),nullable=False)
    expense_id = Column(Integer,ForeignKey('expenses.id'),nullable=True,unique=True)
    created_at= Column(DateTime(timezone=True),nullable=False,default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True),nullable=False,default=lambda: datetime.now(timezone.utc),onupdate=lambda: datetime.now(timezone.utc))

    user=relationship("UserModel",back_populates="obligations")
    expense = relationship("ExpenseModel",back_populates="obligations")
    category = relationship("CategoryModel",back_populates="obligations")


