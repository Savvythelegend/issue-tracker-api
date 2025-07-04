def register_and_login(client, email="a@a.com", password="pass"):
    client.post("/register", json={"email": email, "password": password})
    res = client.post("/login", json={"email": email, "password": password})
    return res.json["access_token"]


def test_create_issue(client):
    token = register_and_login(client)
    headers = {"Authorization": f"Bearer {token}"}
    res = client.post(
        "/issues",
        json={"title": "Sample Issue", "description": "Test description"},
        headers=headers,
    )

    assert res.status_code == 201
    assert res.json["title"] == "Sample Issue"


def test_list_issues(client):
    token = register_and_login(client)
    headers = {"Authorization": f"Bearer {token}"}

    # Create an issue
    client.post("/issues", json={"title": "T", "description": "D"}, headers=headers)

    res = client.get("/issues", headers=headers)
    assert res.status_code == 200
    assert isinstance(res.json, list)


def test_get_single_issue(client):
    token = register_and_login(client)
    headers = {"Authorization": f"Bearer {token}"}

    post = client.post(
        "/issues", json={"title": "T", "description": "D"}, headers=headers
    )
    issue_id = post.json["id"]

    res = client.get(f"/issues/{issue_id}", headers=headers)
    assert res.status_code == 200
    assert res.json["id"] == issue_id


def test_update_issue(client):
    token = register_and_login(client)
    headers = {"Authorization": f"Bearer {token}"}

    post = client.post(
        "/issues", json={"title": "Old", "description": "Old"}, headers=headers
    )
    issue_id = post.json["id"]

    res = client.put(
        f"/issues/{issue_id}",
        json={"title": "New", "description": "New"},
        headers=headers,
    )
    assert res.status_code == 200
    assert res.json["title"] == "New"


def test_patch_issue_status(client):
    token = register_and_login(client)
    headers = {"Authorization": f"Bearer {token}"}

    post = client.post(
        "/issues", json={"title": "Bug", "description": "Fix me"}, headers=headers
    )
    issue_id = post.json["id"]

    res = client.patch(
        f"/issues/{issue_id}", json={"status": "closed"}, headers=headers
    )
    assert res.status_code == 200
    assert res.json["status"] == "closed"


def test_delete_issue(client):
    token = register_and_login(client)
    headers = {"Authorization": f"Bearer {token}"}

    post = client.post(
        "/issues", json={"title": "To Delete", "description": "Bye"}, headers=headers
    )
    issue_id = post.json["id"]

    res = client.delete(f"/issues/{issue_id}", headers=headers)
    assert res.status_code == 204
