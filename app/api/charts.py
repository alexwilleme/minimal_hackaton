"""
Charts API
"""

from fastapi import APIRouter

from app.api.constants import MULTI_LINES_CHART_PATH
from app.config import ConfigManager
from app.logger import logger
from app.models.time_series import DailyTimeSeriesData
from app.queries.time_series import get_mock_daily_time_series_data
from app.schemas.charts import MultiLinesChartRequest, MultiLinesChartResponse

router = APIRouter()


@router.post(MULTI_LINES_CHART_PATH)
async def multi_lines_chart(request: MultiLinesChartRequest) -> MultiLinesChartResponse:
    """
    Get a multi lines chart
    """
    logger.info(f"Getting multi lines chart for {request.data_identifiers} from {request.start_date} to {request.end_date}")

    data_identifiers = request.data_identifiers
    start_date = request.start_date
    end_date = request.end_date

    data: dict[str, list[DailyTimeSeriesData]] = {}

    for identifier in data_identifiers:
        df = get_mock_daily_time_series_data(identifier, start_date, end_date)
        data_for_id = [DailyTimeSeriesData(**record) for record in df.to_dict(orient="records")]  # type: ignore
        data |= {identifier: data_for_id}

    config = ConfigManager().get_config()
    logger.info(str(config))

    return MultiLinesChartResponse(data=data, start_date=request.start_date, end_date=request.end_date)
