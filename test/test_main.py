def test_get_user_me(client):
    headers = {"api-key": "test"}
    response = client.get("/api/users/me", headers=headers)
    result = response.json
    assert response.status_code == 200
    assert result["user"]["name"] == "Ivan"