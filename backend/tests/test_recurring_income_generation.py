from decimal import Decimal

from app.models.income_model import IncomeModel, IncomeStatus
from app.models.user_model import UserModel
from app.schemas.recurring_income_rule import RecurringIncomeRuleCreate
from app.services.recurring_income_rule_service import (
    create_recurring_income_rule_service,
    generate_expected_incomes_for_month_service,
)


def test_recurring_income_rules_generate_expected_incomes_without_duplicates(
    db_session,
    test_user,
    test_user_data
):
    current_user = (
        db_session.query(UserModel)
        .filter(
            UserModel.email == test_user_data["email"]
        )
        .first()
    )

    assert current_user is not None

    salary_rule = RecurringIncomeRuleCreate(
        name="Salary",
        expected_amount=Decimal("1300.00"),
        expected_day=28
    )

    second_income_rule = RecurringIncomeRuleCreate(
        name="Second Income",
        expected_amount=Decimal("500.00"),
        expected_day=31
    )

    create_recurring_income_rule_service(
        salary_rule,
        current_user,
        db_session
    )

    create_recurring_income_rule_service(
        second_income_rule,
        current_user,
        db_session
    )

    created_incomes = (
        generate_expected_incomes_for_month_service(
            year=2027,
            month=2,
            current_user=current_user,
            db=db_session
        )
    )

    assert len(created_incomes) == 2

    incomes = (
        db_session.query(IncomeModel)
        .filter(
            IncomeModel.user_id == current_user.id
        )
        .order_by(IncomeModel.amount.desc())
        .all()
    )

    assert len(incomes) == 2

    salary_income = incomes[0]
    second_income = incomes[1]

    assert salary_income.source == "Salary"
    assert salary_income.amount == Decimal("1300.00")
    assert salary_income.status == IncomeStatus.EXPECTED
    assert salary_income.expected_date.year == 2027
    assert salary_income.expected_date.month == 2
    assert salary_income.expected_date.day == 28
    assert salary_income.received_date is None
    assert salary_income.recurring_income_rule_id is not None

    assert second_income.source == "Second Income"
    assert second_income.amount == Decimal("500.00")
    assert second_income.status == IncomeStatus.EXPECTED


    assert second_income.expected_date.day == 28

    second_generation = (
        generate_expected_incomes_for_month_service(
            year=2027,
            month=2,
            current_user=current_user,
            db=db_session
        )
    )

    assert len(second_generation) == 0

    incomes_after_second_generation = (
        db_session.query(IncomeModel)
        .filter(
            IncomeModel.user_id == current_user.id
        )
        .all()
    )

    assert len(incomes_after_second_generation) == 2