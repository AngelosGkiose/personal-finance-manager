from sqlalchemy.orm import Session

from app.models.recurring_income_rule_model import RecurringIncomeRuleModel


def get_recurring_income_rule_by_id(
    db: Session,
    recurring_income_rule_id: int,
    current_user_id: int
):
    return (
        db.query(RecurringIncomeRuleModel)
        .filter(
            RecurringIncomeRuleModel.id == recurring_income_rule_id,
            RecurringIncomeRuleModel.user_id == current_user_id
        )
        .first()
    )


def get_recurring_income_rule_by_name(
    db: Session,
    current_user_id: int,
    name: str
):
    return (
        db.query(RecurringIncomeRuleModel)
        .filter(
            RecurringIncomeRuleModel.user_id == current_user_id,
            RecurringIncomeRuleModel.name == name
        )
        .first()
    )


def get_recurring_income_rules_by_user(
    db: Session,
    current_user_id: int
):
    return (
        db.query(RecurringIncomeRuleModel)
        .filter(
            RecurringIncomeRuleModel.user_id == current_user_id
        )
        .order_by(
            RecurringIncomeRuleModel.id.asc()
        )
        .all()
    )


def add_recurring_income_rule(
    db: Session,
    recurring_income_rule: RecurringIncomeRuleModel
):
    db.add(recurring_income_rule)
    db.flush()

    return recurring_income_rule


def delete_recurring_income_rule(
    db: Session,
    recurring_income_rule: RecurringIncomeRuleModel
):
    db.delete(recurring_income_rule)
    db.flush()


def get_active_recurring_income_rules(
    db: Session,
    current_user_id: int
):
    return (
        db.query(RecurringIncomeRuleModel)
        .filter(
            RecurringIncomeRuleModel.user_id == current_user_id,
            RecurringIncomeRuleModel.is_active.is_(True)
        )
        .order_by(
            RecurringIncomeRuleModel.id.asc()
        )
        .all()
    )