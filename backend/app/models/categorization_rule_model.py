from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.database.database import Base


class CategorizationRuleModel(Base):
    __tablename__ = "categorization_rules"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "keyword",
            name="uq_categorization_rule_user_keyword"
        ),
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    keyword = Column(
        String(100),
        nullable=False
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    category_id = Column(
        Integer,
        ForeignKey(
            "categories.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    user = relationship(
        "UserModel",
        back_populates="categorization_rules"
    )

    category = relationship(
        "CategoryModel",
        back_populates="categorization_rules"
    )