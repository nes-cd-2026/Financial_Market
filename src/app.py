import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql://user:password@db:5432/finance")

st.title("📈 Mercado Financeiro Simplificado")

# carregar dados
query = """
SELECT a.name, p.date, p.price
FROM prices p
JOIN assets a ON p.asset_id = a.id
"""

df = pd.read_sql(query, engine)

# seletor de ativo
assets = df["name"].unique()
asset = st.selectbox("Escolha o ativo", assets)

df_asset = df[df["name"] == asset].sort_values("date")

# gráfico preço
st.subheader("Preço ao longo do tempo")
st.line_chart(df_asset.set_index("date")["price"])

# retorno diário
df_asset["return"] = df_asset["price"].pct_change()

st.subheader("Retorno diário")
st.line_chart(df_asset.set_index("date")["return"])

# volatilidade
vol = df_asset["return"].std()
st.metric("Volatilidade", f"{vol:.4f}")

# correlação entre ativos
pivot = df.pivot(index="date", columns="name", values="price")
corr = pivot.pct_change().corr()

st.subheader("Correlação entre ativos")
st.dataframe(corr)
