from fastapi import APIRouter, Depends, Query as FastapiQuery
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models import OEData
from app.schemas import OEResponse
from app.routers.utils import (
    CommonQueryParams, PaginatedResponse, query_dataset, _parse_filter_value
)

router = APIRouter()


class OEDatasetParams:
    """OE-specific query parameters."""

    def __init__(
        self,
        area_code: Optional[str] = FastapiQuery(
            None, description="Filter by area_code (comma-separated for OR)"
        ),
        industry_code: Optional[str] = FastapiQuery(
            None, description="Filter by industry_code (comma-separated for OR)"
        ),
        occupation_code: Optional[str] = FastapiQuery(
            None, description="Filter by occupation_code (comma-separated for OR)"
        ),
        datatype_code: Optional[str] = FastapiQuery(
            None, description="Filter by datatype_code (comma-separated for OR)"
        ),
        sector_code: Optional[str] = FastapiQuery(
            None, description="Filter by sector_code (comma-separated for OR)"
        ),
        seasonal_code: Optional[str] = FastapiQuery(
            None, description="Filter by seasonal_code (comma-separated for OR)"
        ),
        areatype_code: Optional[str] = FastapiQuery(
            None, description="Filter by areatype_code (comma-separated for OR)"
        ),
    ):
        self.area_code = area_code
        self.industry_code = industry_code
        self.occupation_code = occupation_code
        self.datatype_code = datatype_code
        self.sector_code = sector_code
        self.seasonal_code = seasonal_code
        self.areatype_code = areatype_code

    def build_filters(self) -> dict:
        filters = {}
        if self.area_code:
            filters["area_code"] = _parse_filter_value(self.area_code)
        if self.industry_code:
            filters["industry_code"] = _parse_filter_value(self.industry_code)
        if self.occupation_code:
            filters["occupation_code"] = _parse_filter_value(self.occupation_code)
        if self.datatype_code:
            filters["datatype_code"] = _parse_filter_value(self.datatype_code)
        if self.sector_code:
            filters["sector_code"] = _parse_filter_value(self.sector_code)
        if self.seasonal_code:
            filters["seasonal_code"] = _parse_filter_value(self.seasonal_code)
        if self.areatype_code:
            filters["areatype_code"] = _parse_filter_value(self.areatype_code)
        return filters


@router.get("", response_model=PaginatedResponse[OEResponse])
def get_oe_data(
    common: CommonQueryParams = Depends(),
    dataset: OEDatasetParams = Depends(),
    db: Session = Depends(get_db),
):
    return query_dataset(common, dataset.build_filters(), db, OEData)
