from unittest import mock


def test_login_route(test_client, db):
    response = test_client.get("/api/v1/auth/discord/login")
    assert response.status_code == 200
    assert "url" in response.json()
    assert response.json()["url"].startswith("https://discord.com/oauth2/authorize")
