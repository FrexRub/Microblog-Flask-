import pytest


def test_get_user_me(client):
    headers = {"api-key": "test"}
    response = client.get("/api/users/me", headers=headers)
    result = response.json
    assert response.status_code == 200
    assert result["user"]["name"] == "Ivan"


@pytest.mark.parametrize("route", ["/api/users/1", "/api/users/2", "/api/users/3", "/api/users/4"])
def test_get_user_id(client, route):
    headers = {"api-key": "test"}
    response = client.get(route, headers=headers)
    result = response.json
    assert response.status_code == 200