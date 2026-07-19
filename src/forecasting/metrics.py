from dataclasses import dataclass


@dataclass
class ForecastResult:

    company_id: str

    metric: str

    forecast_year: int

    predicted_value: float