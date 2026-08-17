def test_user_only_sees_own_categories(
    client,
    auth_headers,
    second_user_auth_headers
):
    create_response = client.post(
        "/categories/",
        json={
            "name": "Electricity"
        },
        headers=auth_headers
    )

    assert create_response.status_code == 201

    response = client.get(
        "/categories/",
        headers=second_user_auth_headers
    )

    assert response.status_code == 200
    assert response.json() == []

def test_user_cannot_update_another_users_category(
    client,
    auth_headers,
    second_user_auth_headers
):
    create_response = client.post(
        "/categories/",
        json={
            "name": "Electricity"
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

    assert len(categories) == 1
    assert categories[0]["name"] == "Electricity"


def test_user_cannot_delete_another_users_category(
    client,
    auth_headers,
    second_user_auth_headers
):
    create_response = client.post(
        "/categories/",
        json={
            "name": "Electricity"
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
    assert len(owner_response.json()) == 1