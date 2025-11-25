from typing import Any

from pydantic import BaseModel


class TableData(BaseModel):
    """
    Data schema for the daily time series data
    """
    number_of_rows: int
    columns: list[str]
    # each row  has format {"column1": "value1", "column2": "value2"}
    rows: list[dict[str, Any]]
