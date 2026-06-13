import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

from sklearn.metrics import (
    mean_absolute_error,
    root_mean_squared_error
)


def train_model(
    df,
    model_name
):

    X = np.arange(
        len(df)
    ).reshape(
        -1,
        1
    )

    y = df["price"]

    if model_name == "Linear Regression":

        model = LinearRegression()

    else:

        model = RandomForestRegressor(

            n_estimators=100,

            random_state=42

        )

    model.fit(
        X,
        y
    )

    pred = model.predict(
        X
    )

    mae = mean_absolute_error(
        y,
        pred
    )

    rmse = root_mean_squared_error(
        y,
        pred
    )

    return (

        model,

        pred,

        mae,

        rmse,

        X,

        y

    )
