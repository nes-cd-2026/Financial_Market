# Projeto — Previsão de Mercado Financeiro

## Tema

Tema 5 — Mercado Financeiro

## Objetivo

Desenvolver uma aplicação para análise e previsão de séries temporais financeiras utilizando arquitetura baseada em microsserviços com Docker.

A aplicação permite:

* visualizar séries históricas;
* selecionar ativo financeiro;
* definir período de análise;
* definir horizonte de previsão;
* definir corte temporal (t0);
* comparar previsão e valores reais;
* executar toda a solução por contêineres.

---

# Tecnologias Utilizadas

* Python
* Streamlit
* FastAPI
* PostgreSQL
* Pandas
* Scikit-Learn
* SQLAlchemy
* Docker
* Docker Compose

---

# Estrutura do Projeto

```text
Financial_market-main/

├── api/
│   └── main.py

├── src/
│   ├── app.py
│   └── model/

├── Dockerfile.api
├── Dockerfile.dashboard
├── docker-compose.yml
├── requirements.txt
├── README.md
└── slides_apresentacao.pdf.7z
```

---

# Como Executar

Pré-requisito:

Instalar Docker Desktop.

Executar:

```bash
docker compose up --build
```

---

# Acessos

Dashboard:

http://localhost:8501

Documentação da API:

http://localhost:8000/docs

API:

http://localhost:8000

---

# Rotas da API

## GET /health

Verifica se a API está ativa.

Exemplo:

```text
http://localhost:8000/health
```

Resposta:

```json
{
  "status": "ok"
}
```

---

## GET /dados

Retorna dados históricos filtrados.

Parâmetros:

| Nome   | Tipo            |
| ------ | --------------- |
| ativo  | string          |
| inicio | data (opcional) |
| fim    | data (opcional) |

Exemplo:

```text
http://localhost:8000/dados?ativo=AAPL
```

Exemplo com período:

```text
http://localhost:8000/dados?ativo=AAPL&inicio=2023-01-01&fim=2023-06-01
```

---

## GET /resumo

Retorna estatísticas descritivas.

Parâmetros:

| Nome  | Tipo   |
| ----- | ------ |
| ativo | string |

Exemplo:

```text
http://localhost:8000/resumo?ativo=AAPL
```

---

# Requisitos da AV2 Atendidos

## Dashboard

✔ Seleção da variável (ativo)

✔ Seleção do horizonte de previsão

✔ Definição do corte temporal (t0)

✔ Comparação previsão × série real

✔ Visualização da previsão sobreposta

✔ Filtro temporal

---

## Modelo

✔ Motivação

✔ Pré-processamento

✔ Hiperparâmetros

✔ Métricas

✔ Limitações

---

## Infraestrutura

✔ API documentada

✔ Docker Compose

✔ Execução automatizada

✔ Ambiente reproduzível

---

# Observações

Os slides foram compactados em arquivo `.7z` devido ao limite de upload.

Para visualizar:

1. Baixar o arquivo;
2. Extrair;
3. Abrir o PDF.
