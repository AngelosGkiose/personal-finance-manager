from decimal import Decimal


def test_expenses_by_category_calculates_totals_and_percentages(
    client,
    auth_headers,
    test_category
):
    second_category_response = client.post(
        "/categories/",
        json={
            "name": "Dining"
        },
        headers=auth_headers
    )

    assert second_category_response.status_code == 201

    second_category = second_category_response.json()

    expense_1 = client.post(
        "/expenses/",
        json={
            "amount": 100,
            "description": "Supermarket 1",
            "expense_date": "2026-08-10",
            "category_id": test_category["id"]
        },
        headers=auth_headers
    )

    assert expense_1.status_code == 201

    expense_2 = client.post(
        "/expenses/",
        json={
            "amount": 50,
            "description": "Supermarket 2",
            "expense_date": "2026-08-15",
            "category_id": test_category["id"]
        },
        headers=auth_headers
    )

    assert expense_2.status_code == 201

    expense_3 = client.post(
        "/expenses/",
        json={
            "amount": 50,
            "description": "Restaurant",
            "expense_date": "2026-08-17",
            "category_id": second_category["id"]
        },
        headers=auth_headers
    )

    assert expense_3.status_code == 201

    response = client.get(
        "/dashboard/expenses-by-category?month=8&year=2026",
        headers=auth_headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["month"] == 8
    assert data["year"] == 2026

    assert Decimal(
        data["total_expenses"]
    ) == Decimal("200.00")

    categories = {
        category["category_name"]: category
        for category in data["categories"]
    }

    test_category_data = categories["Test Category"]

    assert Decimal(
        test_category_data["amount"]
    ) == Decimal("150.00")

    assert Decimal(
        test_category_data["percentage"]
    ) == Decimal("75.00")

    dining_data = categories["Dining"]

    assert Decimal(
        dining_data["amount"]
    ) == Decimal("50.00")

    assert Decimal(
        dining_data["percentage"]
    ) == Decimal("25.00")


def test_expenses_by_category_only_uses_current_users_expenses(
    client,
    auth_headers,
    second_user_auth_headers,
    test_category
):
    user_a_expense = client.post(
        "/expenses/",
        json={
            "amount": 100,
            "description": "User A Expense",
            "expense_date": "2026-08-17",
            "category_id": test_category["id"]
        },
        headers=auth_headers
    )

    assert user_a_expense.status_code == 201

    user_b_category_response = client.post(
        "/categories/",
        json={
            "name": "User B Category"
        },
        headers=second_user_auth_headers
    )

    assert user_b_category_response.status_code == 201

    user_b_category = user_b_category_response.json()

    user_b_expense = client.post(
        "/expenses/",
        json={
            "amount": 500,
            "description": "User B Expense",
            "expense_date": "2026-08-17",
            "category_id": user_b_category["id"]
        },
        headers=second_user_auth_headers
    )

    assert user_b_expense.status_code == 201

    response = client.get(
        "/dashboard/expenses-by-category?month=8&year=2026",
        headers=auth_headers
    )

    assert response.status_code == 200

    data = response.json()

    assert Decimal(
        data["total_expenses"]
    ) == Decimal("100.00")

    assert len(data["categories"]) == 1

    category = data["categories"][0]

    assert category["category_name"] == "Test Category"

    assert Decimal(
        category["amount"]
    ) == Decimal("100.00")

    assert Decimal(
        category["percentage"]
    ) == Decimal("100.00")