from fastapi import APIRouter, Depends, Query as FastapiQuery
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models import LAData
from app.schemas import LAResponse
from app.routers.utils import (
    CommonQueryParams, PaginatedResponse, query_dataset, _parse_filter_value
)

router = APIRouter()


class LADatasetParams:
    """LA-specific query parameters."""

    def __init__(
        self,
        state_code: Optional[str] = FastapiQuery(
            None, description="Filter by state_code (comma-separated for OR)"
        ),
        area_code: Optional[str] = FastapiQuery(
            None, description="Filter by area_code (comma-separated for OR)"
        ),
        measure_code: Optional[str] = FastapiQuery(
            None, description="Filter by measure_code (comma-separated for OR)"
        ),
        seasonal_code: Optional[str] = FastapiQuery(
            None, description="Filter by seasonal_code (comma-separated for OR)"
        ),
        area_type_code: Optional[str] = FastapiQuery(
            None, description="Filter by area_type_code (comma-separated for OR)"
        ),
    ):
        self.state_code = state_code
        self.area_code = area_code
        self.measure_code = measure_code
        self.seasonal_code = seasonal_code
        self.area_type_code = area_type_code

    def build_filters(self) -> dict:
        filters = {}
        if self.state_code:
            filters["state_code"] = _parse_filter_value(self.state_code)
        if self.area_code:
            filters["area_code"] = _parse_filter_value(self.area_code)
        if self.measure_code:
            filters["measure_code"] = _parse_filter_value(self.measure_code)
        if self.seasonal_code:
            filters["seasonal_code"] = _parse_filter_value(self.seasonal_code)
        if self.area_type_code:
            filters["area_type_code"] = _parse_filter_value(self.area_type_code)
        return filters


@router.get("", response_model=PaginatedResponse[LAResponse])
def get_la_data(
    common: CommonQueryParams = Depends(),
    dataset: LADatasetParams = Depends(),
    db: Session = Depends(get_db),
):
    return query_dataset(common, dataset.build_filters(), db, LAData)
