def test_get_user(client):
    headers = {"api-key": "test"}
    response = client.get("/api/users/me", headers=headers)
    assert response.status_code == 200
    # assert response.json()["user"]["name"] == "Ivan"