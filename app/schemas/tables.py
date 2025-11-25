import datetime as dt

from pydantic import BaseModel, field_validator

from app.models.table import TableData


class MultiTimeSeriesTableRequest(BaseModel):
    """
    Request schema for the multi lines chart endpoint
    """
    data_identifiers: list[str]
    start_date: dt.date
    end_date: dt.date

    @field_validator('data_identifiers')
    @classmethod
    def data_identifiers_must_be_unique(cls, v):
        if len(v) != len(set(v)):
            raise ValueError("data_identifiers must contain unique values")
        return v


class MultiTimeSeriesTableResponse(BaseModel):
    """
    Response schema for the multi lines chart endpoint
    """
    start_date: dt.date
    end_date: dt.date
    data: TableData
