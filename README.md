# Sistema de Recomendação de Livros

### Integrantes
- Felipe Teodoro Bandeira
- Eduardo Galvão de Aquino Cavalheiro
- João Victor ferreira marques

Este repositório contém a implementação de um sistema de recomendação de livros baseado em filtragem colaborativa. O projeto foi desenvolvido como parte da disciplina de Desenvolvimento de Inteligência Artificial, utilizando FastAPI para a interface de aplicação, Docker para containerização e PostgreSQL (Neon) para persistência de dados.

## Visão Geral do Projeto

O sistema foi projetado para processar o dataset *Book-Crossings*, armazenar as informações em um banco de dados relacional na nuvem e disponibilizar recomendações personalizadas através de uma API RESTful. A arquitetura prioriza a escalabilidade e a reprodutibilidade do ambiente.

### Objetivos
* Implementar um fluxo de Engenharia de Machine Learning (ML Engineering).
* Desenvolver uma API performática para servir o modelo.
* Utilizar containerização para padronização do ambiente de desenvolvimento e produção.
* Integrar a aplicação com banco de dados em nuvem.

## Stack Tecnológica

* **Linguagem:** Python 3.11
* **Framework Web:** FastAPI
* **Servidor:** Uvicorn
* **Containerização:** Docker e Docker Compose
* **Banco de Dados:** PostgreSQL (Serverless via Neon Tech)
* **Machine Learning:** Scikit-Learn (TruncatedSVD), Pandas, NumPy
* **Gerenciamento de Dependências:** Pip

## Arquitetura e Decisões de Design

### 1. Modelo de Recomendação (SVD)
Utilizou-se a técnica de Fatoração de Matriz via *Singular Value Decomposition* (SVD).
* **Estratégia de Inferência:** Devido ao custo computacional de calcular decomposições de matrizes grandes em tempo real, adotou-se uma abordagem de **treinamento offline**. Um script dedicado processa os dados, gera os vetores latentes de usuários e itens, e serializa o modelo (`.pkl`). A API carrega esses artefatos na inicialização, garantindo baixa latência nas requisições.

### 2. Banco de Dados (Neon PostgreSQL)
A escolha pelo Neon (PostgreSQL serverless) permite desacoplar a camada de persistência da aplicação containerizada, simulando um ambiente de produção real e evitando a perda de dados ao reiniciar os containers.

### 3. Estrutura de Pastas
* `/app`: Contém o código-fonte da API (`main.py`) e os artefatos do modelo (`model_artifacts/`).
* `/scripts`: Scripts de ETL (`load_data_to_neon.py`) e treinamento (`train_model.py`).
* `/data`: Diretório local para armazenamento temporário dos datasets brutos (não versionado).
* `/tests`: Diretório para realização de testes unitários.
* `Dockerfile` e `docker-compose.yml`: Configurações de infraestrutura.

## Guia de Instalação e Execução

### Pré-requisitos
* Docker e Docker Desktop instalados.
* Git instalado.
* Conta e projeto configurado no Neon (ou instância PostgreSQL compatível).

### 1. Clonagem do Repositório

```bash
git clone https://github.com/Felipe-teodoro05/recomendation-system.git
cd recomendation-system
```

### 2. Configuração de Variáveis de Ambiente
É necessário criar um arquivo .env na raiz do projeto para configurar a conexão com o banco de dados. Este arquivo não é versionado por questões de segurança.

Crie o arquivo .env com o seguinte conteúdo:
```
DATABASE_URL="postgres://usuario:senha@host-do-neon/nome-do-banco?sslmode=require"
```
### 3. Preparação do Banco de Dados e Modelo
Antes de iniciar a API, é necessário popular o banco de dados e treinar o modelo inicial. Recomenda-se executar estes scripts localmente em um ambiente virtual Python.

```Bash

# Criação do ambiente virtual (Linux/Mac)
python3 -m venv venv
source venv/bin/activate

# Criação do ambiente virtual (Windows)
python -m venv venv
.\venv\Scripts\activate

# Instalação das dependências
pip install -r requirements.txt

# Execução do ETL (Carga de dados para o Neon)
python scripts/load_data_to_neon.py

# Treinamento do Modelo (Geração dos arquivos .pkl)
python scripts/train_model.py
```
### 4. Execução da Aplicação com Docker
Com o banco populado e os artefatos gerados na pasta app/model_artifacts, inicie o serviço via Docker Compose:

```
docker-compose up --build
O terminal exibirá os logs de inicialização. Aguarde a mensagem indicando que o servidor Uvicorn está rodando.

Utilização da API
A documentação interativa (Swagger UI) pode ser acessada em:

URL: http://localhost:8000/docs

Principais Endpoints
GET /: Verificação de status da API.

GET /test-db: Teste de conectividade com o banco de dados PostgreSQL.

GET /recommendations/{user_id}: Retorna a lista de livros recomendados para o ID informado.

Exemplo: /recommendations/276747

POST /preferences/: Registra novas interações de usuários (simulação).
```

### Testes
O projeto conta com testes automatizados para validar a integridade dos endpoints e da conexão com o banco.

```
/tests
```

