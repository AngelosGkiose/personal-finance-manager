def test_get_current_user(client, auth_headers):
    response = client.get(
        "/auth/me",
        headers=auth_headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"

def test_create_category_fixture(test_category):
    assert test_category["name"] == "Test Category"
    assert "id" in test_category