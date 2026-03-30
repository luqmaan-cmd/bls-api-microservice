from pydantic import BaseModel
from typing import Optional
from decimal import Decimal


class CEResponse(BaseModel):
    series_id: str
    year: int
    period: str
    period_name: Optional[str] = None
    value: Optional[Decimal] = None
    supersector_code: Optional[str] = None
    supersector_name: Optional[str] = None
    industry_code: Optional[str] = None
    industry_name: Optional[str] = None
    datatype_code: Optional[str] = None
    datatype_name: Optional[str] = None
    seasonal_code: Optional[str] = None
    seasonal_name: Optional[str] = None
    footnote_codes: Optional[str] = None

    class Config:
        from_attributes = True


class CPIResponse(BaseModel):
    id: int
    series_id: Optional[str] = None
    year: Optional[int] = None
    period: Optional[str] = None
    period_name: Optional[str] = None
    value: Optional[Decimal] = None
    area_code: Optional[str] = None
    area_name: Optional[str] = None
    item_code: Optional[str] = None
    item_name: Optional[str] = None
    seasonal_code: Optional[str] = None
    seasonal_text: Optional[str] = None

    class Config:
        from_attributes = True


class PPIResponse(BaseModel):
    series_id: str
    year: int
    period: str
    period_name: Optional[str] = None
    value: Optional[Decimal] = None
    measure_code: Optional[str] = None
    measure_name: Optional[str] = None
    sector_code: Optional[str] = None
    sector_name: Optional[str] = None
    class_code: Optional[str] = None
    class_name: Optional[str] = None
    duration_code: Optional[str] = None
    duration_name: Optional[str] = None
    seasonal_code: Optional[str] = None
    seasonal_name: Optional[str] = None
    footnote_codes: Optional[str] = None

    class Config:
        from_attributes = True


class JTResponse(BaseModel):
    series_id: str
    year: int
    period: str
    value: Optional[Decimal] = None
    industry_code: Optional[str] = None
    industry_name: Optional[str] = None
    state_code: Optional[str] = None
    state_name: Optional[str] = None
    area_code: Optional[str] = None
    area_name: Optional[str] = None
    sizeclass_code: Optional[str] = None
    sizeclass_name: Optional[str] = None
    dataelement_code: Optional[str] = None
    dataelement_name: Optional[str] = None
    ratelevel_code: Optional[str] = None
    ratelevel_name: Optional[str] = None
    seasonal_code: Optional[str] = None
    seasonal_name: Optional[str] = None
    footnote_codes: Optional[str] = None

    class Config:
        from_attributes = True


class LAResponse(BaseModel):
    series_id: str
    year: int
    period: str
    value: Optional[Decimal] = None
    area_type_code: Optional[str] = None
    area_type_name: Optional[str] = None
    area_code: Optional[str] = None
    area_name: Optional[str] = None
    measure_code: Optional[str] = None
    measure_name: Optional[str] = None
    seasonal_code: Optional[str] = None
    seasonal_name: Optional[str] = None
    state_code: Optional[str] = None
    state_name: Optional[str] = None
    footnote_codes: Optional[str] = None

    class Config:
        from_attributes = True


class CIResponse(BaseModel):
    series_id: str
    year: int
    period: str
    value: Optional[Decimal] = None
    owner_code: Optional[str] = None
    owner_name: Optional[str] = None
    industry_code: Optional[str] = None
    industry_name: Optional[str] = None
    occupation_code: Optional[str] = None
    occupation_name: Optional[str] = None
    area_code: Optional[str] = None
    area_name: Optional[str] = None
    estimate_code: Optional[str] = None
    estimate_name: Optional[str] = None
    periodicity_code: Optional[str] = None
    periodicity_name: Optional[str] = None
    seasonal_code: Optional[str] = None
    seasonal_name: Optional[str] = None
    footnote_codes: Optional[str] = None

    class Config:
        from_attributes = True


class MPResponse(BaseModel):
    series_id: str
    year: int
    period: str
    value: Optional[Decimal] = None
    sector_code: Optional[str] = None
    sector_name: Optional[str] = None
    measure_code: Optional[str] = None
    measure_name: Optional[str] = None
    duration_code: Optional[str] = None
    duration_name: Optional[str] = None
    seasonal_code: Optional[str] = None
    seasonal_name: Optional[str] = None
    footnote_codes: Optional[str] = None

    class Config:
        from_attributes = True


class OEResponse(BaseModel):
    series_id: str
    year: int
    period: str
    value: Optional[Decimal] = None
    areatype_code: Optional[str] = None
    areatype_name: Optional[str] = None
    area_code: Optional[str] = None
    area_name: Optional[str] = None
    industry_code: Optional[str] = None
    industry_name: Optional[str] = None
    occupation_code: Optional[str] = None
    occupation_name: Optional[str] = None
    datatype_code: Optional[str] = None
    datatype_name: Optional[str] = None
    sector_code: Optional[str] = None
    sector_name: Optional[str] = None
    seasonal_code: Optional[str] = None
    seasonal_name: Optional[str] = None
    footnote_codes: Optional[str] = None

    class Config:
        from_attributes = True


class SAResponse(BaseModel):
    series_id: str
    year: int
    period: str
    value: Optional[Decimal] = None
    state_code: Optional[str] = None
    state_name: Optional[str] = None
    area_code: Optional[str] = None
    area_name: Optional[str] = None
    industry_code: Optional[str] = None
    industry_name: Optional[str] = None
    detail_code: Optional[str] = None
    detail_name: Optional[str] = None
    data_type_code: Optional[str] = None
    data_type_name: Optional[str] = None
    seasonal_code: Optional[str] = None
    seasonal_name: Optional[str] = None
    footnote_codes: Optional[str] = None

    class Config:
        from_attributes = True


class SMResponse(BaseModel):
    series_id: str
    year: int
    period: str
    value: Optional[Decimal] = None
    state_code: Optional[str] = None
    state_name: Optional[str] = None
    area_code: Optional[str] = None
    area_name: Optional[str] = None
    supersector_code: Optional[str] = None
    supersector_name: Optional[str] = None
    industry_code: Optional[str] = None
    industry_name: Optional[str] = None
    data_type_code: Optional[str] = None
    data_type_name: Optional[str] = None
    seasonal_code: Optional[str] = None
    seasonal_name: Optional[str] = None
    footnote_codes: Optional[str] = None

    class Config:
        from_attributes = True
