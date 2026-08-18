from decimal import Decimal


def test_monthly_dashboard_only_uses_current_users_data(
    client,
    auth_headers,
    second_user_auth_headers,
    test_category
):
    # -------------------------
    # User A data
    # -------------------------

    expense_a = client.post(
        "/expenses/",
        json={
            "amount": 100,
            "description": "User A Expense",
            "expense_date": "2026-08-17",
            "category_id": test_category["id"]
        },
        headers=auth_headers
    )

    assert expense_a.status_code == 201

    income_a = client.post(
        "/incomes/",
        json={
            "amount": 500,
            "source": "User A Income",
            "expected_date": "2026-08-20"
        },
        headers=auth_headers
    )

    assert income_a.status_code == 201

    obligation_a = client.post(
        "/obligations/",
        json={
            "title": "User A Bill",
            "amount": 50,
            "due_date": "2026-08-25",
            "category_id": test_category["id"]
        },
        headers=auth_headers
    )

    assert obligation_a.status_code == 201


    # -------------------------
    # User B category
    # -------------------------

    category_b_response = client.post(
        "/categories/",
        json={
            "name": "User B Category"
        },
        headers=second_user_auth_headers
    )

    assert category_b_response.status_code == 201

    category_b = category_b_response.json()


    # -------------------------
    # User B data
    # -------------------------

    expense_b = client.post(
        "/expenses/",
        json={
            "amount": 20,
            "description": "User B Expense",
            "expense_date": "2026-08-17",
            "category_id": category_b["id"]
        },
        headers=second_user_auth_headers
    )

    assert expense_b.status_code == 201

    income_b = client.post(
        "/incomes/",
        json={
            "amount": 80,
            "source": "User B Income",
            "expected_date": "2026-08-20"
        },
        headers=second_user_auth_headers
    )

    assert income_b.status_code == 201

    obligation_b = client.post(
        "/obligations/",
        json={
            "title": "User B Bill",
            "amount": 30,
            "due_date": "2026-08-25",
            "category_id": category_b["id"]
        },
        headers=second_user_auth_headers
    )

    assert obligation_b.status_code == 201


    # -------------------------
    # User A dashboard
    # -------------------------

    dashboard_a_response = client.get(
        "/dashboard/monthly?month=8&year=2026",
        headers=auth_headers
    )

    assert dashboard_a_response.status_code == 200

    dashboard_a = dashboard_a_response.json()

    assert Decimal(dashboard_a["received_income"]) == Decimal("0.00")
    assert Decimal(dashboard_a["expected_income"]) == Decimal("500.00")
    assert Decimal(dashboard_a["expenses"]) == Decimal("100.00")
    assert Decimal(dashboard_a["pending_obligations"]) == Decimal("50.00")

    assert Decimal(dashboard_a["monthly_balance"]) == Decimal("-100.00")
    assert Decimal(dashboard_a["projected_balance"]) == Decimal("350.00")


    # -------------------------
    # User B dashboard
    # -------------------------

    dashboard_b_response = client.get(
        "/dashboard/monthly?month=8&year=2026",
        headers=second_user_auth_headers
    )

    assert dashboard_b_response.status_code == 200

    dashboard_b = dashboard_b_response.json()

    assert Decimal(dashboard_b["received_income"]) == Decimal("0.00")
    assert Decimal(dashboard_b["expected_income"]) == Decimal("80.00")
    assert Decimal(dashboard_b["expenses"]) == Decimal("20.00")
    assert Decimal(dashboard_b["pending_obligations"]) == Decimal("30.00")

    assert Decimal(dashboard_b["monthly_balance"]) == Decimal("-20.00")
    assert Decimal(dashboard_b["projected_balance"]) == Decimal("30.00")