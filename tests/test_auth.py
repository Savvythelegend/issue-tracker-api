# tests/test_auth.py


def test_register_user(client):
    payload = {"email": "user1@example.com", "password": "pass1234"}
    response = client.post("/register", json=payload)
    assert response.status_code == 201


def test_register_duplicate_email(client):
    payload = {"email": "user2@example.com", "password": "pass1234"}
    # First registration
    client.post("/register", json=payload)

    # Second attempt with same email
    response = client.post("/register", json=payload)
    assert response.status_code == 400


def test_login_success(client):
    # Register first
    payload = {"email": "user3@example.com", "password": "pass1234"}
    client.post("/register", json=payload)

    # Login
    response = client.post("/login", json=payload)
    assert response.status_code == 200
    assert "access_token" in response.json
    assert "refresh_token" in response.json


def test_login_invalid_password(client):
    # Register first
    client.post(
        "/register", json={"email": "user4@example.com", "password": "pass1234"}
    )

    # Wrong password
    response = client.post(
        "/login", json={"email": "user4@example.com", "password": "wrongpass"}
    )
    assert response.status_code == 401


def test_login_nonexistent_user(client):
    response = client.post(
        "/login", json={"email": "nouser@example.com", "password": "whatever"}
    )
    assert response.status_code == 401
