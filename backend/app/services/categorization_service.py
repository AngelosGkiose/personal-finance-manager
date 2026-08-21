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
import re
import unicodedata
MIXED_SCRIPT_CONFUSABLES = str.maketrans({
    "Α": "A",
    "Β": "B",
    "Ε": "E",
    "Ζ": "Z",
    "Η": "H",
    "Ι": "I",
    "Κ": "K",
    "Μ": "M",
    "Ν": "N",
    "Ο": "O",
    "Ρ": "P",
    "Τ": "T",
    "Υ": "Y",
    "Χ": "X",
})


GREEK_TO_LATIN = str.maketrans({
    "Α": "A",
    "Β": "B",
    "Γ": "G",
    "Δ": "D",
    "Ε": "E",
    "Ζ": "Z",
    "Η": "H",
    "Θ": "TH",
    "Ι": "I",
    "Κ": "K",
    "Λ": "L",
    "Μ": "M",
    "Ν": "N",
    "Ξ": "X",
    "Ο": "O",
    "Π": "P",
    "Ρ": "R",
    "Σ": "S",
    "Τ": "T",
    "Υ": "Y",
    "Φ": "F",
    "Χ": "X",
    "Ψ": "PS",
    "Ω": "O",
})
def normalize_alpha_segment(segment: str) -> str:
    has_latin = any(
        "A" <= char <= "Z"
        for char in segment
    )

    has_greek = any(
        "\u0370" <= char <= "\u03ff"
        for char in segment
    )

    if has_latin and has_greek:
        return segment.translate(
            MIXED_SCRIPT_CONFUSABLES
        )

    if has_greek:
        return segment.translate(
            GREEK_TO_LATIN
        )

    return segment
def normalize_transaction_text(value: str) -> str:
    value = value.strip().upper()

    value = unicodedata.normalize(
        "NFD",
        value
    )

    value = "".join(
        char
        for char in value
        if not unicodedata.combining(char)
    )

    value = re.sub(
        r"[A-ZΑ-Ω]+",
        lambda match: normalize_alpha_segment(
            match.group()
        ),
        value
    )

    return " ".join(
        value.split()
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