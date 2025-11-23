import datetime as dt
import os

import pandas as pd

from app.models.time_series import DailyTimeSeriesData


def get_mock_daily_time_series_data(data_identifier: str, start_date: dt.date, end_date: dt.date) -> list[DailyTimeSeriesData]:
    """
    Get mock daily time series data
    """
    data: list[DailyTimeSeriesData] = []

    mock_data_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), "mock_data")
    file_path = os.path.join(mock_data_folder, f"{data_identifier}.csv")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Mock data file not found: {file_path}")

    df = pd.read_csv(file_path)
    df["date"] = pd.to_datetime(df["date"]).dt.date
    df = df[df["date"] >= start_date]
    df = df[df["date"] <= end_date]
    df = df.sort_values(by="date")
    return [DailyTimeSeriesData(**record) for record in df.to_dict(orient="records")]  # type: ignore
