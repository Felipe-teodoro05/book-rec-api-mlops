def test_create_item(client):
    payload = {
        "isbn": "TEST-BOOK-456",   # novo ISBN único
        "book_title": "Livro Teste 2",
        "book_author": "Autor X",
        "year_of_publication": 2022,
        "publisher": "Editora X"
    }

    response = client.post("/items/", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert "message" in data
    assert "sucesso" in data["message"].lower()
