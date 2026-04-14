def test_register_success(client):
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "user1@example.com", "username": "user1", "password": "strongpass123"},
    )
    assert response.status_code == 201
    assert response.json()["email"] == "user1@example.com"


def test_register_duplicate_email(client):
    payload = {"email": "dup@example.com", "username": "dup1", "password": "strongpass123"}
    client.post("/api/v1/auth/register", json=payload)
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "dup@example.com", "username": "dup2", "password": "strongpass123"},
    )
    assert response.status_code == 400


def test_login_success(client):
    client.post(
        "/api/v1/auth/register",
        json={"email": "login@example.com", "username": "loginuser", "password": "strongpass123"},
    )
    response = client.post("/api/v1/auth/login", json={"email": "login@example.com", "password": "strongpass123"})
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_wrong_password(client):
    client.post(
        "/api/v1/auth/register",
        json={"email": "wrong@example.com", "username": "wronguser", "password": "strongpass123"},
    )
    response = client.post("/api/v1/auth/login", json={"email": "wrong@example.com", "password": "badpass123"})
    assert response.status_code == 401


def test_get_me_unauthorized(client):
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401
