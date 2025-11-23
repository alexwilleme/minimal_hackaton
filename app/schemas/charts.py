import datetime as dt
from typing import List

from pydantic import BaseModel, field_validator

from app.models.time_series import DailyTimeSeriesData


class MultiLinesChartRequest(BaseModel):
    """
    Request schema for the multi lines chart endpoint
    """
    data_identifiers: List[str]
    start_date: dt.date
    end_date: dt.date

    @field_validator('data_identifiers')
    @classmethod
    def data_identifiers_must_be_unique(cls, v):
        if len(v) != len(set(v)):
            raise ValueError("data_identifiers must contain unique values")
        return v


class MultiLinesChartResponse(BaseModel):
    """
    Response schema for the multi lines chart endpoint
    """
    data: dict[str, List[DailyTimeSeriesData]]
    start_date: dt.date
    end_date: dt.date
