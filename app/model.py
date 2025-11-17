import os
import pickle
import pandas as pd
from sqlalchemy import create_engine
from surprise import SVD
from dotenv import load_dotenv   # <-- IMPORTANTE: carregar .env

# ======================================================
# 1. CARREGAR VARIÁVEIS DO .env ANTES DE TUDO
# ======================================================
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL não encontrada. Verifique seu arquivo .env")

# ======================================================
# 2. CRIAR ENGINE
# ======================================================
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# ======================================================
# 3. CARREGAR MODELO TREINADO
# ======================================================
MODEL_PATH = "app/model_artifacts/svd_model.pkl"

def load_model():
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    return model

svd_model = load_model()

# ======================================================
# 4. FUNÇÃO DE RECOMENDAÇÃO
# ======================================================
def get_recommendations(user_id: int, top_n: int = 10):
    """
    Retorna os TOP-N livros recomendados para o usuário.
    """

    # 1) Carregar livros do banco
    books = pd.read_sql("SELECT isbn, book_title, book_author FROM books", engine)

    # 2) Carregar avaliações do usuário
    ratings = pd.read_sql(f"SELECT isbn FROM ratings WHERE user_id={user_id}", engine)
    already_rated = set(ratings["isbn"].tolist())

    # 3) Prever nota para cada livro não avaliado
    predictions = []
    for _, row in books.iterrows():
        isbn = row["isbn"]

        if isbn in already_rated:
            continue

        pred = svd_model.predict(str(user_id), str(isbn)).est
        predictions.append((isbn, row["book_title"], row["book_author"], pred))

    # 4) Ordenar por nota prevista
    predictions.sort(key=lambda x: x[3], reverse=True)

    # 5) Retornar top_n
    results = [
        {
            "isbn": isbn,
            "title": title,
            "author": author,
            "predicted_rating": float(score)
        }
        for isbn, title, author, score in predictions[:top_n]
    ]

    return results
