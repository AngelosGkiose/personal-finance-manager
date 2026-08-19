from app.models.user_model import UserModel
from app.repositories.category_repository import get_category_by_name
from app.services.categorization_service import (
    create_categorization_rule_service,
    find_category_for_transaction_service,
)


def test_categorization_rule_matches_transaction_and_uses_fallback(
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

    fuel_category = get_category_by_name(
        db=db_session,
        current_user_id=current_user.id,
        category_name="Fuel"
    )

    assert fuel_category is not None

    rule = create_categorization_rule_service(
        keyword="  shell  ",
        category_id=fuel_category.id,
        current_user=current_user,
        db=db_session
    )

    assert rule.keyword == "SHELL"
    assert rule.category_id == fuel_category.id

    matched_category = find_category_for_transaction_service(
        description="Shell Kifisias Store 123",
        current_user=current_user,
        db=db_session
    )

    assert matched_category.name == "Fuel"

    fallback_category = find_category_for_transaction_service(
        description="Unknown Merchant Athens",
        current_user=current_user,
        db=db_session
    )

    assert fallback_category.name == "Other Expenses"
    assert fallback_category.is_system is True