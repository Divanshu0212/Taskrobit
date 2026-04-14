def auth_header(client, email="tasks@example.com", username="taskuser"):
    client.post(
        "/api/v1/auth/register",
        json={"email": email, "username": username, "password": "strongpass123"},
    )
    login = client.post("/api/v1/auth/login", json={"email": email, "password": "strongpass123"}).json()
    return {"Authorization": f"Bearer {login['access_token']}"}


def test_create_task(client):
    headers = auth_header(client)
    response = client.post(
        "/api/v1/tasks/",
        headers=headers,
        json={"title": "Write docs", "description": "Finish API docs", "priority": "high"},
    )
    assert response.status_code == 201


def test_get_tasks(client):
    headers = auth_header(client)
    client.post("/api/v1/tasks/", headers=headers, json={"title": "Task 1"})
    response = client.get("/api/v1/tasks/", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_update_task(client):
    headers = auth_header(client)
    task = client.post("/api/v1/tasks/", headers=headers, json={"title": "Task 1"}).json()
    response = client.put(f"/api/v1/tasks/{task['id']}", headers=headers, json={"status": "completed"})
    assert response.status_code == 200
    assert response.json()["status"] == "completed"


def test_delete_task(client):
    headers = auth_header(client)
    task = client.post("/api/v1/tasks/", headers=headers, json={"title": "Task 1"}).json()
    response = client.delete(f"/api/v1/tasks/{task['id']}", headers=headers)
    assert response.status_code == 204


def test_user_cannot_access_others_task(client):
    owner_headers = auth_header(client, "owner@example.com", "owner")
    other_headers = auth_header(client, "other@example.com", "other")
    task = client.post("/api/v1/tasks/", headers=owner_headers, json={"title": "Private"}).json()

    response = client.get(f"/api/v1/tasks/{task['id']}", headers=other_headers)
    assert response.status_code == 404
