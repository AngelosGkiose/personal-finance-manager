from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.category_model import CategoryModel
from app.models.categorization_rule_model import (
    CategorizationRuleModel,
)
from app.models.recurring_income_rule_model import (
    RecurringIncomeRuleModel,
)
from app.models.user_model import UserModel

from app.repositories.category_repository import (
    get_category_by_name,
)
from app.repositories.categorization_rule_repository import (
    get_categorization_rule_by_keyword,
)
from app.repositories.recurring_income_rule_repository import (
    get_recurring_income_rule_by_name,
)

from app.schemas.financial_profile import (
    FinancialProfileInitializationResult,
    FinancialProfileSeed,
)

from app.services.categorization_service import (
    normalize_transaction_text,
)


def initialize_financial_profile_service(
    profile: FinancialProfileSeed,
    current_user: UserModel,
    db: Session
) -> FinancialProfileInitializationResult:

    categories_created = 0
    categorization_rules_created = 0
    recurring_income_rules_created = 0

    try:

        # ---------------------------------------------
        # Categories
        # ---------------------------------------------

        for category_name in profile.categories:

            normalized_name = category_name.strip()

            existing_category = get_category_by_name(
                category_name=normalized_name,
                current_user_id=current_user.id,
                db=db
            )

            if existing_category:
                continue

            category = CategoryModel(
                name=normalized_name,
                is_system=False,
                user_id=current_user.id
            )

            db.add(category)
            db.flush()

            categories_created += 1

        # ---------------------------------------------
        # Categorization Rules
        # ---------------------------------------------

        for rule_data in profile.categorization_rules:

            normalized_keyword = normalize_transaction_text(
                rule_data.keyword
            )

            existing_rule = get_categorization_rule_by_keyword(
                db,
                current_user.id,
                normalized_keyword
            )

            if existing_rule:
                continue

            category = get_category_by_name(
                category_name=rule_data.category_name.strip(),
                current_user_id=current_user.id,
                db=db
            )

            if not category:
                raise ValueError(
                    f"Category '{rule_data.category_name}' "
                    f"does not exist"
                )

            rule = CategorizationRuleModel(
                keyword=normalized_keyword,
                user_id=current_user.id,
                category_id=category.id
            )

            db.add(rule)
            db.flush()

            categorization_rules_created += 1

        # ---------------------------------------------
        # Recurring Income Rules
        # ---------------------------------------------

        for rule_data in profile.recurring_income_rules:

            normalized_name = rule_data.name.strip()

            existing_rule = get_recurring_income_rule_by_name(
                db,
                current_user.id,
                normalized_name
            )

            if existing_rule:
                continue

            transaction_keyword = (
                normalize_transaction_text(
                    rule_data.transaction_keyword
                )
                if rule_data.transaction_keyword
                else None
            )

            recurring_rule = RecurringIncomeRuleModel(
                name=normalized_name,
                expected_amount=rule_data.expected_amount,
                expected_day=rule_data.expected_day,
                transaction_keyword=transaction_keyword,
                is_active=True,
                user_id=current_user.id
            )

            db.add(recurring_rule)
            db.flush()

            recurring_income_rules_created += 1

        db.commit()

    except Exception:
        db.rollback()
        raise

    return FinancialProfileInitializationResult(
        categories_created=categories_created,
        categorization_rules_created=(
            categorization_rules_created
        ),
        recurring_income_rules_created=(
            recurring_income_rules_created
        )
    )