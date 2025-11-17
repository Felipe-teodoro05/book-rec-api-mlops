import os
import pandas as pd
from sqlalchemy import create_engine
from surprise import Dataset, Reader, SVD
import pickle
from dotenv import load_dotenv

# ===============================
# 1. Carrega variável de ambiente
# ===============================
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL não encontrada no .env")

engine = create_engine(DATABASE_URL)

# ===============================
# 2. Puxa os dados do banco Neon
# ===============================
print("🔄 Carregando dados do banco...")

query = """
SELECT user_id, isbn, book_rating
FROM ratings
WHERE book_rating > 0;
"""

df = pd.read_sql(query, engine)

print(f"📘 Total de avaliações carregadas: {len(df)}")

# ===============================
# 3. Prepara para o Surprise (SVD)
# ===============================
reader = Reader(rating_scale=(1, 10))

data = Dataset.load_from_df(
    df[["user_id", "isbn", "book_rating"]],
    reader
)

trainset = data.build_full_trainset()

# ===============================
# 4. Treinar o modelo SVD
# ===============================
print("⚙️ Treinando modelo SVD...")

model = SVD(n_factors=50, n_epochs=20)

model.fit(trainset)

print("✅ Modelo treinado com sucesso!")

# ===============================
# 5. Salvar o modelo treinado
# ===============================

os.makedirs("app/model_artifacts", exist_ok=True)

with open("app/model_artifacts/svd_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("💾 Modelo salvo em: app/model_artifacts/svd_model.pkl")
