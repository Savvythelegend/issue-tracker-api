def test_refresh_token(client):
    client.post("/register", json={"email": "a@a.com", "password": "pass"})
    res = client.post("/login", json={"email": "a@a.com", "password": "pass"})
    refresh_token = res.json["refresh_token"]

    res = client.post("/refresh", headers={"Authorization": f"Bearer {refresh_token}"})
    assert res.status_code == 200
    assert "access_token" in res.json


def test_logout_revokes_access_token(client):
    client.post("/register", json={"email": "a@a.com", "password": "pass"})
    res = client.post("/login", json={"email": "a@a.com", "password": "pass"})
    access_token = res.json["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    # Log out to blacklist token
    res = client.post("/logout", headers=headers)
    assert res.status_code == 200

    # Try using the blacklisted token again
    res = client.get("/issues", headers=headers)
    assert res.status_code == 401


def test_logout_refresh_revokes_refresh_token(client):
    client.post("/register", json={"email": "a@a.com", "password": "pass"})
    res = client.post("/login", json={"email": "a@a.com", "password": "pass"})
    refresh_token = res.json["refresh_token"]
    headers = {"Authorization": f"Bearer {refresh_token}"}

    # Logout refresh token
    res = client.post("/logout-refresh", headers=headers)
    assert res.status_code == 200

    # Try to use refresh token again
    res = client.post("/refresh", headers=headers)
    assert res.status_code == 401
