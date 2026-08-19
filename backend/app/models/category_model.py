from datetime import timezone, datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint, Boolean
from sqlalchemy.orm import relationship

from app.database.database import Base


class CategoryModel(Base):
    __tablename__ = 'categories'
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "name",
            name="uq_categories_user_id_name",
        ),
    )
    id = Column(Integer, primary_key=True,index=True)
    name = Column(String,nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )
    is_system = Column(
        Boolean,
        nullable=False,
        default=False
    )
    user_id = Column(Integer,ForeignKey('users.id'),nullable=False)

    user=relationship("UserModel",back_populates="categories")
    expenses = relationship("ExpenseModel",back_populates="category")
    obligations = relationship("ObligationModel", back_populates="category")

    categorization_rules = relationship(
        "CategorizationRuleModel",
        back_populates="category"
    )