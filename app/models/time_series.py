import datetime as dt
from pydantic import BaseModel


class DailyTimeSeriesData(BaseModel):
    """
    Data schema for the daily time series data
    """
    date: dt.date
    value: float
