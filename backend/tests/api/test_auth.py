from jwt import encode


def test_authenticated_no_header(test_client, db):
    response = test_client.get("/api/v1/auth/authenticated")
    assert response.status_code == 200
    assert response.json() == {"is_authenticated": False}


def test_authenticated_invalid_provider(test_client, db):
    token = encode({"sub": "expired_token"}, "SECRET_KEY", algorithm="HS256")
    headers = {
        "authorization": f"Bearer {token}"
    }
    response = test_client.get("/api/v1/auth/authenticated", headers=headers,
                               params={"auth_provider": "invalid_provider"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid auth provider"}


def test_authenticated_expired_token(test_client, db):
    expired_token = encode({"sub": "expired_token", "exp": 0}, "SECRET_KEY", algorithm="HS256")
    headers = {
        "authorization": f"Bearer {expired_token}"
    }
    response = test_client.get("/api/v1/auth/authenticated", headers=headers, params={"auth_provider": "google"})

    assert response.status_code == 401
    assert response.json() == {"detail": "Token has expired"}


def test_logout(test_client, db):
    response = test_client.get("/api/v1/auth/logout")

    assert response.status_code == 200
    assert response.json() == {"redirect_url": "http://localhost:4000"}
