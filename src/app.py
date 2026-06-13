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

import streamlit as st
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from model.predictor import train_model


st.set_page_config(
    page_title="Mercado Financeiro",
    layout="wide"
)

st.title(
    "📈 Mercado Financeiro — Previsão de Ativos"
)

# ESCOLHAS

ativo = st.selectbox(

    "Variável a prever",

    [
        "AAPL",
        "GOOGL",
        "TSLA"
    ]

)

modelo = st.selectbox(

    "Modelo",

    [

        "Linear Regression",

        "Random Forest"

    ]

)

# API
response = requests.get(

    "http://api:8000/dados",

    params={

        "ativo": ativo

    }

)

if response.status_code != 200:

    st.error(
        response.text
    )

    st.stop()

dados = response.json()

df = pd.DataFrame(
    dados
)

df["date"] = pd.to_datetime(
    df["date"]
)

# FILTRO PERÍODO
data_min = df["date"].min().date()

data_max = df["date"].max().date()

inicio = st.date_input(

    "Data inicial",

    value=data_min,

    min_value=data_min,

    max_value=data_max

)

fim = st.date_input(

    "Data final",

    value=data_max,

    min_value=inicio,

    max_value=data_max

)
# SEGUNDA CONSULTA

response = requests.get(

    "http://api:8000/dados",

    params={

        "ativo": ativo,

        "inicio": inicio.isoformat(),

        "fim": fim.isoformat()

    }

)

if response.status_code != 200:

    st.error(
        response.text
    )

    st.stop()

dados = response.json()

df = pd.DataFrame(
    dados
)

df["date"] = pd.to_datetime(
    df["date"]
)

df = df.sort_values(
    "date"
)

# CORTE TEMPORAL

st.subheader(
    "Configuração da Previsão"
)

min_t0 = 1

max_t0 = max(
    1,
    len(df)-5
)

valor_padrao = min(
    int(len(df)*0.8),
    max_t0
)

t0 = st.slider(

    "Corte temporal (t0)",

    min_value=min_t0,

    max_value=max_t0,

    value=valor_padrao

)

# HORIZONTE

max_horizonte = max(
    1,
    len(df)-t0
)

horizonte = st.slider(

    "Horizonte de previsão",

    min_value=1,

    max_value=max_horizonte,

    value=min(
        30,
        max_horizonte
    )

)

if len(df) > 1:

    st.info(

        f"""
Treino:
{df.iloc[0]["date"].date()}
→
{df.iloc[min(t0, len(df)-1)]["date"].date()}

Previsão:
{horizonte} dias
"""

    )
    
# DIVISÃO

train = df.iloc[:t0]

test = df.iloc[
    t0:
    t0+horizonte
]

# MODELO


model,_,mae,rmse,_,_ = train_model(

    train,

    modelo

)

future = np.arange(

    len(train),

    len(train)+len(test)

).reshape(
    -1,
    1
)

pred = model.predict(
    future
)

# INTERVALO CONFIANÇA

desvio = np.std(
    pred
)

inferior = pred-desvio

superior = pred+desvio

# PLOT

st.subheader(
    "Série Temporal"
)

fig = plt.figure(
    figsize=(14,7)
)

plt.plot(

    df["date"],

    df["price"],

    label="Preço Real"

)

plt.plot(

    test["date"],

    pred,

    "--",

    linewidth=3,

    label="Previsão"

)

plt.fill_between(

    test["date"],

    inferior,

    superior,

    alpha=0.2

)

plt.axvline(

    df.iloc[t0]["date"],

    linestyle=":",

    linewidth=2

)

plt.xlabel(
    "Data"
)

plt.ylabel(
    "Preço"
)

plt.legend()

st.pyplot(
    fig
)

# MÉTRICAS

c1,c2 = st.columns(
    2
)

with c1:

    st.metric(

        "MAE",

        round(
            mae,
            2
        )

    )

with c2:

    st.metric(

        "RMSE",

        round(
            rmse,
            2
        )

    )

# -----------------------
# RESUMO
# -----------------------

resumo = requests.get(

    f"http://api:8000/resumo?ativo={ativo}"

).json()

st.subheader(
    "Resumo Estatístico"
)

st.json(
    resumo
)
