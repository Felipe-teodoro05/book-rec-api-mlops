import os
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from app.model import get_recommendations
from pydantic import BaseModel


class Preference(BaseModel):
    user_id: int
    isbn: str
    rating: int


# Carrega as variáveis de ambiente (do .env)
# O Docker Compose vai garantir que o container veja esse .env
load_dotenv()

app = FastAPI(
    title="Sistema de Recomendação de Livros",
    description="API para o projeto de recomendação com Neon DB e Docker.",
    version="0.1"
)

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("Variável DATABASE_URL não encontrada. Verifique seu .env")

# Cria a "engine" do SQLAlchemy.
try:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    print("Conexão com Neon (engine) criada com sucesso.")
except Exception as e:
    print(f"Erro ao criar a engine do DB: {e}")
    engine = None

# Endpoints da API


@app.get("/")
def read_root():
    """ Rota raiz para verificar se a API está online. """
    return {"message": "API de Recomendação no ar! Acesse /docs para documentação."}


@app.get("/test-db")
def test_database_connection():
    """
    Endpoint de diagnóstico para testar a conexão com o banco Neon.
    Tenta executar uma consulta SQL simples.
    """
    if engine is None:
        raise HTTPException(
            status_code=500, detail="Conexão com o banco de dados falhou na inicialização.")

    try:
        with engine.connect() as connection:
            query = text("SELECT COUNT(*) FROM users;")
            result = connection.execute(query)

            # Pega o primeiro (e único) resultado
            user_count = result.scalar()

            return {
                "message": "Conexão com o Neon DB bem-sucedida!",
                "user_count_from_db": user_count
            }

    except Exception as e:
        print(f"Erro no endpoint /test-db: {e}")
        raise HTTPException(
            status_code=500, detail=f"Erro ao consultar o banco de dados: {str(e)}")


@app.get("/recommendations/{user_id}")
def recommend(user_id: int, top_n: int = 10):
    try:
        recs = get_recommendations(user_id, top_n)
        return {"user_id": user_id, "recommendations": recs}
    except Exception as e:
        print("Erro ao gerar recomendações:", e)
        raise HTTPException(
            status_code=500, detail="Erro ao processar recomendações")


@app.post("/preferences/")
def add_preference(pref: Preference):
    """
    Salva uma nova avaliação (rating) do usuário no banco Neon.
    """
    try:
        with engine.connect() as conn:
            query = text("""
                INSERT INTO ratings (user_id, isbn, book_rating)
                VALUES (:user_id, :isbn, :rating)
            """)

            conn.execute(query, {
                "user_id": pref.user_id,
                "isbn": pref.isbn,
                "rating": pref.rating
            })

            conn.commit()

        return {
            "message": "Avaliação salva com sucesso!",
            "user_id": pref.user_id,
            "isbn": pref.isbn,
            "rating": pref.rating
        }

    except Exception as e:
        print("Erro ao salvar preferência:", e)
        raise HTTPException(
            status_code=500,
            detail="Erro ao salvar avaliação no banco."
        )


class UserCreate(BaseModel):
    user_id: int
    location: str | None = None
    age: int | None = None


@app.post("/users/")
def create_user(user: UserCreate):
    try:
        with engine.connect() as conn:
            query = text("""
                INSERT INTO users (user_id, location, age)
                VALUES (:user_id, :location, :age)
            """)
            conn.execute(query, {
                "user_id": user.user_id,
                "location": user.location,
                "age": user.age
            })
            conn.commit()

        return {"message": "Usuário criado com sucesso!"}

    except Exception as e:
        print("Erro ao inserir usuário:", e)
        raise HTTPException(
            status_code=500,
            detail="Erro ao adicionar usuário."
        )


class ItemCreate(BaseModel):
    isbn: str
    book_title: str
    book_author: str | None = None
    year_of_publication: int | None = None
    publisher: str | None = None


@app.post("/items/")
def create_item(item: ItemCreate):
    try:
        with engine.connect() as conn:
            query = text("""
                INSERT INTO books (isbn, book_title, book_author, year_of_publication, publisher)
                VALUES (:isbn, :book_title, :book_author, :year, :publisher)
            """)
            conn.execute(query, {
                "isbn": item.isbn,
                "book_title": item.book_title,
                "book_author": item.book_author,
                "year": item.year_of_publication,
                "publisher": item.publisher
            })
            conn.commit()

        return {"message": "Livro adicionado com sucesso!"}

    except Exception as e:
        print("Erro ao inserir livro:", e)
        raise HTTPException(
            status_code=500,
            detail="Erro ao adicionar livro."
        )
