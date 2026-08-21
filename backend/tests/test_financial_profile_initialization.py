from decimal import Decimal

from app.models.category_model import CategoryModel
from app.models.categorization_rule_model import CategorizationRuleModel
from app.models.recurring_income_rule_model import RecurringIncomeRuleModel
from app.models.user_model import UserModel

from app.schemas.financial_profile import (
    CategorizationRuleSeed,
    FinancialProfileSeed,
    RecurringIncomeRuleSeed,
)
from app.services.categorization_service import normalize_transaction_text

from app.services.financial_profile_initialization_service import (
    initialize_financial_profile_service,
)


def test_financial_profile_initialization_is_idempotent_and_extendable(
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

    # -------------------------------------------------
    # Initial profile
    # -------------------------------------------------

    initial_profile = FinancialProfileSeed(
        categories=[
            "Subscriptions",
            "Restaurants",
        ],

        categorization_rules=[
            CategorizationRuleSeed(
                keyword="SHELL",
                category_name="Fuel"
            ),
            CategorizationRuleSeed(
                keyword="NETFLIX",
                category_name="Subscriptions"
            ),
        ],

        recurring_income_rules=[
            RecurringIncomeRuleSeed(
                name="Payroll",
                expected_amount=Decimal("2448.52"),
                expected_day=30,
                transaction_keyword="PAYROLL"
            ),
            RecurringIncomeRuleSeed(
                name="EFKA Pension",
                expected_amount=Decimal("393.81"),
                expected_day=24,
                transaction_keyword="ΣΥΝΤ.Ε.Φ.Κ.Α."
            ),
        ]
    )

    # -------------------------------------------------
    # First initialization
    # -------------------------------------------------

    first_result = initialize_financial_profile_service(
        profile=initial_profile,
        current_user=current_user,
        db=db_session
    )

    assert first_result.categories_created == 2
    assert first_result.categorization_rules_created == 2
    assert first_result.recurring_income_rules_created == 2

    # -------------------------------------------------
    # Verify created categories
    # -------------------------------------------------

    categories = (
        db_session.query(CategoryModel)
        .filter(
            CategoryModel.user_id == current_user.id
        )
        .all()
    )

    category_names = {
        category.name
        for category in categories
    }

    assert "Subscriptions" in category_names
    assert "Restaurants" in category_names

    # Existing default categories must still exist
    assert "Fuel" in category_names
    assert "Supermarket" in category_names
    assert "Other Expenses" in category_names

    # -------------------------------------------------
    # Verify categorization rules
    # -------------------------------------------------

    categorization_rules = (
        db_session.query(CategorizationRuleModel)
        .filter(
            CategorizationRuleModel.user_id == current_user.id
        )
        .all()
    )

    assert len(categorization_rules) == 2

    rules_by_keyword = {
        rule.keyword: rule
        for rule in categorization_rules
    }

    assert "SHELL" in rules_by_keyword
    assert "NETFLIX" in rules_by_keyword

    shell_rule = rules_by_keyword["SHELL"]
    netflix_rule = rules_by_keyword["NETFLIX"]

    assert shell_rule.category.name == "Fuel"
    assert netflix_rule.category.name == "Subscriptions"

    # -------------------------------------------------
    # Verify recurring income rules
    # -------------------------------------------------

    recurring_rules = (
        db_session.query(RecurringIncomeRuleModel)
        .filter(
            RecurringIncomeRuleModel.user_id == current_user.id
        )
        .all()
    )

    assert len(recurring_rules) == 2

    recurring_by_name = {
        rule.name: rule
        for rule in recurring_rules
    }

    payroll_rule = recurring_by_name["Payroll"]

    assert payroll_rule.expected_amount == Decimal("2448.52")
    assert payroll_rule.expected_day == 30
    assert payroll_rule.transaction_keyword == normalize_transaction_text(
        "PAYROLL"
    )
    assert payroll_rule.is_active is True

    efka_rule = recurring_by_name["EFKA Pension"]

    assert efka_rule.expected_amount == Decimal("393.81")
    assert efka_rule.expected_day == 24
    assert efka_rule.transaction_keyword == normalize_transaction_text(
        "ΣΥΝΤ.Ε.Φ.Κ.Α."
    )
    assert efka_rule.is_active is True

    # -------------------------------------------------
    # Second initialization with SAME profile
    # -------------------------------------------------

    second_result = initialize_financial_profile_service(
        profile=initial_profile,
        current_user=current_user,
        db=db_session
    )

    assert second_result.categories_created == 0
    assert second_result.categorization_rules_created == 0
    assert second_result.recurring_income_rules_created == 0

    # -------------------------------------------------
    # Extend profile later
    # -------------------------------------------------

    extended_profile = FinancialProfileSeed(
        categories=[
            "Subscriptions",
            "Restaurants",
            "Shopping",
        ],

        categorization_rules=[
            CategorizationRuleSeed(
                keyword="SHELL",
                category_name="Fuel"
            ),
            CategorizationRuleSeed(
                keyword="NETFLIX",
                category_name="Subscriptions"
            ),
            CategorizationRuleSeed(
                keyword="SPOTIFY",
                category_name="Subscriptions"
            ),
            CategorizationRuleSeed(
                keyword="ZARA",
                category_name="Shopping"
            ),
        ],

        recurring_income_rules=[
            RecurringIncomeRuleSeed(
                name="Payroll",
                expected_amount=Decimal("2448.52"),
                expected_day=30,
                transaction_keyword="PAYROLL"
            ),
            RecurringIncomeRuleSeed(
                name="EFKA Pension",
                expected_amount=Decimal("393.81"),
                expected_day=24,
                transaction_keyword="ΣΥΝΤ.Ε.Φ.Κ.Α."
            ),
        ]
    )

    third_result = initialize_financial_profile_service(
        profile=extended_profile,
        current_user=current_user,
        db=db_session
    )

    assert third_result.categories_created == 1
    assert third_result.categorization_rules_created == 2
    assert third_result.recurring_income_rules_created == 0

    # -------------------------------------------------
    # Final verification
    # -------------------------------------------------

    final_categories = (
        db_session.query(CategoryModel)
        .filter(
            CategoryModel.user_id == current_user.id
        )
        .all()
    )

    final_category_names = {
        category.name
        for category in final_categories
    }

    assert "Shopping" in final_category_names

    final_rules = (
        db_session.query(CategorizationRuleModel)
        .filter(
            CategorizationRuleModel.user_id == current_user.id
        )
        .all()
    )

    final_rules_by_keyword = {
        rule.keyword: rule
        for rule in final_rules
    }

    assert len(final_rules) == 4

    assert final_rules_by_keyword["SHELL"].category.name == "Fuel"
    assert (
        final_rules_by_keyword["NETFLIX"].category.name
        == "Subscriptions"
    )
    assert (
        final_rules_by_keyword["SPOTIFY"].category.name
        == "Subscriptions"
    )
    assert (
        final_rules_by_keyword["ZARA"].category.name
        == "Shopping"
    )

    final_recurring_rules = (
        db_session.query(RecurringIncomeRuleModel)
        .filter(
            RecurringIncomeRuleModel.user_id == current_user.id
        )
        .all()
    )

    assert len(final_recurring_rules) == 2