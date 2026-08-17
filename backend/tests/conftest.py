import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.database import Base
from app.dependencies.db import get_db
from app.main import app

from app.models.user_model import UserModel
from app.models.category_model import CategoryModel
from app.models.expense_model import ExpenseModel
from app.models.income_model import IncomeModel
from app.models.obligation_model import ObligationModel


TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

if TEST_DATABASE_URL is None:
    raise RuntimeError(
        "TEST_DATABASE_URL environment variable is not set"
    )


test_engine = create_engine(
    TEST_DATABASE_URL
)


TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    autocommit=False
)


def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    yield

    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def client():
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def db_session():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def test_user_data():
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "TestPassword123"
    }


@pytest.fixture
def test_user(client, test_user_data):
    response = client.post(
        "/auth/register",
        json=test_user_data
    )

    assert response.status_code == 201

    return response.json()


@pytest.fixture
def auth_headers(client, test_user, test_user_data):
    response = client.post(
        "/auth/login",
        json={
            "email": test_user_data["email"],
            "password": test_user_data["password"]
        }
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


@pytest.fixture
def test_category(client, auth_headers):
    response = client.post(
        "/categories/",
        json={
            "name": "Test Category"
        },
        headers=auth_headers
    )

    assert response.status_code == 201

    return response.json()

@pytest.fixture
def second_user_data():
    return {
        "username": "seconduser",
        "email": "second@example.com",
        "password": "SecondPassword123"
    }


@pytest.fixture
def second_user_auth_headers(client, second_user_data):
    register_response = client.post(
        "/auth/register",
        json=second_user_data
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        json={
            "email": second_user_data["email"],
            "password": second_user_data["password"]
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }