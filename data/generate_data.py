import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy import text
import time

# esperar o banco iniciar
time.sleep(10)

engine = create_engine(
    "postgresql://user:password@db:5432/finance"
)

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

# remover dados antigos
with engine.connect() as conn:
    conn.execute(text("DELETE FROM prices"))
    conn.execute(text("DELETE FROM assets"))
    conn.commit()

# gerar dados
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

# inserir dados
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

print("Dados gerados com sucesso!")
