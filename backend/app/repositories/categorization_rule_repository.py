from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.categorization_rule_model import CategorizationRuleModel


def get_categorization_rule_by_keyword(
    db: Session,
    user_id: int,
    keyword: str
):
    return (
        db.query(CategorizationRuleModel)
        .filter(
            CategorizationRuleModel.user_id == user_id,
            CategorizationRuleModel.keyword == keyword
        )
        .first()
    )


def get_categorization_rules_by_user(
    db: Session,
    user_id: int
):
    return (
        db.query(CategorizationRuleModel)
        .filter(
            CategorizationRuleModel.user_id == user_id
        )
        .order_by(
            func.length(CategorizationRuleModel.keyword).desc()
        )
        .all()
    )


def add_categorization_rule(
    db: Session,
    rule: CategorizationRuleModel
):
    db.add(rule)
    db.flush()

    return rule

