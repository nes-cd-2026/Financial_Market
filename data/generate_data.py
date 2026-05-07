import pandas as pd
import numpy as np
from sqlalchemy import create_engine

engine = create_engine("postgresql://user:password@db:5432/finance")

np.random.seed(42)

assets = ["AAPL", "GOOGL", "TSLA"]

assets_df = pd.DataFrame({"name": assets})

dates = pd.date_range("2023-01-01", "2023-12-31")

price_data = []

for i, asset in enumerate(assets, start=1):
    price = 100

    for date in dates:
        price *= np.random.normal(1.0005, 0.02)  # random walk
        price_data.append([i, date, price])

prices_df = pd.DataFrame(price_data, columns=["asset_id", "date", "price"])

assets_df.to_sql("assets", engine, if_exists="replace", index=False)
prices_df.to_sql("prices", engine, if_exists="replace", index=False)

print("Dados gerados com sucesso!")
