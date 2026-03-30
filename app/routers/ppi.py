from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models import PPIData
from app.schemas import PPIResponse
from app.routers.utils import (
    apply_filters, apply_range_filters, build_paginated_response,
    calculate_offset, parse_multi_value, PaginatedResponse
)

router = APIRouter()


@router.get("", response_model=PaginatedResponse[PPIResponse])
def get_ppi_data(
    year: Optional[str] = Query(None, description="Filter by year (comma-separated for OR)"),
    year_gte: Optional[int] = Query(None, description="Year >= value"),
    year_lte: Optional[int] = Query(None, description="Year <= value"),
    year_gt: Optional[int] = Query(None, description="Year > value"),
    year_lt: Optional[int] = Query(None, description="Year < value"),
    series_id: Optional[str] = Query(None, description="Filter by series_id (comma-separated for OR)"),
    sector_code: Optional[str] = Query(None, description="Filter by sector_code (comma-separated for OR)"),
    class_code: Optional[str] = Query(None, description="Filter by class_code (comma-separated for OR)"),
    measure_code: Optional[str] = Query(None, description="Filter by measure_code (comma-separated for OR)"),
    seasonal_code: Optional[str] = Query(None, description="Filter by seasonal_code (comma-separated for OR)"),
    limit: int = Query(100, le=1000),
    offset: Optional[int] = Query(None, ge=0),
    page: Optional[int] = Query(None, ge=1),
    db: Session = Depends(get_db)
):
    query = db.query(PPIData)
    
    filters = {}
    if year:
        years = parse_multi_value(year)
        filters["year"] = int(years[0]) if len(years) == 1 else [int(y) for y in years]
    if series_id:
        ids = parse_multi_value(series_id)
        filters["series_id"] = ids[0] if len(ids) == 1 else ids
    if sector_code:
        codes = parse_multi_value(sector_code)
        filters["sector_code"] = codes[0] if len(codes) == 1 else codes
    if class_code:
        codes = parse_multi_value(class_code)
        filters["class_code"] = codes[0] if len(codes) == 1 else codes
    if measure_code:
        codes = parse_multi_value(measure_code)
        filters["measure_code"] = codes[0] if len(codes) == 1 else codes
    if seasonal_code:
        codes = parse_multi_value(seasonal_code)
        filters["seasonal_code"] = codes[0] if len(codes) == 1 else codes
    
    query = apply_filters(query, PPIData, filters)
    
    range_filters = {}
    if year_gte is not None:
        range_filters["year_gte"] = year_gte
    if year_lte is not None:
        range_filters["year_lte"] = year_lte
    if year_gt is not None:
        range_filters["year_gt"] = year_gt
    if year_lt is not None:
        range_filters["year_lt"] = year_lt
    
    query = apply_range_filters(query, PPIData, range_filters)
    
    actual_offset = calculate_offset(page, offset, limit)
    return build_paginated_response(query, limit, actual_offset)
