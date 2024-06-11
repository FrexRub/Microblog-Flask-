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


def test_get_user_id_error(client):
    headers = {"api-key": "test"}
    response = client.get("/api/users/10", headers=headers)
    result = response.json
    print(result)
    assert response.status_code == 418
    assert result["result"] == False


def test_get_tweet(client):
    headers = {"api-key": "test"}
    response = client.get("/api/tweets/", headers=headers)
    assert response.status_code == 200


def test_post_tweet(client):
    headers = {"api-key": "test"}
    tweet = {"tweet_data": "Hi", "tweet_media_ids": [0]}
    response = client.post("/api/tweets/", headers=headers, json=tweet)
    result = response.json
    assert response.status_code == 201
    assert result["tweet_id"] == 1


def test_post_likes_tweet(client):
    headers = {"api-key": "test1"}
    response = client.post("/api/tweets/1/likes", headers=headers, )
    result = response.json
    assert response.status_code == 201


def test_delete_likes_twee_bad(client):
    headers = {"api-key": "test"}
    response = client.delete("/api/tweets/1/likes", headers=headers)
    assert response.status_code == 400


def test_delete_likes_twee(client):
    headers = {"api-key": "test1"}
    response = client.delete("/api/tweets/1/likes", headers=headers)
    result = response.json
    assert response.status_code == 200


def test_delete_tweet(client):
    headers = {"api-key": "test"}
    response = client.delete("/api/tweets/1", headers=headers)
    result = response.json
    assert response.status_code == 200
