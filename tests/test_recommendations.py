def test_recommendations_valid_user(client):
    response = client.get("/recommendations/1")
    assert response.status_code == 200

    data = response.json()
    assert "recommendations" in data
    assert isinstance(data["recommendations"], list)
