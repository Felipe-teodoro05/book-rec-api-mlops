# BookMind: MLOps Recommendation Engine

[![FastAPI](https://img.shields.io/badge/API-FastAPI-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Deploy-Docker-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![PostgreSQL](https://img.shields.io/badge/DB-Neon%20Serverless-336791?style=flat&logo=postgresql&logoColor=white)](https://neon.tech/)
[![Python](https://img.shields.io/badge/Core-Python%203.11-3776AB?style=flat&logo=python&logoColor=white)]()

## Project Overview

O **BookMind** é um microserviço de alta performance projetado para entregar recomendações personalizadas de livros em tempo real. A arquitetura foi construída seguindo princípios de **ML Engineering**, garantindo escalabilidade via Docker e persistência de dados em nuvem (Neon Serverless Postgres).

Ao contrário de scripts simples de ML, este projeto foca no ciclo completo de vida do modelo (MLOps): desde a engenharia de dados (ETL) até a exposição da inferência via API RESTful.

---

## Architecture & MLOps Strategy

O sistema adota uma estratégia híbrida de **Offline Training** com **Online Inference** para garantir baixa latência.

```mermaid
graph LR
    subgraph "Data Engineering Layer"
        A["Raw Dataset"] -->|ETL Script| B[("Neon Postgres Cloud")]
    end

    subgraph "Training Pipeline (Offline)"
        B -->|Fetch Data| C["Training Script"]
        C -->|SVD Algorithm| D["Model Artifacts (.pkl)"]
    end

    subgraph "Serving Layer (Online)"
        D -->|Load on Startup| E["FastAPI Container"]
        U["User Request"] -->|GET /recommend| E
        E -->|JSON Response| U
    end
```

### Decisões Técnicas de Design

- **Modelo SVD (Singular Value Decomposition):** escolhido pela eficiência em filtragem colaborativa. O treinamento é desacoplado da API, gerando artefatos serializados para inferência rápida.
- **Database Serverless (Neon):** desacoplamento da camada de dados. Permite que a API em Docker seja reiniciada sem perda de estado, simulando um ambiente de produção cloud-native.
- **Containerização:** o ambiente é padronizado via `docker-compose`, eliminando problemas de “works on my machine”.

### Tech Stack

| Componente | Tecnologia | Função |
|---|---|---|
| API Framework | FastAPI | Interface REST assíncrona de alta velocidade |
| Server | Uvicorn | Servidor ASGI para produção |
| Container | Docker & Compose | Orquestração do ambiente |
| Database | PostgreSQL (Neon) | Armazenamento persistente na nuvem |
| ML Core | Scikit-Learn | Implementação do algoritmo `TruncatedSVD` |

## Installation & Setup

### Pré-requisitos
- Docker Desktop instalado.
- Conta no Neon Tech (ou qualquer Postgres externo).

### 1. Clone & Configuração

```bash
git clone https://github.com/Felipe-teodoro05/book-rec-api-mlops.git
cd book-rec-api-mlops
```
### 2. Variáveis de Ambiente
Crie um arquivo .env na raiz (não versionado) com sua string de conexão:

```text
DATABASE_URL="postgres://usuario:senha@host-do-neon/nome-do-banco?sslmode=require"
```
### 3. Pipeline de Dados (ETL & Treino)
Antes de subir a API, execute o pipeline de dados localmente para popular o banco e gerar o modelo:

```bash
# Setup do ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
pip install -r requirements.txt

# Passo 1: Carga de Dados (ETL)
python scripts/load_data_to_neon.py

# Passo 2: Treinamento do Modelo
python scripts/train_model.py
Isso criará os arquivos .pkl necessários na pasta app/model_artifacts.
```
### 4. Deploy (Docker)
```bash
docker-compose up --build
Aguarde o log: Uvicorn running on http://0.0.0.0:8000

📡 API Usage
Acesse a documentação interativa (Swagger UI) em: http://localhost:8000/docs

Exemplo de recomendação: GET /recommendations/276747

json
[
  {
    "book_title": "The Lovely Bones",
    "author": "Alice Sebold",
    "score": 0.98
  },
  {
    "book_title": "The Da Vinci Code",
    "author": "Dan Brown",
    "score": 0.95
  }
]
```
Credits & Team
Desenvolvido como projeto prático de Engenharia de IA.

Felipe Teodoro Bandeira — ML Engineering & API

Eduardo Galvão — Data Pipeline

João Victor Ferreira — Model Tuning
