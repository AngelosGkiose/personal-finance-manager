import calendar
from datetime import date

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.income_model import IncomeModel, IncomeStatus
from app.models.recurring_income_rule_model import RecurringIncomeRuleModel
from app.models.user_model import UserModel
from app.repositories.income_repository import get_income_by_recurring_rule_and_expected_date
from app.repositories.recurring_income_rule_repository import (
    add_recurring_income_rule,
    delete_recurring_income_rule,
    get_recurring_income_rule_by_id,
    get_recurring_income_rule_by_name,
    get_recurring_income_rules_by_user, get_active_recurring_income_rules,
)

from app.schemas.recurring_income_rule import (
    RecurringIncomeRuleCreate,
    RecurringIncomeRuleUpdate,
)


def create_recurring_income_rule_service(
    recurring_income_rule_data: RecurringIncomeRuleCreate,
    current_user: UserModel,
    db: Session
):
    normalized_name = recurring_income_rule_data.name.strip()

    existing_rule = get_recurring_income_rule_by_name(
        db,
        current_user.id,
        normalized_name
    )

    if existing_rule:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Recurring income rule already exists"
        )

    transaction_keyword = (
        recurring_income_rule_data.transaction_keyword.strip().upper()
        if recurring_income_rule_data.transaction_keyword
        else None
    )

    recurring_income_rule = RecurringIncomeRuleModel(
        name=normalized_name,
        expected_amount=recurring_income_rule_data.expected_amount,
        expected_day=recurring_income_rule_data.expected_day,
        transaction_keyword=transaction_keyword,
        user_id=current_user.id
    )

    try:
        add_recurring_income_rule(
            db,
            recurring_income_rule
        )

        db.commit()
        db.refresh(recurring_income_rule)

    except SQLAlchemyError:
        db.rollback()
        raise

    return recurring_income_rule


def get_recurring_income_rules_service(
    current_user: UserModel,
    db: Session
):
    return get_recurring_income_rules_by_user(
        db,
        current_user.id
    )


def get_recurring_income_rule_service(
    recurring_income_rule_id: int,
    current_user: UserModel,
    db: Session
):
    recurring_income_rule = get_recurring_income_rule_by_id(
        db,
        recurring_income_rule_id,
        current_user.id
    )

    if not recurring_income_rule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recurring income rule not found"
        )

    return recurring_income_rule
def update_recurring_income_rule_service(
    recurring_income_rule_id: int,
    recurring_income_rule_data: RecurringIncomeRuleUpdate,
    current_user: UserModel,
    db: Session
):
    recurring_income_rule = get_recurring_income_rule_by_id(
        db,
        recurring_income_rule_id,
        current_user.id
    )

    if not recurring_income_rule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recurring income rule not found"
        )

    update_data = recurring_income_rule_data.model_dump(
        exclude_unset=True
    )

    if "name" in update_data:
        normalized_name = update_data["name"].strip()

        existing_rule = get_recurring_income_rule_by_name(
            db,
            current_user.id,
            normalized_name
        )

        if (
            existing_rule
            and existing_rule.id != recurring_income_rule.id
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Recurring income rule already exists"
            )

        update_data["name"] = normalized_name

    if (
        "transaction_keyword" in update_data
        and update_data["transaction_keyword"] is not None
    ):
        update_data["transaction_keyword"] = (
            update_data["transaction_keyword"]
            .strip()
            .upper()
        )

    for field, value in update_data.items():
        setattr(
            recurring_income_rule,
            field,
            value
        )

    try:
        db.commit()
        db.refresh(recurring_income_rule)

    except SQLAlchemyError:
        db.rollback()
        raise

    return recurring_income_rule
def delete_recurring_income_rule_service(
    recurring_income_rule_id: int,
    current_user: UserModel,
    db: Session
):
    recurring_income_rule = get_recurring_income_rule_by_id(
        db,
        recurring_income_rule_id,
        current_user.id
    )

    if not recurring_income_rule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recurring income rule not found"
        )

    try:
        delete_recurring_income_rule(
            db,
            recurring_income_rule
        )

        db.commit()

    except SQLAlchemyError:
        db.rollback()
        raise
def generate_expected_incomes_for_month_service(
    year: int,
    month: int,
    current_user: UserModel,
    db: Session
):
    active_rules = get_active_recurring_income_rules(
        db,
        current_user.id
    )

    created_incomes = []

    try:
        for rule in active_rules:

            last_day_of_month = calendar.monthrange(
                year,
                month
            )[1]

            expected_day = min(
                rule.expected_day,
                last_day_of_month
            )

            expected_date = date(
                year,
                month,
                expected_day
            )

            existing_income = (
                get_income_by_recurring_rule_and_expected_date(
                    db,
                    current_user.id,
                    rule.id,
                    expected_date
                )
            )

            if existing_income:
                continue

            income = IncomeModel(
                amount=rule.expected_amount,
                source=rule.name,
                status=IncomeStatus.EXPECTED,
                expected_date=expected_date,
                received_date=None,
                user_id=current_user.id,
                recurring_income_rule_id=rule.id
            )

            db.add(income)
            db.flush()

            created_incomes.append(income)

        db.commit()

        for income in created_incomes:
            db.refresh(income)

    except SQLAlchemyError:
        db.rollback()
        raise

    return created_incomes