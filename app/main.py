import os
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

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
        raise HTTPException(status_code=500, detail="Conexão com o banco de dados falhou na inicialização.")

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
        raise HTTPException(status_code=500, detail=f"Erro ao consultar o banco de dados: {str(e)}")