from fastapi import APIRouter, Depends, Query as FastapiQuery
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models import JTData
from app.schemas import JTResponse
from app.routers.utils import (
    CommonQueryParams, PaginatedResponse, query_dataset, _parse_filter_value
)

router = APIRouter()


class JTDatasetParams:
    """JT-specific query parameters."""

    def __init__(
        self,
        state_code: Optional[str] = FastapiQuery(
            None, description="Filter by state_code (comma-separated for OR)"
        ),
        industry_code: Optional[str] = FastapiQuery(
            None, description="Filter by industry_code (comma-separated for OR)"
        ),
        area_code: Optional[str] = FastapiQuery(
            None, description="Filter by area_code (comma-separated for OR)"
        ),
        dataelement_code: Optional[str] = FastapiQuery(
            None, description="Filter by dataelement_code (comma-separated for OR)"
        ),
        seasonal_code: Optional[str] = FastapiQuery(
            None, description="Filter by seasonal_code (comma-separated for OR)"
        ),
        sizeclass_code: Optional[str] = FastapiQuery(
            None, description="Filter by sizeclass_code (comma-separated for OR)"
        ),
        ratelevel_code: Optional[str] = FastapiQuery(
            None, description="Filter by ratelevel_code (comma-separated for OR)"
        ),
    ):
        self.state_code = state_code
        self.industry_code = industry_code
        self.area_code = area_code
        self.dataelement_code = dataelement_code
        self.seasonal_code = seasonal_code
        self.sizeclass_code = sizeclass_code
        self.ratelevel_code = ratelevel_code

    def build_filters(self) -> dict:
        filters = {}
        if self.state_code:
            filters["state_code"] = _parse_filter_value(self.state_code)
        if self.industry_code:
            filters["industry_code"] = _parse_filter_value(self.industry_code)
        if self.area_code:
            filters["area_code"] = _parse_filter_value(self.area_code)
        if self.dataelement_code:
            filters["dataelement_code"] = _parse_filter_value(self.dataelement_code)
        if self.seasonal_code:
            filters["seasonal_code"] = _parse_filter_value(self.seasonal_code)
        if self.sizeclass_code:
            filters["sizeclass_code"] = _parse_filter_value(self.sizeclass_code)
        if self.ratelevel_code:
            filters["ratelevel_code"] = _parse_filter_value(self.ratelevel_code)
        return filters


@router.get("", response_model=PaginatedResponse[JTResponse])
def get_jt_data(
    common: CommonQueryParams = Depends(),
    dataset: JTDatasetParams = Depends(),
    db: Session = Depends(get_db),
):
    return query_dataset(common, dataset.build_filters(), db, JTData)
