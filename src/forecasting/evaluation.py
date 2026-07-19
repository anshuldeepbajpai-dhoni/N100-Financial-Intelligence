from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
import numpy as np


class ForecastEvaluator:

    @staticmethod
    def evaluate(actual, predicted):
        """
        Evaluate forecast performance.

        Parameters
        ----------
        actual : array-like
        predicted : array-like

        Returns
        -------
        dict
        """

        mae = mean_absolute_error(actual, predicted)

        rmse = np.sqrt(
            mean_squared_error(actual, predicted)
        )

        return {
            "MAE": round(mae, 2),
            "RMSE": round(rmse, 2),
        }