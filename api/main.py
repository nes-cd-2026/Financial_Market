from fastapi import FastAPI
from sqlalchemy import create_engine
import pandas as pd

app = FastAPI()

engine = create_engine(
    "postgresql://user:password@db:5432/finance"
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/dados")
def dados(

    ativo: str,

    inicio: str = None,

    fim: str = None

):

    query = f"""
    SELECT
        a.name,
        p.date,
        p.price
    FROM prices p
    JOIN assets a
      ON p.asset_id = a.id
    WHERE a.name='{ativo}'
    """

    if inicio:

        query += f"""
        AND p.date >= '{inicio}'
        """

    if fim:

        query += f"""
        AND p.date <= '{fim}'
        """

    query += """

    ORDER BY p.date

    """

    df = pd.read_sql(
        query,
        engine
    )

    return (
        df
        .to_dict(
            orient="records"
        )
    )

@app.get("/resumo")
def resumo(ativo: str):

    query = f"""
    SELECT p.price
    FROM prices p
    JOIN assets a
      ON p.asset_id = a.id
    WHERE a.name = '{ativo}'
    """

    df = pd.read_sql(query, engine)

    return {
        "media": float(df.price.mean()),
        "minimo": float(df.price.min()),
        "maximo": float(df.price.max())
    }
