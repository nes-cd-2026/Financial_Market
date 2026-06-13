import pandas as pd
import numpy as np

from sqlalchemy import (
    create_engine,
    text
)

import time

time.sleep(10)

engine = create_engine(
    "postgresql://user:password@db:5432/finance"
)

with engine.connect() as conn:

    conn.execute(text("""

    CREATE TABLE IF NOT EXISTS assets(

        id SERIAL PRIMARY KEY,

        name TEXT

    )

    """))

    conn.execute(text("""

    CREATE TABLE IF NOT EXISTS prices(

        id SERIAL PRIMARY KEY,

        asset_id INT,

        date DATE,

        price FLOAT

    )

    """))

    conn.commit()

assets = pd.DataFrame({

"id":[1,2,3],

"name":[
"AAPL",
"GOOGL",
"TSLA"
]

})
assets.to_sql(
"assets",
engine,
if_exists="replace",
index=False
)

dates = pd.date_range(
"2023-01-01",
"2023-12-31"
)

rows=[]

np.random.seed(42)

for asset_id in [1,2,3]:

    price=100

    for d in dates:

        price*=np.random.normal(
            1.0005,
            0.02
        )

        rows.append([

            asset_id,
            d,
            round(price,2)

        ])

prices=pd.DataFrame(

rows,

columns=[

"asset_id",
"date",
"price"

]

)

prices.to_sql(

"prices",

engine,

if_exists="replace",

index=False

)

print("dados criados")
