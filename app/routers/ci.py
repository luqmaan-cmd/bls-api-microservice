from fastapi import APIRouter, Depends, Query as FastapiQuery
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models import CIData
from app.schemas import CIResponse
from app.routers.utils import (
    CommonQueryParams, PaginatedResponse, query_dataset, _parse_filter_value
)

router = APIRouter()


class CIDatasetParams:
    """CI-specific query parameters."""

    def __init__(
        self,
        industry_code: Optional[str] = FastapiQuery(
            None, description="Filter by industry_code (comma-separated for OR)"
        ),
        occupation_code: Optional[str] = FastapiQuery(
            None, description="Filter by occupation_code (comma-separated for OR)"
        ),
        area_code: Optional[str] = FastapiQuery(
            None, description="Filter by area_code (comma-separated for OR)"
        ),
        seasonal_code: Optional[str] = FastapiQuery(
            None, description="Filter by seasonal_code (comma-separated for OR)"
        ),
        owner_code: Optional[str] = FastapiQuery(
            None, description="Filter by owner_code (comma-separated for OR)"
        ),
        estimate_code: Optional[str] = FastapiQuery(
            None, description="Filter by estimate_code (comma-separated for OR)"
        ),
        periodicity_code: Optional[str] = FastapiQuery(
            None, description="Filter by periodicity_code (comma-separated for OR)"
        ),
    ):
        self.industry_code = industry_code
        self.occupation_code = occupation_code
        self.area_code = area_code
        self.seasonal_code = seasonal_code
        self.owner_code = owner_code
        self.estimate_code = estimate_code
        self.periodicity_code = periodicity_code

    def build_filters(self) -> dict:
        filters = {}
        if self.industry_code:
            filters["industry_code"] = _parse_filter_value(self.industry_code)
        if self.occupation_code:
            filters["occupation_code"] = _parse_filter_value(self.occupation_code)
        if self.area_code:
            filters["area_code"] = _parse_filter_value(self.area_code)
        if self.seasonal_code:
            filters["seasonal_code"] = _parse_filter_value(self.seasonal_code)
        if self.owner_code:
            filters["owner_code"] = _parse_filter_value(self.owner_code)
        if self.estimate_code:
            filters["estimate_code"] = _parse_filter_value(self.estimate_code)
        if self.periodicity_code:
            filters["periodicity_code"] = _parse_filter_value(self.periodicity_code)
        return filters


@router.get("", response_model=PaginatedResponse[CIResponse])
def get_ci_data(
    common: CommonQueryParams = Depends(),
    dataset: CIDatasetParams = Depends(),
    db: Session = Depends(get_db),
):
    return query_dataset(common, dataset.build_filters(), db, CIData)
