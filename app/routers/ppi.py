from fastapi import APIRouter, Depends, Query as FastapiQuery
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models import PPIData
from app.schemas import PPIResponse
from app.routers.utils import (
    CommonQueryParams, PaginatedResponse, query_dataset, _parse_filter_value
)

router = APIRouter()


class PPIDatasetParams:
    """PPI-specific query parameters."""

    def __init__(
        self,
        sector_code: Optional[str] = FastapiQuery(
            None, description="Filter by sector_code (comma-separated for OR)"
        ),
        class_code: Optional[str] = FastapiQuery(
            None, description="Filter by class_code (comma-separated for OR)"
        ),
        measure_code: Optional[str] = FastapiQuery(
            None, description="Filter by measure_code (comma-separated for OR)"
        ),
        seasonal_code: Optional[str] = FastapiQuery(
            None, description="Filter by seasonal_code (comma-separated for OR)"
        ),
        duration_code: Optional[str] = FastapiQuery(
            None, description="Filter by duration_code (comma-separated for OR)"
        ),
    ):
        self.sector_code = sector_code
        self.class_code = class_code
        self.measure_code = measure_code
        self.seasonal_code = seasonal_code
        self.duration_code = duration_code

    def build_filters(self) -> dict:
        filters = {}
        if self.sector_code:
            filters["sector_code"] = _parse_filter_value(self.sector_code)
        if self.class_code:
            filters["class_code"] = _parse_filter_value(self.class_code)
        if self.measure_code:
            filters["measure_code"] = _parse_filter_value(self.measure_code)
        if self.seasonal_code:
            filters["seasonal_code"] = _parse_filter_value(self.seasonal_code)
        if self.duration_code:
            filters["duration_code"] = _parse_filter_value(self.duration_code)
        return filters


@router.get("", response_model=PaginatedResponse[PPIResponse])
def get_ppi_data(
    common: CommonQueryParams = Depends(),
    dataset: PPIDatasetParams = Depends(),
    db: Session = Depends(get_db),
):
    return query_dataset(common, dataset.build_filters(), db, PPIData)
