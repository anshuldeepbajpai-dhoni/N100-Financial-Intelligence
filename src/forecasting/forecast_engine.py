import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from .model_selector import ForecastModelSelector
from .preprocess import ForecastPreprocessor
from .evaluation import ForecastEvaluator

class ForecastEngine:

    def __init__(self, years_to_predict=3):

        self.years_to_predict = years_to_predict

    def forecast_company(
        self,
        df,
        company,
        metric,
    ):

        company_df = df[
            df["company_id"] == company
        ]

        if len(company_df) < 3:
            return []

        X = company_df["year"].values.reshape(-1, 1)

        y = company_df[metric].values


        model_name, model, scores = (

            ForecastModelSelector.best_model(
                X,
                y,
            )

        )

        print(

            f"{company} | "

            f"{metric} | "

            f"{model_name} | "

            f"RMSE={scores['RMSE']}"

        )

        # Evaluate model on historical data
        predicted = model.predict(X)



        scores = ForecastEvaluator.evaluate(
            y,
            predicted,
        )

        print(
            f"{company} | {metric} | "
            f"MAE={scores['MAE']} | "
            f"RMSE={scores['RMSE']}"
        )

        last_year = int(company_df["year"].max())

        future = [
            last_year + i
            for i in range(
                1,
                self.years_to_predict + 1,
            )
        ]

        if model_name == "Linear Regression":

            predictions = model.predict(
                np.array(future).reshape(-1, 1)
            )

        else:

            predictions = model.forecast(
                self.years_to_predict
            )

        rows = []

        for yr, value in zip(
            future,
            predictions,
        ):

            rows.append(
                {
                    "company_id": company,
                    "metric": metric,
                    "forecast_year": yr,
                    "predicted_value": round(
                        float(value),
                        2,
                    ),
                }
            )

        return rows

    def forecast(
        self,
        dataframe,
        metric,
    ):

        data = ForecastPreprocessor.prepare(
            dataframe,
            metric,
        )

        forecasts = []

        for company in sorted(
            data["company_id"].unique()
        ):

            forecasts.extend(

                self.forecast_company(

                    data,

                    company,

                    metric,

                )

            )

        return pd.DataFrame(
            forecasts
        )
    
    def forecast_multiple(
        self,
        dataframe,
        metrics,
    ):
        """
        Forecast multiple financial metrics.

        Parameters
        ----------
        dataframe : DataFrame
        metrics : list

        Returns
        -------
        dict
            {
                metric_name: forecast_dataframe
            }
        """

        results = {}

        for metric in metrics:

            try:

                results[metric] = self.forecast(
                    dataframe,
                    metric,
                )

            except Exception as e:

                print(f"Skipping {metric}: {e}")

        return results