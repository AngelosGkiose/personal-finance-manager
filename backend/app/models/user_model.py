from datetime import datetime,timezone

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from app.database.database import Base


class UserModel(Base):
    __tablename__ = 'users'
    id =Column(Integer, primary_key=True,index=True)
    username =Column(String,nullable=False)
    email=Column(String,unique=True,nullable=False)
    hashed_password =Column(String,nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )
    categories=relationship("CategoryModel",back_populates="user")
    expenses = relationship("ExpenseModel",back_populates="user")
    
    incomes = relationship(
        "IncomeModel",
        back_populates="user"
    )
    obligations = relationship("ObligationModel", back_populates="user")


















