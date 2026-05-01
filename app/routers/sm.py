from fastapi import APIRouter, Depends, Query as FastapiQuery
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models import SMData
from app.schemas import SMResponse
from app.routers.utils import (
    CommonQueryParams, PaginatedResponse, query_dataset, _parse_filter_value
)

router = APIRouter()


class SMDatasetParams:
    """SM-specific query parameters."""

    def __init__(
        self,
        state_code: Optional[str] = FastapiQuery(
            None, description="Filter by state_code (comma-separated for OR)"
        ),
        area_code: Optional[str] = FastapiQuery(
            None, description="Filter by area_code (comma-separated for OR)"
        ),
        industry_code: Optional[str] = FastapiQuery(
            None, description="Filter by industry_code (comma-separated for OR)"
        ),
        supersector_code: Optional[str] = FastapiQuery(
            None, description="Filter by supersector_code (comma-separated for OR)"
        ),
        data_type_code: Optional[str] = FastapiQuery(
            None, description="Filter by data_type_code (comma-separated for OR)"
        ),
        seasonal_code: Optional[str] = FastapiQuery(
            None, description="Filter by seasonal_code (comma-separated for OR)"
        ),
    ):
        self.state_code = state_code
        self.area_code = area_code
        self.industry_code = industry_code
        self.supersector_code = supersector_code
        self.data_type_code = data_type_code
        self.seasonal_code = seasonal_code

    def build_filters(self) -> dict:
        filters = {}
        if self.state_code:
            filters["state_code"] = _parse_filter_value(self.state_code)
        if self.area_code:
            filters["area_code"] = _parse_filter_value(self.area_code)
        if self.industry_code:
            filters["industry_code"] = _parse_filter_value(self.industry_code)
        if self.supersector_code:
            filters["supersector_code"] = _parse_filter_value(self.supersector_code)
        if self.data_type_code:
            filters["data_type_code"] = _parse_filter_value(self.data_type_code)
        if self.seasonal_code:
            filters["seasonal_code"] = _parse_filter_value(self.seasonal_code)
        return filters


@router.get("", response_model=PaginatedResponse[SMResponse])
def get_sm_data(
    common: CommonQueryParams = Depends(),
    dataset: SMDatasetParams = Depends(),
    db: Session = Depends(get_db),
):
    return query_dataset(common, dataset.build_filters(), db, SMData)
