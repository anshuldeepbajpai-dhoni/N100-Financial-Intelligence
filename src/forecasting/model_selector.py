import numpy as np

from sklearn.linear_model import LinearRegression

from statsmodels.tsa.holtwinters import ExponentialSmoothing

from .evaluation import ForecastEvaluator


class ForecastModelSelector:

    @staticmethod
    def linear(X, y):

        model = LinearRegression()

        model.fit(X, y)

        pred = model.predict(X)

        score = ForecastEvaluator.evaluate(
            y,
            pred,
        )

        return model, score

    @staticmethod
    def exponential(y):

        model = ExponentialSmoothing(

            y,

            trend="add",

            seasonal=None,

        ).fit()

        pred = model.fittedvalues

        score = ForecastEvaluator.evaluate(
            y,
            pred,
        )

        return model, score

    @staticmethod
    def best_model(X, y):

        linear_model, linear_score = (

            ForecastModelSelector.linear(
                X,
                y,
            )

        )

        exp_model, exp_score = (

            ForecastModelSelector.exponential(
                y
            )

        )

        if linear_score["RMSE"] <= exp_score["RMSE"]:

            return (

                "Linear Regression",

                linear_model,

                linear_score,

            )

        return (

            "Exponential Smoothing",

            exp_model,

            exp_score,

        )