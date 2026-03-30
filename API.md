# BLS API Microservice

**Version:** 1.0.0  
**Base URL:** `https://your-deployed-url.com`  
**Last Updated:** March 2026

---

## Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Common Parameters](#common-parameters)
4. [Response Format](#response-format)
5. [Endpoints](#endpoints)
   - [Consumer Price Index (CPI)](#1-consumer-price-index-cpi)
   - [Current Employment Statistics (CE)](#2-current-employment-statistics-ce)
   - [Producer Price Index (PPI)](#3-producer-price-index-ppi)
   - [Job Openings and Labor Turnover (JOLTS)](#4-job-openings-and-labor-turnover-jolts)
   - [Local Area Unemployment Statistics (LA)](#5-local-area-unemployment-statistics-la)
   - [Employment Cost Index (CI)](#6-employment-cost-index-ci)
   - [Mass Layoff Statistics (MP)](#7-mass-layoff-statistics-mp)
   - [Occupational Employment and Wages (OE)](#8-occupational-employment-and-wages-oe)
   - [State and Area Employment (SA)](#9-state-and-area-employment-sa)
   - [State and Metropolitan Employment (SM)](#10-state-and-metropolitan-employment-sm)
6. [Error Handling](#error-handling)
7. [Rate Limits](#rate-limits)
8. [Support](#support)

---

## Overview

The BLS API Microservice provides programmatic access to 10 Bureau of Labor Statistics (BLS) datasets. This RESTful API enables developers to query employment, inflation, and labor market data stored in a PostgreSQL database.

### Available Datasets

| Dataset | Code | Description |
|---------|------|-------------|
| Consumer Price Index | CPI | Measures price changes in goods and services |
| Current Employment Statistics | CE | Employment, hours, and earnings by industry |
| Producer Price Index | PPI | Measures price changes from sellers' perspective |
| Job Openings and Labor Turnover | JT | Job openings, hires, and separations |
| Local Area Unemployment | LA | Unemployment data for local areas |
| Employment Cost Index | CI | Changes in employer labor costs |
| Mass Layoff Statistics | MP | Large-scale layoff events |
| Occupational Employment and Wages | OE | Employment and wages by occupation |
| State and Area Employment | SA | Employment by state and area |
| State and Metropolitan Employment | SM | Employment for states and metros |

---

## Authentication

All API requests require authentication via an API key.

### How to Authenticate

Include your API key as a query parameter in every request:

```
GET /cpi?api_key=YOUR_API_KEY
```

### Example Request

```bash
curl "https://your-deployed-url.com/cpi?api_key=YOUR_API_KEY&limit=10"
```

### Error Response (Missing/Invalid Key)

```json
{
  "detail": "Invalid or missing API key"
}
```

---

## Common Parameters

All endpoints support the following query parameters:

### Pagination

| Parameter | Type | Default | Max | Description |
|-----------|------|---------|-----|-------------|
| `limit` | integer | 100 | 1000 | Maximum number of records to return |
| `offset` | integer | 0 | — | Number of records to skip |
| `page` | integer | — | — | Page number (1-based). Overrides `offset` if provided |

### Year Filtering

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `year` | string | Exact year match (comma-separated for multiple) | `year=2023` or `year=2021,2022,2023` |
| `year_gte` | integer | Year greater than or equal to | `year_gte=2020` |
| `year_lte` | integer | Year less than or equal to | `year_lte=2023` |
| `year_gt` | integer | Year greater than | `year_gt=2019` |
| `year_lt` | integer | Year less than | `year_lt=2024` |

### Multi-Value Filtering

Most filter parameters accept comma-separated values for OR logic:

```
?area_code=0000,0100&industry_code=100000,200000
```

---

## Response Format

All endpoints return a standardized paginated response:

```json
{
  "data": [
    { "...record 1..." },
    { "...record 2..." }
  ],
  "total": 15420,
  "limit": 100,
  "offset": 0,
  "has_more": true
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `data` | array | Array of records matching the query |
| `total` | integer | Total number of matching records |
| `limit` | integer | Maximum records returned in this response |
| `offset` | integer | Number of records skipped |
| `has_more` | boolean | Whether more records are available |

---

## Endpoints

---

### 1. Consumer Price Index (CPI)

Measures the average change over time in prices paid by urban consumers for a market basket of consumer goods and services.

| Property | Value |
|----------|-------|
| **Endpoint** | `GET /cpi` |
| **Table** | `cpi_data` |
| **HTTP Method** | GET |

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `year` | string | Filter by year (comma-separated for OR) |
| `year_gte` | integer | Year ≥ value |
| `year_lte` | integer | Year ≤ value |
| `year_gt` | integer | Year > value |
| `year_lt` | integer | Year < value |
| `series_id` | string | Filter by series ID |
| `area_code` | string | Filter by geographic area code |
| `item_code` | string | Filter by item category code |
| `seasonal_code` | string | Filter by seasonal adjustment (S/U) |
| `limit` | integer | Max results (default: 100, max: 1000) |
| `offset` | integer | Records to skip |
| `page` | integer | Page number |

#### Response Schema

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Unique record identifier |
| `series_id` | string | BLS series identifier |
| `year` | integer | Data year |
| `period` | string | Period identifier (e.g., "M01") |
| `period_name` | string | Period name (e.g., "January") |
| `value` | decimal | CPI index value |
| `area_code` | string | Geographic area code |
| `area_name` | string | Geographic area name |
| `item_code` | string | Item category code |
| `item_name` | string | Item category name |
| `seasonal_code` | string | Seasonal adjustment code |
| `seasonal_text` | string | Seasonal adjustment description |

#### Example Request

```bash
GET /cpi?year=2023&area_code=0000&limit=10&api_key=YOUR_KEY
```

#### Example Response

```json
{
  "data": [
    {
      "id": 1,
      "series_id": "CUSR0000SA0",
      "year": 2023,
      "period": "M01",
      "period_name": "January",
      "value": 299.170,
      "area_code": "0000",
      "area_name": "U.S. city average",
      "item_code": "SA0",
      "item_name": "All items",
      "seasonal_code": "S",
      "seasonal_text": "Seasonally Adjusted"
    }
  ],
  "total": 1,
  "limit": 10,
  "offset": 0,
  "has_more": false
}
```

---

### 2. Current Employment Statistics (CE)

Provides national data on employment, hours, and earnings by industry.

| Property | Value |
|----------|-------|
| **Endpoint** | `GET /ce` |
| **Table** | `ce_data` |
| **HTTP Method** | GET |

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `year` | string | Filter by year (comma-separated for OR) |
| `year_gte` | integer | Year ≥ value |
| `year_lte` | integer | Year ≤ value |
| `year_gt` | integer | Year > value |
| `year_lt` | integer | Year < value |
| `series_id` | string | Filter by series ID |
| `industry_code` | string | Filter by industry code |
| `supersector_code` | string | Filter by supersector code |
| `datatype_code` | string | Filter by data type code |
| `seasonal_code` | string | Filter by seasonal adjustment |
| `limit` | integer | Max results (default: 100, max: 1000) |
| `offset` | integer | Records to skip |
| `page` | integer | Page number |

#### Response Schema

| Field | Type | Description |
|-------|------|-------------|
| `series_id` | string | BLS series identifier |
| `year` | integer | Data year |
| `period` | string | Period identifier |
| `period_name` | string | Period name |
| `value` | decimal | Data value |
| `supersector_code` | string | Supersector code |
| `supersector_name` | string | Supersector name |
| `industry_code` | string | Industry code |
| `industry_name` | string | Industry name |
| `datatype_code` | string | Data type code |
| `datatype_name` | string | Data type name |
| `seasonal_code` | string | Seasonal adjustment code |
| `seasonal_name` | string | Seasonal adjustment name |
| `footnote_codes` | string | Footnote codes |

#### Example Request

```bash
GET /ce?year=2023&industry_code=05000000&api_key=YOUR_KEY
```

#### Example Response

```json
{
  "data": [
    {
      "series_id": "CES0000000001",
      "year": 2023,
      "period": "M01",
      "period_name": "January",
      "value": 155276.0,
      "supersector_code": "00",
      "supersector_name": "Total nonfarm",
      "industry_code": "00000000",
      "industry_name": "Total nonfarm",
      "datatype_code": "01",
      "datatype_name": "All Employees, In Thousands",
      "seasonal_code": "S",
      "seasonal_name": "Seasonally Adjusted",
      "footnote_codes": null
    }
  ],
  "total": 1,
  "limit": 100,
  "offset": 0,
  "has_more": false
}
```

---

### 3. Producer Price Index (PPI)

Measures average changes in selling prices received by domestic producers for their output.

| Property | Value |
|----------|-------|
| **Endpoint** | `GET /ppi` |
| **Table** | `ppi_data` |
| **HTTP Method** | GET |

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `year` | string | Filter by year (comma-separated for OR) |
| `year_gte` | integer | Year ≥ value |
| `year_lte` | integer | Year ≤ value |
| `year_gt` | integer | Year > value |
| `year_lt` | integer | Year < value |
| `series_id` | string | Filter by series ID |
| `sector_code` | string | Filter by sector code |
| `class_code` | string | Filter by class code |
| `measure_code` | string | Filter by measure code |
| `seasonal_code` | string | Filter by seasonal adjustment |
| `limit` | integer | Max results (default: 100, max: 1000) |
| `offset` | integer | Records to skip |
| `page` | integer | Page number |

#### Response Schema

| Field | Type | Description |
|-------|------|-------------|
| `series_id` | string | BLS series identifier |
| `year` | integer | Data year |
| `period` | string | Period identifier |
| `period_name` | string | Period name |
| `value` | decimal | PPI index value |
| `measure_code` | string | Measure code |
| `measure_name` | string | Measure name |
| `sector_code` | string | Sector code |
| `sector_name` | string | Sector name |
| `class_code` | string | Class code |
| `class_name` | string | Class name |
| `duration_code` | string | Duration code |
| `duration_name` | string | Duration name |
| `seasonal_code` | string | Seasonal adjustment code |
| `seasonal_name` | string | Seasonal adjustment name |
| `footnote_codes` | string | Footnote codes |

#### Example Request

```bash
GET /ppi?year_gte=2020&year_lte=2023&api_key=YOUR_KEY
```

#### Example Response

```json
{
  "data": [
    {
      "series_id": "WPUFD4111",
      "year": 2023,
      "period": "M01",
      "period_name": "January",
      "value": 287.5,
      "measure_code": "01",
      "measure_name": "Index",
      "sector_code": "FD4",
      "sector_name": "Final demand",
      "class_code": "411",
      "class_name": "Foods",
      "duration_code": null,
      "duration_name": null,
      "seasonal_code": "S",
      "seasonal_name": "Seasonally Adjusted",
      "footnote_codes": null
    }
  ],
  "total": 1,
  "limit": 100,
  "offset": 0,
  "has_more": false
}
```

---

### 4. Job Openings and Labor Turnover (JOLTS)

Measures job vacancies, hires, and separations to gauge labor market dynamics.

| Property | Value |
|----------|-------|
| **Endpoint** | `GET /jt` |
| **Table** | `jt_data` |
| **HTTP Method** | GET |

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `year` | string | Filter by year (comma-separated for OR) |
| `year_gte` | integer | Year ≥ value |
| `year_lte` | integer | Year ≤ value |
| `year_gt` | integer | Year > value |
| `year_lt` | integer | Year < value |
| `series_id` | string | Filter by series ID |
| `state_code` | string | Filter by state code |
| `industry_code` | string | Filter by industry code |
| `area_code` | string | Filter by area code |
| `dataelement_code` | string | Filter by data element code |
| `limit` | integer | Max results (default: 100, max: 1000) |
| `offset` | integer | Records to skip |
| `page` | integer | Page number |

#### Response Schema

| Field | Type | Description |
|-------|------|-------------|
| `series_id` | string | BLS series identifier |
| `year` | integer | Data year |
| `period` | string | Period identifier |
| `value` | decimal | Data value |
| `industry_code` | string | Industry code |
| `industry_name` | string | Industry name |
| `state_code` | string | State code |
| `state_name` | string | State name |
| `area_code` | string | Area code |
| `area_name` | string | Area name |
| `sizeclass_code` | string | Establishment size class code |
| `sizeclass_name` | string | Establishment size class name |
| `dataelement_code` | string | Data element code |
| `dataelement_name` | string | Data element name |
| `ratelevel_code` | string | Rate/level indicator code |
| `ratelevel_name` | string | Rate/level indicator name |
| `seasonal_code` | string | Seasonal adjustment code |
| `seasonal_name` | string | Seasonal adjustment name |
| `footnote_codes` | string | Footnote codes |

#### Example Request

```bash
GET /jt?state_code=00&year=2023&api_key=YOUR_KEY
```

#### Example Response

```json
{
  "data": [
    {
      "series_id": "JTU00000000000000000JOL",
      "year": 2023,
      "period": "M01",
      "value": 11042.0,
      "industry_code": "000000",
      "industry_name": "Total nonfarm",
      "state_code": "00",
      "state_name": "Total US",
      "area_code": "00",
      "area_name": "Total US",
      "sizeclass_code": "00",
      "sizeclass_name": "Total all sizes",
      "dataelement_code": "JOL",
      "dataelement_name": "Job Openings",
      "ratelevel_code": "L",
      "ratelevel_name": "Level in Thousands",
      "seasonal_code": "S",
      "seasonal_name": "Seasonally Adjusted",
      "footnote_codes": null
    }
  ],
  "total": 1,
  "limit": 100,
  "offset": 0,
  "has_more": false
}
```

---

### 5. Local Area Unemployment Statistics (LA)

Provides employment and unemployment data for states, counties, and metropolitan areas.

| Property | Value |
|----------|-------|
| **Endpoint** | `GET /la` |
| **Table** | `la_data` |
| **HTTP Method** | GET |

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `year` | string | Filter by year (comma-separated for OR) |
| `year_gte` | integer | Year ≥ value |
| `year_lte` | integer | Year ≤ value |
| `year_gt` | integer | Year > value |
| `year_lt` | integer | Year < value |
| `series_id` | string | Filter by series ID |
| `state_code` | string | Filter by state code |
| `area_code` | string | Filter by area code |
| `measure_code` | string | Filter by measure code |
| `seasonal_code` | string | Filter by seasonal adjustment |
| `limit` | integer | Max results (default: 100, max: 1000) |
| `offset` | integer | Records to skip |
| `page` | integer | Page number |

#### Response Schema

| Field | Type | Description |
|-------|------|-------------|
| `series_id` | string | BLS series identifier |
| `year` | integer | Data year |
| `period` | string | Period identifier |
| `value` | decimal | Data value |
| `area_type_code` | string | Area type code |
| `area_type_name` | string | Area type name |
| `area_code` | string | Area code |
| `area_name` | string | Area name |
| `measure_code` | string | Measure code |
| `measure_name` | string | Measure name |
| `seasonal_code` | string | Seasonal adjustment code |
| `seasonal_name` | string | Seasonal adjustment name |
| `state_code` | string | State code |
| `state_name` | string | State name |
| `footnote_codes` | string | Footnote codes |

#### Example Request

```bash
GET /la?state_code=06&year=2023&api_key=YOUR_KEY
```

#### Example Response

```json
{
  "data": [
    {
      "series_id": "LASST060000000000003",
      "year": 2023,
      "period": "M01",
      "value": 4.2,
      "area_type_code": "A",
      "area_type_name": "State",
      "area_code": "06000000",
      "area_name": "California",
      "measure_code": "03",
      "measure_name": "Unemployment Rate",
      "seasonal_code": "S",
      "seasonal_name": "Seasonally Adjusted",
      "state_code": "06",
      "state_name": "California",
      "footnote_codes": null
    }
  ],
  "total": 1,
  "limit": 100,
  "offset": 0,
  "has_more": false
}
```

---

### 6. Employment Cost Index (CI)

Measures changes in the costs of labor compensation over time.

| Property | Value |
|----------|-------|
| **Endpoint** | `GET /ci` |
| **Table** | `ci_data` |
| **HTTP Method** | GET |

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `year` | string | Filter by year (comma-separated for OR) |
| `year_gte` | integer | Year ≥ value |
| `year_lte` | integer | Year ≤ value |
| `year_gt` | integer | Year > value |
| `year_lt` | integer | Year < value |
| `series_id` | string | Filter by series ID |
| `industry_code` | string | Filter by industry code |
| `occupation_code` | string | Filter by occupation code |
| `area_code` | string | Filter by area code |
| `limit` | integer | Max results (default: 100, max: 1000) |
| `offset` | integer | Records to skip |
| `page` | integer | Page number |

#### Response Schema

| Field | Type | Description |
|-------|------|-------------|
| `series_id` | string | BLS series identifier |
| `year` | integer | Data year |
| `period` | string | Period identifier |
| `value` | decimal | Index value |
| `owner_code` | string | Owner code |
| `owner_name` | string | Owner name |
| `industry_code` | string | Industry code |
| `industry_name` | string | Industry name |
| `occupation_code` | string | Occupation code |
| `occupation_name` | string | Occupation name |
| `area_code` | string | Area code |
| `area_name` | string | Area name |
| `estimate_code` | string | Estimate code |
| `estimate_name` | string | Estimate name |
| `periodicity_code` | string | Periodicity code |
| `periodicity_name` | string | Periodicity name |
| `seasonal_code` | string | Seasonal adjustment code |
| `seasonal_name` | string | Seasonal adjustment name |
| `footnote_codes` | string | Footnote codes |

#### Example Request

```bash
GET /ci?year=2023&industry_code=000000&api_key=YOUR_KEY
```

#### Example Response

```json
{
  "data": [
    {
      "series_id": "CIU1010000000000I",
      "year": 2023,
      "period": "Q01",
      "value": 155.2,
      "owner_code": "1",
      "owner_name": "Civilian",
      "industry_code": "10100000",
      "industry_name": "Goods-producing industries",
      "occupation_code": "000000",
      "occupation_name": "All workers",
      "area_code": "00",
      "area_name": "United States",
      "estimate_code": "01",
      "estimate_name": "Wages and salaries",
      "periodicity_code": "Q",
      "periodicity_name": "Quarterly",
      "seasonal_code": "S",
      "seasonal_name": "Seasonally Adjusted",
      "footnote_codes": null
    }
  ],
  "total": 1,
  "limit": 100,
  "offset": 0,
  "has_more": false
}
```

---

### 7. Mass Layoff Statistics (MP)

Tracks large-scale layoff events and initial claimants for unemployment insurance.

| Property | Value |
|----------|-------|
| **Endpoint** | `GET /mp` |
| **Table** | `mp_data` |
| **HTTP Method** | GET |

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `year` | string | Filter by year (comma-separated for OR) |
| `year_gte` | integer | Year ≥ value |
| `year_lte` | integer | Year ≤ value |
| `year_gt` | integer | Year > value |
| `year_lt` | integer | Year < value |
| `series_id` | string | Filter by series ID |
| `sector_code` | string | Filter by sector code |
| `measure_code` | string | Filter by measure code |
| `duration_code` | string | Filter by duration code |
| `limit` | integer | Max results (default: 100, max: 1000) |
| `offset` | integer | Records to skip |
| `page` | integer | Page number |

#### Response Schema

| Field | Type | Description |
|-------|------|-------------|
| `series_id` | string | BLS series identifier |
| `year` | integer | Data year |
| `period` | string | Period identifier |
| `value` | decimal | Data value |
| `sector_code` | string | Sector code |
| `sector_name` | string | Sector name |
| `measure_code` | string | Measure code |
| `measure_name` | string | Measure name |
| `duration_code` | string | Duration code |
| `duration_name` | string | Duration name |
| `seasonal_code` | string | Seasonal adjustment code |
| `seasonal_name` | string | Seasonal adjustment name |
| `footnote_codes` | string | Footnote codes |

#### Example Request

```bash
GET /mp?year=2022,2023&api_key=YOUR_KEY
```

#### Example Response

```json
{
  "data": [
    {
      "series_id": "MLUMS00NN0001001",
      "year": 2023,
      "period": "M01",
      "value": 1523.0,
      "sector_code": "00",
      "sector_name": "Total private",
      "measure_code": "01",
      "measure_name": "Mass Layoff Events",
      "duration_code": "N",
      "duration_name": "Not applicable",
      "seasonal_code": "U",
      "seasonal_name": "Not Seasonally Adjusted",
      "footnote_codes": null
    }
  ],
  "total": 1,
  "limit": 100,
  "offset": 0,
  "has_more": false
}
```

---

### 8. Occupational Employment and Wages (OE)

Provides employment and wage estimates by occupation for various geographic areas.

| Property | Value |
|----------|-------|
| **Endpoint** | `GET /oe` |
| **Table** | `oe_data` |
| **HTTP Method** | GET |

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `year` | string | Filter by year (comma-separated for OR) |
| `year_gte` | integer | Year ≥ value |
| `year_lte` | integer | Year ≤ value |
| `year_gt` | integer | Year > value |
| `year_lt` | integer | Year < value |
| `series_id` | string | Filter by series ID |
| `area_code` | string | Filter by area code |
| `industry_code` | string | Filter by industry code |
| `occupation_code` | string | Filter by occupation code |
| `datatype_code` | string | Filter by data type code |
| `limit` | integer | Max results (default: 100, max: 1000) |
| `offset` | integer | Records to skip |
| `page` | integer | Page number |

#### Response Schema

| Field | Type | Description |
|-------|------|-------------|
| `series_id` | string | BLS series identifier |
| `year` | integer | Data year |
| `period` | string | Period identifier |
| `value` | decimal | Data value |
| `areatype_code` | string | Area type code |
| `areatype_name` | string | Area type name |
| `area_code` | string | Area code |
| `area_name` | string | Area name |
| `industry_code` | string | Industry code |
| `industry_name` | string | Industry name |
| `occupation_code` | string | Occupation code |
| `occupation_name` | string | Occupation name |
| `datatype_code` | string | Data type code |
| `datatype_name` | string | Data type name |
| `sector_code` | string | Sector code |
| `sector_name` | string | Sector name |
| `seasonal_code` | string | Seasonal adjustment code |
| `seasonal_name` | string | Seasonal adjustment name |
| `footnote_codes` | string | Footnote codes |

#### Example Request

```bash
GET /oe?occupation_code=15-1250&year=2023&api_key=YOUR_KEY
```

#### Example Response

```json
{
  "data": [
    {
      "series_id": "OEUN0000000000000151250",
      "year": 2023,
      "period": "A01",
      "value": 458520.0,
      "areatype_code": "N",
      "areatype_name": "National",
      "area_code": "00",
      "area_name": "United States",
      "industry_code": "000000",
      "industry_name": "Cross-industry",
      "occupation_code": "15-1250",
      "occupation_name": "Software Developers and Software Quality Assurance Analysts and Testers",
      "datatype_code": "01",
      "datatype_name": "Employment",
      "sector_code": "00",
      "sector_name": "Cross-industry",
      "seasonal_code": "U",
      "seasonal_name": "Not Seasonally Adjusted",
      "footnote_codes": null
    }
  ],
  "total": 1,
  "limit": 100,
  "offset": 0,
  "has_more": false
}
```

---

### 9. State and Area Employment (SA)

Provides employment data for states and metropolitan statistical areas.

| Property | Value |
|----------|-------|
| **Endpoint** | `GET /sa` |
| **Table** | `sa_data` |
| **HTTP Method** | GET |

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `year` | string | Filter by year (comma-separated for OR) |
| `year_gte` | integer | Year ≥ value |
| `year_lte` | integer | Year ≤ value |
| `year_gt` | integer | Year > value |
| `year_lt` | integer | Year < value |
| `series_id` | string | Filter by series ID |
| `state_code` | string | Filter by state code |
| `area_code` | string | Filter by area code |
| `industry_code` | string | Filter by industry code |
| `data_type_code` | string | Filter by data type code |
| `limit` | integer | Max results (default: 100, max: 1000) |
| `offset` | integer | Records to skip |
| `page` | integer | Page number |

#### Response Schema

| Field | Type | Description |
|-------|------|-------------|
| `series_id` | string | BLS series identifier |
| `year` | integer | Data year |
| `period` | string | Period identifier |
| `value` | decimal | Data value |
| `state_code` | string | State code |
| `state_name` | string | State name |
| `area_code` | string | Area code |
| `area_name` | string | Area name |
| `industry_code` | string | Industry code |
| `industry_name` | string | Industry name |
| `detail_code` | string | Detail code |
| `detail_name` | string | Detail name |
| `data_type_code` | string | Data type code |
| `data_type_name` | string | Data type name |
| `seasonal_code` | string | Seasonal adjustment code |
| `seasonal_name` | string | Seasonal adjustment name |
| `footnote_codes` | string | Footnote codes |

#### Example Request

```bash
GET /sa?state_code=06&industry_code=000000&api_key=YOUR_KEY
```

#### Example Response

```json
{
  "data": [
    {
      "series_id": "SMS06000000000000001",
      "year": 2023,
      "period": "M01",
      "value": 17521.9,
      "state_code": "06",
      "state_name": "California",
      "area_code": "00000",
      "area_name": "Statewide",
      "industry_code": "000000",
      "industry_name": "Total Nonfarm",
      "detail_code": "00",
      "detail_name": "Total Nonfarm",
      "data_type_code": "01",
      "data_type_name": "All Employees, In Thousands",
      "seasonal_code": "S",
      "seasonal_name": "Seasonally Adjusted",
      "footnote_codes": null
    }
  ],
  "total": 1,
  "limit": 100,
  "offset": 0,
  "has_more": false
}
```

---

### 10. State and Metropolitan Employment (SM)

Provides employment data for states and metropolitan areas by industry.

| Property | Value |
|----------|-------|
| **Endpoint** | `GET /sm` |
| **Table** | `sm_data` |
| **HTTP Method** | GET |

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `year` | string | Filter by year (comma-separated for OR) |
| `year_gte` | integer | Year ≥ value |
| `year_lte` | integer | Year ≤ value |
| `year_gt` | integer | Year > value |
| `year_lt` | integer | Year < value |
| `series_id` | string | Filter by series ID |
| `state_code` | string | Filter by state code |
| `area_code` | string | Filter by area code |
| `industry_code` | string | Filter by industry code |
| `supersector_code` | string | Filter by supersector code |
| `limit` | integer | Max results (default: 100, max: 1000) |
| `offset` | integer | Records to skip |
| `page` | integer | Page number |

#### Response Schema

| Field | Type | Description |
|-------|------|-------------|
| `series_id` | string | BLS series identifier |
| `year` | integer | Data year |
| `period` | string | Period identifier |
| `value` | decimal | Data value |
| `state_code` | string | State code |
| `state_name` | string | State name |
| `area_code` | string | Area code |
| `area_name` | string | Area name |
| `supersector_code` | string | Supersector code |
| `supersector_name` | string | Supersector name |
| `industry_code` | string | Industry code |
| `industry_name` | string | Industry name |
| `data_type_code` | string | Data type code |
| `data_type_name` | string | Data type name |
| `seasonal_code` | string | Seasonal adjustment code |
| `seasonal_name` | string | Seasonal adjustment name |
| `footnote_codes` | string | Footnote codes |

#### Example Request

```bash
GET /sm?state_code=06&supersector_code=10&api_key=YOUR_KEY
```

#### Example Response

```json
{
  "data": [
    {
      "series_id": "SMS06000001000000001",
      "year": 2023,
      "period": "M01",
      "value": 2845.2,
      "state_code": "06",
      "state_name": "California",
      "area_code": "00000",
      "area_name": "Statewide",
      "supersector_code": "10",
      "supersector_name": "Mining and Logging",
      "industry_code": "100000",
      "industry_name": "Mining and Logging",
      "data_type_code": "01",
      "data_type_name": "All Employees, In Thousands",
      "seasonal_code": "S",
      "seasonal_name": "Seasonally Adjusted",
      "footnote_codes": null
    }
  ],
  "total": 1,
  "limit": 100,
  "offset": 0,
  "has_more": false
}
```

---

## Error Handling

The API returns standard HTTP status codes:

| Status Code | Description |
|-------------|-------------|
| `200 OK` | Request successful |
| `401 Unauthorized` | Invalid or missing API key |
| `422 Unprocessable Entity` | Invalid query parameters |
| `500 Internal Server Error` | Server-side error |

### Error Response Format

```json
{
  "detail": "Error message describing the issue"
}
```

---

## Rate Limits

| Limit | Value |
|-------|-------|
| Maximum results per request | 1,000 records |
| Default results per request | 100 records |

---

## Support

For issues or questions, contact the development team or refer to the internal documentation.

---

## Appendix: State Codes Reference

Common state FIPS codes used in queries:

| Code | State |
|------|-------|
| `00` | National (all states) |
| `01` | Alabama |
| `06` | California |
| `17` | Illinois |
| `36` | New York |
| `48` | Texas |

For a complete list of state codes, refer to the [BLS State Code Reference](https://www.bls.gov/sae/additional-resources/state-and-area-code-lists.htm).
