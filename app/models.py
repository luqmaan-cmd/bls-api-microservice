from sqlalchemy import Column, String, Integer, Numeric
from app.database import Base


class CEData(Base):
    __tablename__ = "ce_data"

    series_id = Column(String(20), primary_key=True)
    year = Column(Integer, primary_key=True)
    period = Column(String(3), primary_key=True)
    period_name = Column(String(20))
    value = Column(Numeric(14, 2))
    supersector_code = Column(String(5))
    supersector_name = Column(String(100))
    industry_code = Column(String(10))
    industry_name = Column(String(200))
    datatype_code = Column(String(5))
    datatype_name = Column(String(100))
    seasonal_code = Column(String(1))
    seasonal_name = Column(String(30))
    footnote_codes = Column(String(10))


class CPIData(Base):
    __tablename__ = "cpi_data"

    id = Column(Integer, primary_key=True)
    series_id = Column(String(20))
    year = Column(Integer)
    period = Column(String(5))
    period_name = Column(String(50))
    value = Column(Numeric(15, 4))
    area_code = Column(String(10))
    area_name = Column(String(255))
    item_code = Column(String(20))
    item_name = Column(String(500))
    seasonal_code = Column(String(1))
    seasonal_text = Column(String(50))


class PPIData(Base):
    __tablename__ = "ppi_data"

    series_id = Column(String(20), primary_key=True)
    year = Column(Integer, primary_key=True)
    period = Column(String(3), primary_key=True)
    period_name = Column(String(20))
    value = Column(Numeric(12, 4))
    measure_code = Column(String(2))
    measure_name = Column(String(100))
    sector_code = Column(String(10))
    sector_name = Column(String(200))
    class_code = Column(String(10))
    class_name = Column(String(200))
    duration_code = Column(String(2))
    duration_name = Column(String(50))
    seasonal_code = Column(String(1))
    seasonal_name = Column(String(20))
    footnote_codes = Column(String(10))


class JTData(Base):
    __tablename__ = "jt_data"

    series_id = Column(String(22), primary_key=True)
    year = Column(Integer, primary_key=True)
    period = Column(String(3), primary_key=True)
    value = Column(Numeric(14, 2))
    industry_code = Column(String(10))
    industry_name = Column(String(200))
    state_code = Column(String(10))
    state_name = Column(String(100))
    area_code = Column(String(10))
    area_name = Column(String(200))
    sizeclass_code = Column(String(10))
    sizeclass_name = Column(String(100))
    dataelement_code = Column(String(10))
    dataelement_name = Column(String(100))
    ratelevel_code = Column(String(10))
    ratelevel_name = Column(String(50))
    seasonal_code = Column(String(10))
    seasonal_name = Column(String(30))
    footnote_codes = Column(String(10))


class LAData(Base):
    __tablename__ = "la_data"

    series_id = Column(String(20), primary_key=True)
    year = Column(Integer, primary_key=True)
    period = Column(String(3), primary_key=True)
    value = Column(Numeric(14, 2))
    area_type_code = Column(String(2))
    area_type_name = Column(String(100))
    area_code = Column(String(20))
    area_name = Column(String(200))
    measure_code = Column(String(2))
    measure_name = Column(String(100))
    seasonal_code = Column(String(1))
    seasonal_name = Column(String(30))
    state_code = Column(String(2))
    state_name = Column(String(100))
    footnote_codes = Column(String(10))


class CIData(Base):
    __tablename__ = "ci_data"

    series_id = Column(String(20), primary_key=True)
    year = Column(Integer, primary_key=True)
    period = Column(String(3), primary_key=True)
    value = Column(Numeric(14, 2))
    owner_code = Column(String(10))
    owner_name = Column(String(100))
    industry_code = Column(String(10))
    industry_name = Column(String(200))
    occupation_code = Column(String(10))
    occupation_name = Column(String(200))
    area_code = Column(String(10))
    area_name = Column(String(200))
    estimate_code = Column(String(10))
    estimate_name = Column(String(200))
    periodicity_code = Column(String(10))
    periodicity_name = Column(String(50))
    seasonal_code = Column(String(10))
    seasonal_name = Column(String(30))
    footnote_codes = Column(String(10))


class MPData(Base):
    __tablename__ = "mp_data"

    series_id = Column(String(20), primary_key=True)
    year = Column(Integer, primary_key=True)
    period = Column(String(3), primary_key=True)
    value = Column(Numeric(14, 2))
    sector_code = Column(String(10))
    sector_name = Column(String(200))
    measure_code = Column(String(10))
    measure_name = Column(String(100))
    duration_code = Column(String(10))
    duration_name = Column(String(100))
    seasonal_code = Column(String(10))
    seasonal_name = Column(String(30))
    footnote_codes = Column(String(10))


class OEData(Base):
    __tablename__ = "oe_data"

    series_id = Column(String(35), primary_key=True)
    year = Column(Integer, primary_key=True)
    period = Column(String(10), primary_key=True)
    value = Column(Numeric(14, 2))
    areatype_code = Column(String(10))
    areatype_name = Column(String(100))
    area_code = Column(String(20))
    area_name = Column(String(200))
    industry_code = Column(String(20))
    industry_name = Column(String(200))
    occupation_code = Column(String(20))
    occupation_name = Column(String(200))
    datatype_code = Column(String(10))
    datatype_name = Column(String(100))
    sector_code = Column(String(20))
    sector_name = Column(String(100))
    seasonal_code = Column(String(10))
    seasonal_name = Column(String(30))
    footnote_codes = Column(String(250))


class SAData(Base):
    __tablename__ = "sa_data"

    series_id = Column(String(20), primary_key=True)
    year = Column(Integer, primary_key=True)
    period = Column(String(3), primary_key=True)
    value = Column(Numeric(14, 2))
    state_code = Column(String(2))
    state_name = Column(String(100))
    area_code = Column(String(10))
    area_name = Column(String(200))
    industry_code = Column(String(10))
    industry_name = Column(String(200))
    detail_code = Column(String(2))
    detail_name = Column(String(100))
    data_type_code = Column(String(2))
    data_type_name = Column(String(100))
    seasonal_code = Column(String(1))
    seasonal_name = Column(String(30))
    footnote_codes = Column(String(10))


class SMData(Base):
    __tablename__ = "sm_data"

    series_id = Column(String(22), primary_key=True)
    year = Column(Integer, primary_key=True)
    period = Column(String(3), primary_key=True)
    value = Column(Numeric(14, 2))
    state_code = Column(String(2))
    state_name = Column(String(100))
    area_code = Column(String(10))
    area_name = Column(String(200))
    supersector_code = Column(String(2))
    supersector_name = Column(String(100))
    industry_code = Column(String(10))
    industry_name = Column(String(200))
    data_type_code = Column(String(2))
    data_type_name = Column(String(100))
    seasonal_code = Column(String(1))
    seasonal_name = Column(String(30))
    footnote_codes = Column(String(10))
