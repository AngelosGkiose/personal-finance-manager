def test_user_cannot_get_another_users_expense(
    client,
    auth_headers,
    second_user_auth_headers,
    test_category
):
    create_response = client.post(
        "/expenses/",
        json={
            "amount": 50,
            "description": "Shell",
            "expense_date": "2026-08-17",
            "category_id": test_category["id"]
        },
        headers=auth_headers
    )

    assert create_response.status_code == 201

    expense_id = create_response.json()["id"]

    response = client.get(
        f"/expenses/{expense_id}",
        headers=second_user_auth_headers
    )

    assert response.status_code == 404


def test_user_cannot_update_another_users_expense(
    client,
    auth_headers,
    second_user_auth_headers,
    test_category
):
    create_response = client.post(
        "/expenses/",
        json={
            "amount": 50,
            "description": "Shell",
            "expense_date": "2026-08-17",
            "category_id": test_category["id"]
        },
        headers=auth_headers
    )

    assert create_response.status_code == 201

    expense_id = create_response.json()["id"]

    update_response = client.put(
        f"/expenses/{expense_id}",
        json={
            "amount": 999,
            "description": "Changed",
            "expense_date": "2026-08-17",
            "category_id": test_category["id"]
        },
        headers=second_user_auth_headers
    )

    assert update_response.status_code == 404

    owner_response = client.get(
        f"/expenses/{expense_id}",
        headers=auth_headers
    )

    assert owner_response.status_code == 200

    expense = owner_response.json()

    assert expense["amount"] == "50.00"
    assert expense["description"] == "Shell"

def test_user_cannot_delete_another_users_expense(
    client,
    auth_headers,
    second_user_auth_headers,
    test_category
):
    create_response = client.post(
        "/expenses/",
        json={
            "amount": 50,
            "description": "Shell",
            "expense_date": "2026-08-17",
            "category_id": test_category["id"]
        },
        headers=auth_headers
    )

    assert create_response.status_code == 201

    expense_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/expenses/{expense_id}",
        headers=second_user_auth_headers
    )

    assert delete_response.status_code == 404

    owner_response = client.get(
        f"/expenses/{expense_id}",
        headers=auth_headers
    )

    assert owner_response.status_code == 200

def test_user_only_sees_own_expenses(
    client,
    auth_headers,
    second_user_auth_headers,
    test_category
):
    create_response = client.post(
        "/expenses/",
        json={
            "amount": 50,
            "description": "Shell",
            "expense_date": "2026-08-17",
            "category_id": test_category["id"]
        },
        headers=auth_headers
    )

    assert create_response.status_code == 201

    response = client.get(
        "/expenses/",
        headers=second_user_auth_headers
    )

    assert response.status_code == 200
    assert response.json() == []