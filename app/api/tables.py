"""
Charts API
"""

import pandas as pd
from fastapi import APIRouter

from app.api.constants import MULTI_TIME_SERIES_TABLE_PATH
from app.config import ConfigManager
from app.logger import logger
from app.models.table import TableData
from app.queries.time_series import get_mock_daily_time_series_data
from app.schemas.tables import MultiTimeSeriesTableRequest, MultiTimeSeriesTableResponse

router = APIRouter()


@router.post(MULTI_TIME_SERIES_TABLE_PATH)
async def multi_time_series_table(request: MultiTimeSeriesTableRequest) -> MultiTimeSeriesTableResponse:
    """
    Get a multi lines chart
    """
    logger.info(f"Getting multi time series table for {request.data_identifiers} from {request.start_date} to {request.end_date}")

    data_identifiers = request.data_identifiers
    start_date = request.start_date
    end_date = request.end_date

    all_dfs: list[pd.DataFrame] = []
    for identifier in data_identifiers:
        df = get_mock_daily_time_series_data(identifier, start_date, end_date)
        df = df.rename(columns={"value": identifier})
        all_dfs.append(df)

    # INSERT_YOUR_CODE
    merged_df = all_dfs[0].copy() if all_dfs else pd.DataFrame()
    for df in all_dfs[1:]:
        merged_df = merged_df.merge(df[["date", df.columns[-1]]], on="date", how="outer")
    merged_df = merged_df.sort_values("date").reset_index(drop=True)
    data = TableData(
        number_of_rows=len(merged_df),
        columns=list(merged_df.columns),
        rows=merged_df.to_dict(orient="records"),  # type: ignore
    )

    config = ConfigManager().get_config()
    logger.info(str(config))

    return MultiTimeSeriesTableResponse(data=data, start_date=request.start_date, end_date=request.end_date)
