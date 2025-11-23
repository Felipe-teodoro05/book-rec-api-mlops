def test_create_preference(client):

    # Criar usuário único
    client.post("/users/", json={
        "user_id": 654321,
        "location": "Teste",
        "age": 30
    })

    # Criar item único
    client.post("/items/", json={
        "isbn": "TEST-PREF-789",
        "book_title": "Livro Pré",
        "book_author": "Autor Pré",
        "year_of_publication": 2021,
        "publisher": "Pré Editora"
    })

    # Criar avaliação
    payload = {
        "user_id": 654321,
        "isbn": "TEST-PREF-789",
        "rating": 9
    }

    response = client.post("/preferences/", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert "message" in data
    assert "sucesso" in data["message"].lower()
