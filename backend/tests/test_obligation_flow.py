from decimal import Decimal


def test_pay_obligation_updates_expenses_and_dashboard(
    client,
    auth_headers,
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

    obligation = create_response.json()
    obligation_id = obligation["id"]

    assert obligation["status"] == "pending"
    assert obligation["paid_date"] is None
    assert obligation["expense_id"] is None


    dashboard_before_response = client.get(
        "/dashboard/monthly?month=8&year=2026",
        headers=auth_headers
    )

    assert dashboard_before_response.status_code == 200

    dashboard_before = dashboard_before_response.json()

    assert Decimal(dashboard_before["expenses"]) == Decimal("0.00")
    assert Decimal(dashboard_before["pending_obligations"]) == Decimal("100.00")


    pay_response = client.patch(
        f"/obligations/{obligation_id}/pay",
        json={
            "paid_date": "2026-08-17"
        },
        headers=auth_headers
    )

    assert pay_response.status_code == 200

    paid_obligation = pay_response.json()

    assert paid_obligation["status"] == "paid"
    assert paid_obligation["paid_date"] == "2026-08-17"
    assert paid_obligation["expense_id"] is not None

    expense_id = paid_obligation["expense_id"]


    expense_response = client.get(
        f"/expenses/{expense_id}",
        headers=auth_headers
    )

    assert expense_response.status_code == 200

    expense = expense_response.json()

    assert expense["description"] == "Protergia"
    assert Decimal(expense["amount"]) == Decimal("100.00")
    assert expense["expense_date"] == "2026-08-17"
    assert expense["category_id"] == test_category["id"]


    dashboard_after_response = client.get(
        "/dashboard/monthly?month=8&year=2026",
        headers=auth_headers
    )

    assert dashboard_after_response.status_code == 200

    dashboard_after = dashboard_after_response.json()

    assert Decimal(dashboard_after["expenses"]) == Decimal("100.00")
    assert Decimal(dashboard_after["pending_obligations"]) == Decimal("0.00")

def test_obligation_cannot_be_paid_twice(
    client,
    auth_headers,
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

    obligation_id = create_response.json()["id"]

    first_payment = client.patch(
        f"/obligations/{obligation_id}/pay",
        json={
            "paid_date": "2026-08-17"
        },
        headers=auth_headers
    )

    assert first_payment.status_code == 200

    second_payment = client.patch(
        f"/obligations/{obligation_id}/pay",
        json={
            "paid_date": "2026-08-17"
        },
        headers=auth_headers
    )

    assert second_payment.status_code == 409
    assert second_payment.json()["detail"] == "Obligation is already paid"