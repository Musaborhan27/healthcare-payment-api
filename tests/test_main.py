def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_register(client):
    response = client.post(
        "/users/register",
        params={
            "email": "test_register@example.com",
            "password": "admin123"
        }
    )
    assert response.status_code == 200
    body = response.json()
    assert body["email"] == "test_register@example.com"
    assert body["role"] == "user"


def test_login(client):
    register_response = client.post(
        "/users/register",
        params={
            "email": "test_login@example.com",
            "password": "admin123"
        }
    )
    assert register_response.status_code == 200

    response = client.post(
        "/auth/login",
        data={
            "username": "test_login@example.com",
            "password": "admin123",
            "grant_type": "password"
        }
    )
    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"