from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette import status

from app.models.categorization_rule_model import CategorizationRuleModel
from app.models.user_model import UserModel
from app.repositories import (
    category_repository,
    categorization_rule_repository,
)


def normalize_transaction_text(value: str) -> str:
    return " ".join(
        value.strip().upper().split()
    )


def create_categorization_rule_service(
    keyword: str,
    category_id: int,
    current_user: UserModel,
    db: Session
):
    normalized_keyword = normalize_transaction_text(keyword)

    category = category_repository.get_category_by_id(
        db,
        category_id,
        current_user.id
    )

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    existing_rule = (
        categorization_rule_repository
        .get_categorization_rule_by_keyword(
            db=db,
            user_id=current_user.id,
            keyword=normalized_keyword
        )
    )

    if existing_rule:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Categorization rule already exists"
        )

    new_rule = CategorizationRuleModel(
        keyword=normalized_keyword,
        category_id=category.id,
        user_id=current_user.id
    )

    try:
        categorization_rule_repository.add_categorization_rule(
            db=db,
            rule=new_rule
        )

        db.commit()
        db.refresh(new_rule)

        return new_rule

    except SQLAlchemyError:
        db.rollback()
        raise


def find_category_for_transaction_service(
    description: str,
    current_user: UserModel,
    db: Session
):
    normalized_description = normalize_transaction_text(
        description
    )

    rules = (
        categorization_rule_repository
        .get_categorization_rules_by_user(
            db=db,
            user_id=current_user.id
        )
    )

    for rule in rules:
        if rule.keyword in normalized_description:
            return rule.category

    other_expenses = category_repository.get_category_by_name(
        db=db,
        current_user_id=current_user.id,
        category_name="Other Expenses"
    )

    if other_expenses is None:
        raise RuntimeError(
            "Other Expenses system category not found"
        )

    return other_expenses