import streamlit as st
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
import time

# conexão
engine = create_engine(
    "postgresql://user:password@db:5432/finance"
)

# esperar banco iniciar
time.sleep(5)

# criar tabelas
with engine.connect() as conn:

    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS assets (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL
        );
    """))

    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS prices (
            id SERIAL PRIMARY KEY,
            asset_id INT REFERENCES assets(id),
            date DATE NOT NULL,
            price FLOAT NOT NULL
        );
    """))

    conn.commit()

# verificar se já existem dados
check_query = """
SELECT COUNT(*) FROM assets
"""

with engine.connect() as conn:
    result = conn.execute(text(check_query))
    count = result.scalar()

# gerar dados automaticamente se vazio
if count == 0:

    np.random.seed(42)

    assets = ["AAPL", "GOOGL", "TSLA"]

    assets_df = pd.DataFrame({
        "name": assets
    })

    dates = pd.date_range("2023-01-01", "2023-12-31")

    price_data = []

    for i, asset in enumerate(assets, start=1):

        price = 100

        for date in dates:

            price *= np.random.normal(1.0005, 0.02)

            price_data.append([
                i,
                date,
                round(price, 2)
            ])

    prices_df = pd.DataFrame(
        price_data,
        columns=["asset_id", "date", "price"]
    )

    assets_df.to_sql(
        "assets",
        engine,
        if_exists="append",
        index=False
    )

    prices_df.to_sql(
        "prices",
        engine,
        if_exists="append",
        index=False
    )

# dashboard
st.title("📈 Mercado Financeiro Simplificado")

query = """
SELECT a.name, p.date, p.price
FROM prices p
JOIN assets a ON p.asset_id = a.id
"""

df = pd.read_sql(query, engine)

assets = df["name"].unique()

asset = st.selectbox(
    "Escolha o ativo",
    assets
)

df_asset = df[df["name"] == asset].sort_values("date")

st.subheader("Preço ao longo do tempo")

st.line_chart(
    df_asset.set_index("date")["price"]
)

df_asset["return"] = df_asset["price"].pct_change()

st.subheader("Retorno diário")

st.line_chart(
    df_asset.set_index("date")["return"]
)

vol = df_asset["return"].std()

st.metric(
    "Volatilidade",
    f"{vol:.4f}"
)

pivot = df.pivot(
    index="date",
    columns="name",
    values="price"
)

corr = pivot.pct_change().corr()

st.subheader("Correlação entre ativos")

st.dataframe(corr)
