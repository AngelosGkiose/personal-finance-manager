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