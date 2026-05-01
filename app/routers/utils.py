from typing import Any, Optional, List, Generic, TypeVar
from pydantic import BaseModel
from sqlalchemy.orm import Query, Session
from sqlalchemy import func
from fastapi import Query as FastapiQuery, Depends

from app.database import get_db

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    data: List[T]
    total: int
    limit: int
    offset: int
    has_more: bool


def parse_multi_value(value: Optional[str]) -> Optional[List[str]]:
    if value is None:
        return None
    return [v.strip() for v in value.split(",") if v.strip()]


def apply_filters(query: Query, model, filters: dict) -> Query:
    for key, value in filters.items():
        if value is None:
            continue
        
        column = getattr(model, key, None)
        if column is None:
            continue
        
        if isinstance(value, list):
            query = query.filter(column.in_(value))
        else:
            query = query.filter(column == value)
    
    return query


def apply_range_filters(query: Query, model, range_filters: dict) -> Query:
    operators = {
        "_gte": "__ge__",
        "_lte": "__le__",
        "_gt": "__gt__",
        "_lt": "__lt__"
    }
    
    for key, value in range_filters.items():
        if value is None:
            continue
        
        for suffix, op in operators.items():
            if key.endswith(suffix):
                field_name = key[:-len(suffix)]
                column = getattr(model, field_name, None)
                if column is not None:
                    query = query.filter(getattr(column, op)(value))
                break
    
    return query


def calculate_offset(page: Optional[int], offset: Optional[int], limit: int) -> int:
    if page is not None and page > 0:
        return (page - 1) * limit
    if offset is not None:
        return offset
    return 0


def build_paginated_response(query: Query, limit: int, offset: int) -> dict:
    # Use COUNT(*) OVER() window function to get total alongside data
    # in a single query instead of separate count() + offset/limit queries.
    count_col = func.count().over().label("_total")
    query_with_count = query.add_columns(count_col)

    # Fetch limit + 1 rows to detect has_more
    rows = query_with_count.offset(offset).limit(limit + 1).all()

    has_more = len(rows) > limit
    if has_more:
        rows = rows[:limit]

    if rows:
        # Rows are (model_instance, total_count) tuples
        total = rows[0][1]
        data = [row[0] for row in rows]
    else:
        # No rows returned (offset beyond result set or empty table);
        # fall back to a separate count query for the total.
        total = query.count()
        data = []

    return {
        "data": data,
        "total": total,
        "limit": limit,
        "offset": offset,
        "has_more": has_more,
    }


def _parse_filter_value(value: Optional[str]) -> Optional[Any]:
    """Parse a comma-separated filter value into a single value or list."""
    if value is None:
        return None
    items = parse_multi_value(value)
    if not items:
        return None
    if len(items) == 1:
        return items[0]
    return items


class CommonQueryParams:
    """Shared query parameters for all dataset endpoints.

    FastAPI's Depends() inspects __init__ signatures (not class-level
    annotations), so all parameters must be declared as __init__ arguments
    with Query() defaults to appear in the OpenAPI schema and be extracted
    from incoming requests.
    """

    def __init__(
        self,
        year: Optional[str] = FastapiQuery(
            None, description="Filter by year (comma-separated for OR)"
        ),
        year_gte: Optional[int] = FastapiQuery(None, description="Year >= value"),
        year_lte: Optional[int] = FastapiQuery(None, description="Year <= value"),
        year_gt: Optional[int] = FastapiQuery(None, description="Year > value"),
        year_lt: Optional[int] = FastapiQuery(None, description="Year < value"),
        series_id: Optional[str] = FastapiQuery(
            None, description="Filter by series_id (comma-separated for OR)"
        ),
        period: Optional[str] = FastapiQuery(
            None, description="Filter by period (comma-separated for OR, e.g. M01,Q01)"
        ),
        limit: int = FastapiQuery(100, le=1000, description="Max results to return"),
        offset: Optional[int] = FastapiQuery(None, ge=0, description="Number of results to skip"),
        page: Optional[int] = FastapiQuery(None, ge=1, description="Page number"),
    ):
        self.year = year
        self.year_gte = year_gte
        self.year_lte = year_lte
        self.year_gt = year_gt
        self.year_lt = year_lt
        self.series_id = series_id
        self.period = period
        self.limit = limit
        self.offset = offset
        self.page = page

    def build_filters(self) -> dict:
        """Build equality filters from year, series_id, and period."""
        filters = {}
        if self.year:
            years = parse_multi_value(self.year)
            if years is not None:
                if len(years) == 1:
                    try:
                        filters["year"] = int(years[0])
                    except ValueError:
                        pass
                else:
                    filters["year"] = [int(y) for y in years if y.isdigit()]
        if self.series_id:
            ids = parse_multi_value(self.series_id)
            if ids is not None:
                filters["series_id"] = ids[0] if len(ids) == 1 else ids
        if self.period:
            filters["period"] = _parse_filter_value(self.period)
        return filters

    def build_range_filters(self) -> dict:
        """Build range filters from year_gte/lte/gt/lt."""
        range_filters = {}
        if self.year_gte is not None:
            range_filters["year_gte"] = self.year_gte
        if self.year_lte is not None:
            range_filters["year_lte"] = self.year_lte
        if self.year_gt is not None:
            range_filters["year_gt"] = self.year_gt
        if self.year_lt is not None:
            range_filters["year_lt"] = self.year_lt
        return range_filters

    def get_offset(self) -> int:
        """Calculate the actual offset from page/offset/limit."""
        return calculate_offset(self.page, self.offset, self.limit)


def query_dataset(common: CommonQueryParams, dataset_filters: dict, db: Session, model) -> dict:
    """Generic query function that applies all filters and returns paginated results.

    Args:
        common: The shared query params (year, series_id, pagination).
        dataset_filters: Pre-built dict of dataset-specific equality filters.
        db: SQLAlchemy session.
        model: The SQLAlchemy model class to query.
    """
    query = db.query(model)

    filters = common.build_filters()
    filters.update(dataset_filters)
    query = apply_filters(query, model, filters)

    range_filters = common.build_range_filters()
    query = apply_range_filters(query, model, range_filters)

    actual_offset = common.get_offset()
    return build_paginated_response(query, common.limit, actual_offset)
