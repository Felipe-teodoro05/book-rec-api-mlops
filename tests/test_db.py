def test_test_db(client):
    response = client.get("/test-db")
    assert response.status_code == 200

    data = response.json()
    assert "message" in data
    assert "user_count_from_db" in data
    assert isinstance(data["user_count_from_db"], int)
