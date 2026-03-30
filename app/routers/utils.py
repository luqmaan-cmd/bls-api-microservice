from typing import Any, Optional, List, Generic, TypeVar
from pydantic import BaseModel
from sqlalchemy.orm import Query
from fastapi import Query as FastapiQuery
from functools import lru_cache

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
    total = query.count()
    data = query.offset(offset).limit(limit + 1).all()
    has_more = len(data) > limit
    if has_more:
        data = data[:limit]
    
    return {
        "data": data,
        "total": total,
        "limit": limit,
        "offset": offset,
        "has_more": has_more
    }


class QueryParams:
    def __init__(
        self,
        year: Optional[str] = FastapiQuery(None, description="Filter by year (comma-separated for multiple)"),
        year_gte: Optional[int] = FastapiQuery(None, description="Year greater than or equal"),
        year_lte: Optional[int] = FastapiQuery(None, description="Year less than or equal"),
        year_gt: Optional[int] = FastapiQuery(None, description="Year greater than"),
        year_lt: Optional[int] = FastapiQuery(None, description="Year less than"),
        series_id: Optional[str] = FastapiQuery(None, description="Filter by series_id (comma-separated for multiple)"),
        limit: int = FastapiQuery(100, le=1000, description="Max results to return"),
        offset: int = FastapiQuery(0, ge=0, description="Number of results to skip")
    ):
        self.year = year
        self.year_gte = year_gte
        self.year_lte = year_lte
        self.year_gt = year_gt
        self.year_lt = year_lt
        self.series_id = series_id
        self.limit = limit
        self.offset = offset
    
    def get_year_filters(self) -> dict:
        filters = {}
        if self.year:
            years = parse_multi_value(self.year)
            if len(years) == 1:
                try:
                    filters["year"] = int(years[0])
                except ValueError:
                    pass
            else:
                filters["year"] = [int(y) for y in years if y.isdigit()]
        return filters
    
    def get_year_range_filters(self) -> dict:
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
    
    def get_series_id_filter(self) -> dict:
        if self.series_id:
            ids = parse_multi_value(self.series_id)
            if len(ids) == 1:
                return {"series_id": ids[0]}
            return {"series_id": ids}
        return {}
