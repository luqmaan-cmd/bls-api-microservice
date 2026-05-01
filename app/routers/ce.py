from fastapi import APIRouter, Depends, Query as FastapiQuery
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models import CEData
from app.schemas import CEResponse
from app.routers.utils import (
    CommonQueryParams, PaginatedResponse, query_dataset, _parse_filter_value
)

router = APIRouter()


class CEDatasetParams:
    """CE-specific query parameters."""

    def __init__(
        self,
        industry_code: Optional[str] = FastapiQuery(
            None, description="Filter by industry_code (comma-separated for OR)"
        ),
        supersector_code: Optional[str] = FastapiQuery(
            None, description="Filter by supersector_code (comma-separated for OR)"
        ),
        datatype_code: Optional[str] = FastapiQuery(
            None, description="Filter by datatype_code (comma-separated for OR)"
        ),
        seasonal_code: Optional[str] = FastapiQuery(
            None, description="Filter by seasonal_code (comma-separated for OR)"
        ),
    ):
        self.industry_code = industry_code
        self.supersector_code = supersector_code
        self.datatype_code = datatype_code
        self.seasonal_code = seasonal_code

    def build_filters(self) -> dict:
        filters = {}
        if self.industry_code:
            filters["industry_code"] = _parse_filter_value(self.industry_code)
        if self.supersector_code:
            filters["supersector_code"] = _parse_filter_value(self.supersector_code)
        if self.datatype_code:
            filters["datatype_code"] = _parse_filter_value(self.datatype_code)
        if self.seasonal_code:
            filters["seasonal_code"] = _parse_filter_value(self.seasonal_code)
        return filters


@router.get("", response_model=PaginatedResponse[CEResponse])
def get_ce_data(
    common: CommonQueryParams = Depends(),
    dataset: CEDatasetParams = Depends(),
    db: Session = Depends(get_db),
):
    return query_dataset(common, dataset.build_filters(), db, CEData)
