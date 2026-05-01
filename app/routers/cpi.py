from fastapi import APIRouter, Depends, Query as FastapiQuery
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models import CPIData
from app.schemas import CPIResponse
from app.routers.utils import (
    CommonQueryParams, PaginatedResponse, query_dataset, _parse_filter_value
)

router = APIRouter()


class CPIDatasetParams:
    """CPI-specific query parameters."""

    def __init__(
        self,
        area_code: Optional[str] = FastapiQuery(
            None, description="Filter by area_code (comma-separated for OR)"
        ),
        item_code: Optional[str] = FastapiQuery(
            None, description="Filter by item_code (comma-separated for OR)"
        ),
        seasonal_code: Optional[str] = FastapiQuery(
            None, description="Filter by seasonal_code (comma-separated for OR)"
        ),
    ):
        self.area_code = area_code
        self.item_code = item_code
        self.seasonal_code = seasonal_code

    def build_filters(self) -> dict:
        filters = {}
        if self.area_code:
            filters["area_code"] = _parse_filter_value(self.area_code)
        if self.item_code:
            filters["item_code"] = _parse_filter_value(self.item_code)
        if self.seasonal_code:
            filters["seasonal_code"] = _parse_filter_value(self.seasonal_code)
        return filters


@router.get("", response_model=PaginatedResponse[CPIResponse])
def get_cpi_data(
    common: CommonQueryParams = Depends(),
    dataset: CPIDatasetParams = Depends(),
    db: Session = Depends(get_db),
):
    return query_dataset(common, dataset.build_filters(), db, CPIData)
