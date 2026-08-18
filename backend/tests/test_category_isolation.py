def test_user_only_sees_own_categories(
    client,
    auth_headers,
    second_user_auth_headers
):
    create_response = client.post(
        "/categories/",
        json={
            "name": "User A Special Category"
        },
        headers=auth_headers
    )

    assert create_response.status_code == 201

    response = client.get(
        "/categories/",
        headers=second_user_auth_headers
    )

    assert response.status_code == 200

    categories = response.json()

    category_names = {
        category["name"]
        for category in categories
    }

    assert "User A Special Category" not in category_names


def test_user_cannot_update_another_users_category(
    client,
    auth_headers,
    second_user_auth_headers
):
    create_response = client.post(
        "/categories/",
        json={
            "name": "User A Editable Category"
        },
        headers=auth_headers
    )

    assert create_response.status_code == 201

    category_id = create_response.json()["id"]

    update_response = client.put(
        f"/categories/{category_id}",
        json={
            "name": "Changed"
        },
        headers=second_user_auth_headers
    )

    assert update_response.status_code == 404

    owner_response = client.get(
        "/categories/",
        headers=auth_headers
    )

    assert owner_response.status_code == 200

    categories = owner_response.json()

    category_names = {
        category["name"]
        for category in categories
    }

    assert "User A Editable Category" in category_names
    assert "Changed" not in category_names


def test_user_cannot_delete_another_users_category(
    client,
    auth_headers,
    second_user_auth_headers
):
    create_response = client.post(
        "/categories/",
        json={
            "name": "User A Delete Category"
        },
        headers=auth_headers
    )

    assert create_response.status_code == 201

    category_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/categories/{category_id}",
        headers=second_user_auth_headers
    )

    assert delete_response.status_code == 404

    owner_response = client.get(
        "/categories/",
        headers=auth_headers
    )

    assert owner_response.status_code == 200

    categories = owner_response.json()

    category_names = {
        category["name"]
        for category in categories
    }

    assert "User A Delete Category" in category_names


def test_register_creates_default_categories(
    client,
    test_user_data
):
    register_response = client.post(
        "/auth/register",
        json=test_user_data
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        json={
            "email": test_user_data["email"],
            "password": test_user_data["password"]
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.get(
        "/categories/",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    categories = response.json()

    category_names = {
        category["name"]
        for category in categories
    }

    assert category_names == {
        "Other Expenses",
        "Supermarket",
        "Fuel",
        "Electricity",
        "Water",
        "Telecom"
    }

    other_expenses = next(
        category
        for category in categories
        if category["name"] == "Other Expenses"
    )

    assert other_expenses["is_system"] is True

    normal_categories = [
        category
        for category in categories
        if category["name"] != "Other Expenses"
    ]

    assert all(
        category["is_system"] is False
        for category in normal_categories
    )