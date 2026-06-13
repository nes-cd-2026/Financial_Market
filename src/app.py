import streamlit as st
import requests
import pandas as pd
import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from model.predictor import train_model
from model.predictor import train_model

st.title("Mercado Financeiro Preditivo")

ativo = st.selectbox(
    "Ativo",
    ["AAPL","GOOGL","TSLA"]
)

modelo = st.selectbox(
    "Modelo",
    [
        "Linear Regression",
        "Random Forest"
    ]
)

response = requests.get(
    f"http://api:8000/dados?ativo={ativo}"
)

if response.status_code != 200:

    st.error(response.text)

    st.stop()

dados = response.json()

df = pd.DataFrame(dados)
df = pd.DataFrame(dados)

df["date"] = pd.to_datetime(df["date"])

st.subheader("Série Histórica")

st.line_chart(
    df.set_index("date")["price"]
)

model,pred,mae,rmse,X_test,y_test = train_model(
    df,
    modelo
)

resultado = pd.DataFrame({
    "Real": y_test.values,
    "Previsto": pred
})

st.subheader("Previsão")

st.line_chart(resultado)

st.metric(
    "MAE",
    round(mae,2)
)

st.metric(
    "RMSE",
    round(rmse,2)
)

resumo = requests.get(
    f"http://api:8000/resumo?ativo={ativo}"
).json()

st.subheader("Resumo")

st.json(resumo)
