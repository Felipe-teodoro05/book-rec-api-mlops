def test_create_user(client):
    payload = {
        "user_id": 123456789,  # ID nunca usado
        "location": "Rio de Janeiro",
        "age": 25
    }

    response = client.post("/users/", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert "message" in data
    assert "sucesso" in data["message"].lower()
