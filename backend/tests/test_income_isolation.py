def test_user_cannot_get_another_users_income(
    client,
    auth_headers,
    second_user_auth_headers
):
    create_response = client.post(
        "/incomes/",
        json={
            "amount": 1000,
            "source": "Salary",
            "expected_date": "2026-08-25"
        },
        headers=auth_headers
    )

    assert create_response.status_code == 201

    income_id = create_response.json()["id"]

    response = client.get(
        f"/incomes/{income_id}",
        headers=second_user_auth_headers
    )

    assert response.status_code == 404

def test_user_cannot_update_another_users_income(
    client,
    auth_headers,
    second_user_auth_headers
):
    create_response = client.post(
        "/incomes/",
        json={
            "amount": 1000,
            "source": "Salary",
            "expected_date": "2026-08-25"
        },
        headers=auth_headers
    )

    assert create_response.status_code == 201

    income_id = create_response.json()["id"]

    update_response = client.put(
        f"/incomes/{income_id}",
        json={
            "amount": 9999,
            "source": "Changed",
            "expected_date": "2026-08-30"
        },
        headers=second_user_auth_headers
    )

    assert update_response.status_code == 404

    owner_response = client.get(
        f"/incomes/{income_id}",
        headers=auth_headers
    )

    assert owner_response.status_code == 200

    income = owner_response.json()

    assert income["amount"] == "1000.00"
    assert income["source"] == "Salary"
    assert income["expected_date"] == "2026-08-25"

def test_user_cannot_receive_another_users_income(
    client,
    auth_headers,
    second_user_auth_headers
):
    create_response = client.post(
        "/incomes/",
        json={
            "amount": 1000,
            "source": "Salary",
            "expected_date": "2026-08-25"
        },
        headers=auth_headers
    )

    assert create_response.status_code == 201

    income_id = create_response.json()["id"]

    receive_response = client.patch(
        f"/incomes/{income_id}/receive",
        json={
            "received_date": "2026-08-25"
        },
        headers=second_user_auth_headers
    )

    assert receive_response.status_code == 404

    owner_response = client.get(
        f"/incomes/{income_id}",
        headers=auth_headers
    )

    assert owner_response.status_code == 200

    income = owner_response.json()

    assert income["status"] == "expected"
    assert income["received_date"] is None

def test_user_cannot_delete_another_users_income(
    client,
    auth_headers,
    second_user_auth_headers
):
    create_response = client.post(
        "/incomes/",
        json={
            "amount": 1000,
            "source": "Salary",
            "expected_date": "2026-08-25"
        },
        headers=auth_headers
    )

    assert create_response.status_code == 201

    income_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/incomes/{income_id}",
        headers=second_user_auth_headers
    )

    assert delete_response.status_code == 404

    owner_response = client.get(
        f"/incomes/{income_id}",
        headers=auth_headers
    )

    assert owner_response.status_code == 200


def test_user_only_sees_own_incomes(
    client,
    auth_headers,
    second_user_auth_headers
):
    create_response = client.post(
        "/incomes/",
        json={
            "amount": 1000,
            "source": "Salary",
            "expected_date": "2026-08-25"
        },
        headers=auth_headers
    )

    assert create_response.status_code == 201

    response = client.get(
        "/incomes/",
        headers=second_user_auth_headers
    )

    assert response.status_code == 200
    assert response.json() == []
    