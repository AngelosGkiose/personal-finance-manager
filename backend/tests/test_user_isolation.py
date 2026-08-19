import pytest
from fastapi import HTTPException

from app.models.user_model import UserModel
from app.repositories.category_repository import get_category_by_name
from app.services.categorization_service import find_category_for_transaction_service, \
    create_categorization_rule_service


def test_user_cannot_get_another_users_obligation(
    client,
    auth_headers,
    second_user_auth_headers,
    test_category
):
    create_response = client.post(
        "/obligations/",
        json={
            "title": "Protergia",
            "amount": 100,
            "due_date": "2026-08-25",
            "category_id": test_category["id"]
        },
        headers=auth_headers
    )

    assert create_response.status_code == 201

    obligation_id = create_response.json()["id"]

    response = client.get(
        f"/obligations/{obligation_id}",
        headers=second_user_auth_headers
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Obligation not found"


def test_user_cannot_pay_another_users_obligation(
    client,
    auth_headers,
    second_user_auth_headers,
    test_category
):
    create_response = client.post(
        "/obligations/",
        json={
            "title": "Vodafone",
            "amount": 50,
            "due_date": "2026-08-25",
            "category_id": test_category["id"]
        },
        headers=auth_headers
    )

    assert create_response.status_code == 201

    obligation_id = create_response.json()["id"]

    pay_response = client.patch(
        f"/obligations/{obligation_id}/pay",
        json={
            "paid_date": "2026-08-17"
        },
        headers=second_user_auth_headers
    )

    assert pay_response.status_code == 404
    assert pay_response.json()["detail"] == "Obligation not found"

    obligation_response = client.get(
        f"/obligations/{obligation_id}",
        headers=auth_headers
    )

    assert obligation_response.status_code == 200

    obligation = obligation_response.json()

    assert obligation["status"] == "pending"
    assert obligation["paid_date"] is None
    assert obligation["expense_id"] is None


def test_categorization_rules_are_isolated_between_users(
    db_session,
    test_user,
    test_user_data,
    second_user_auth_headers,
    second_user_data
):
    user_a = (
        db_session.query(UserModel)
        .filter(
            UserModel.email == test_user_data["email"]
        )
        .first()
    )

    user_b = (
        db_session.query(UserModel)
        .filter(
            UserModel.email == second_user_data["email"]
        )
        .first()
    )

    assert user_a is not None
    assert user_b is not None

    fuel_category_a = get_category_by_name(
        db=db_session,
        current_user_id=user_a.id,
        category_name="Fuel"
    )

    assert fuel_category_a is not None

    create_categorization_rule_service(
        keyword="SHELL",
        category_id=fuel_category_a.id,
        current_user=user_a,
        db=db_session
    )

    category_for_user_a = find_category_for_transaction_service(
        description="SHELL KIFISIAS",
        current_user=user_a,
        db=db_session
    )

    assert category_for_user_a.name == "Fuel"

    category_for_user_b = find_category_for_transaction_service(
        description="SHELL KIFISIAS",
        current_user=user_b,
        db=db_session
    )

    assert category_for_user_b.name == "Other Expenses"
    assert category_for_user_b.is_system is True

def test_user_cannot_create_duplicate_categorization_rule(
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

    create_categorization_rule_service(
        keyword="SHELL",
        category_id=fuel_category.id,
        current_user=current_user,
        db=db_session
    )

    with pytest.raises(HTTPException) as exc:
        create_categorization_rule_service(
            keyword=" shell ",
            category_id=fuel_category.id,
            current_user=current_user,
            db=db_session
        )

    assert exc.value.status_code == 409
    assert exc.value.detail == "Categorization rule already exists"