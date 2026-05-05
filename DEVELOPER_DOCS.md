# BLS API Microservice - Developer Documentation

**Version:** 1.0.0  
**Last Updated:** March 2026

---

## Table of Contents

1. Overview
2. Base URL
3. Authentication
4. HTTP Methods
5. Request Format
6. Response Format
7. Pagination
8. Filtering
9. Endpoints
   - 1. Consumer Price Index (CPI)
   - 2. Current Employment Statistics (CE)
   - 3. Producer Price Index (PPI)
   - 4. Job Openings and Labor Turnover (JOLTS)
   - 5. Local Area Unemployment Statistics (LA)
   - 6. Employment Cost Index (CI)
   - 7. Major Sector Productivity (MP)
   - 8. Occupational Employment and Wages (OE)
   - 9. State and Area Employment (SA)
   - 10. State and Metropolitan Employment (SM)
10. Error Handling
11. Rate Limits
12. Database Schema

---

## Overview

The BLS API Microservice provides RESTful access to 10 Bureau of Labor Statistics datasets. All data is stored in a PostgreSQL database and exposed through standardized endpoints with consistent filtering, pagination, and response formats.

### Available Datasets

| Code | Dataset | Description | Table Name |
|------|---------|-------------|------------|
| CPI | Consumer Price Index | Measures price changes in goods and services | `cpi_data` |
| CE | Current Employment Statistics | Employment, hours, and earnings by industry | `ce_data` |
| PPI | Producer Price Index | Measures price changes from sellers' perspective | `ppi_data` |
| JT | Job Openings and Labor Turnover | Job openings, hires, and separations | `jt_data` |
| LA | Local Area Unemployment | Unemployment data for local areas | `la_data` |
| CI | Employment Cost Index | Changes in employer labor costs | `ci_data` |
| MP | Major Sector Productivity | Measures output efficiency per combined labor and capital inputs | `mp_data` |
| OE | Occupational Employment and Wages | Employment and wages by occupation | `oe_data` |
| SA | State and Area Employment | Employment by state and area | `sa_data` |
| SM | State and Metropolitan Employment | Employment for states and metros | `sm_data` |

---

## Base URL

```
https://bls-api-microservice-832081557693.europe-west2.run.app
```

All endpoints are relative to this base URL and use the `/api/v1/` prefix. For example, the CPI endpoint is at `/api/v1/cpi`.

---

## Authentication

### Method: API Key via Query Parameter

All requests require authentication via an API key passed as a query parameter.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `api_key` | string | Yes | Your API key for authentication |

### Request Example

```http
GET /api/v1/cpi?api_key=YOUR_API_KEY&limit=10
```

### cURL Example

```bash
curl -X GET "https://bls-api-microservice-832081557693.europe-west2.run.app/api/v1/cpi?api_key=YOUR_API_KEY&limit=10"
```

### Authentication Error Response

**Status Code:** `401 Unauthorized`

```json
{
  "error": {
    "type": "authentication_error",
    "message": "Invalid or missing API key",
    "status_code": 401
  }
}
```

---

## HTTP Methods

| Method | Usage | Supported |
|--------|-------|-----------|
| GET | Retrieve data | Yes |
| POST | Create data | No |
| PUT | Update data | No |
| PATCH | Partial update | No |
| DELETE | Remove data | No |

All endpoints are **read-only** and only support the `GET` method.

---

## Request Format

### Query String Parameters

All parameters are passed via the query string. There is no request body for any endpoint.

### Parameter Types

| Type | Format | Example |
|------|--------|---------|
| String | URL-encoded string | `area_code=0000` |
| Integer | Numeric value | `year=2023` |
| Comma-separated | Multiple values with OR logic | `year=2021,2022,2023` |

### Example Request with Multiple Parameters

```http
GET /api/v1/cpi?api_key=YOUR_API_KEY&year=2023&area_code=0000&limit=50&offset=0
```

---

## Response Format

All endpoints return a standardized paginated JSON response.

### Response Structure

```json
{
  "data": [
    { "... record 1 ..." },
    { "... record 2 ..." }
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
| `total` | integer | Total number of matching records (before pagination) |
| `limit` | integer | Maximum records returned in this response |
| `offset` | integer | Number of records skipped |
| `has_more` | boolean | Whether more records are available |

### HTTP Status Codes

| Status Code | Description |
|-------------|-------------|
| `200 OK` | Request successful |
| `401 Unauthorized` | Invalid or missing API key |
| `422 Unprocessable Entity` | Invalid query parameters |
| `500 Internal Server Error` | Server-side error |

---

## Pagination

### Pagination Parameters

| Parameter | Type | Default | Max | Description |
|-----------|------|---------|-----|-------------|
| `limit` | integer | 100 | 1000 | Maximum number of records to return |
| `offset` | integer | 0 | — | Number of records to skip |
| `page` | integer | — | — | Page number (1-based). Overrides `offset` if provided |

### Pagination Examples

#### Using Limit and Offset

```http
GET /api/v1/cpi?api_key=YOUR_API_KEY&limit=50&offset=100
```

Returns records 101-150.

#### Using Page Number

```http
GET /api/v1/cpi?api_key=YOUR_API_KEY&limit=50&page=3
```

Returns records 101-150 (page 3 with 50 records per page).

### Calculating Offset from Page

```
offset = (page - 1) * limit
```

---

## Filtering

### Year Filtering

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `year` | string | Exact year match (comma-separated for OR) | `year=2023` or `year=2021,2022,2023` |
| `year_gte` | integer | Year greater than or equal to | `year_gte=2020` |
| `year_lte` | integer | Year less than or equal to | `year_lte=2023` |
| `year_gt` | integer | Year greater than | `year_gt=2019` |
| `year_lt` | integer | Year less than | `year_lt=2024` |

### Period Filtering

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `period` | string | Filter by period identifier (comma-separated for OR) | `period=M01` or `period=M01,M02` |

### Multi-Value Filtering

Most filter parameters accept comma-separated values for OR logic:

```http
GET /api/v1/cpi?api_key=YOUR_API_KEY&area_code=0000,0100&item_code=SA0,SA0E
```

This returns records where:
- `area_code` is `0000` OR `0100`
- AND `item_code` is `SA0` OR `SA0E`

### Range Filtering Example

```http
GET /api/v1/cpi?api_key=YOUR_API_KEY&year_gte=2020&year_lte=2023
```

Returns records from years 2020, 2021, 2022, and 2023.

### Advanced Querying

All filter types can be combined in a single request. Understanding how they interact is key to building effective queries:

#### Filter Combination Rules

| Rule | Behavior | Example |
|------|----------|---------|
| **Different parameters** | AND logic — all must match | `year=2023&area_code=0000` → year is 2023 **AND** area is 0000 |
| **Same parameter, comma-separated** | OR logic — any value matches | `state_code=06,36,48` → state is 06 **OR** 36 **OR** 48 |
| **Range + exact** | AND logic — both apply | `year_gte=2020&year_lte=2023&seasonal_code=S` → years 2020–2023 **AND** seasonally adjusted |
| **Multiple OR filters** | AND between them, OR within each | `area_code=0000,0100&item_code=SA0,SA0E` → (area 0000 OR 0100) **AND** (item SA0 OR SA0E) |

#### Example 1: Year Range + Area + Seasonal Adjustment (CPI)

Get seasonally adjusted CPI data for the U.S. city average across a 4-year range:

```bash
curl -X GET "https://bls-api-microservice-832081557693.europe-west2.run.app/api/v1/cpi?api_key=YOUR_API_KEY&year_gte=2020&year_lte=2023&area_code=0000&seasonal_code=S&limit=25"
```

**Filters applied:** year 2020–2023 AND area `0000` AND seasonally adjusted.

#### Example 2: Multiple Years + Multiple States + Measure (LA)

Get unemployment rates for California, New York, and Texas in 2022 and 2023:

```bash
curl -X GET "https://bls-api-microservice-832081557693.europe-west2.run.app/api/v1/la?api_key=YOUR_API_KEY&year=2022,2023&state_code=06,36,48&measure_code=03&limit=50"
```

**Filters applied:** year (2022 OR 2023) AND state (06 OR 36 OR 48) AND measure `03` (unemployment rate).

#### Example 3: Year Range + Multiple Industries + Data Type + Pagination (CE)

Get seasonally adjusted employment levels for two industries from 2021 onward, page 2:

```bash
curl -X GET "https://bls-api-microservice-832081557693.europe-west2.run.app/api/v1/ce?api_key=YOUR_API_KEY&year_gte=2021&industry_code=05000000,06000000&datatype_code=01&seasonal_code=S&page=2&limit=50"
```

**Filters applied:** year ≥ 2021 AND industry (05000000 OR 06000000) AND datatype `01` AND seasonally adjusted, returning page 2.

#### Example 4: Year Range + Specific Periods + Data Element (JT)

Get Q1 job openings nationally for 2022 and 2023:

```bash
curl -X GET "https://bls-api-microservice-832081557693.europe-west2.run.app/api/v1/jt?api_key=YOUR_API_KEY&year_gte=2022&year_lte=2023&period=M01,M02,M03&state_code=00&dataelement_code=JO&limit=30"
```

**Filters applied:** year 2022–2023 AND period (M01 OR M02 OR M03) AND state `00` (national) AND data element `JO` (job openings).

#### Example 5: Specific Years + Multiple Sectors + Measure (MP)

Compare Total Factor Productivity for two sectors across 2022 and 2023:

```bash
curl -X GET "https://bls-api-microservice-832081557693.europe-west2.run.app/api/v1/mp?api_key=YOUR_API_KEY&year=2022,2023&sector_code=49,50&measure_code=01&seasonal_code=U&limit=20"
```

**Filters applied:** year (2022 OR 2023) AND sector (49 OR 50) AND measure `01` (Total Factor Productivity) AND not seasonally adjusted.

---

## Endpoints

---

### 1. Consumer Price Index (CPI)

Measures the average change over time in prices paid by urban consumers for a market basket of consumer goods and services.

#### Endpoint Details

| Property | Value |
|----------|-------|
| **Path** | `/api/v1/cpi` |
| **Method** | `GET` |
| **Table** | `cpi_data` |
| **Description** | Consumer Price Index data |

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `api_key` | string | **Required.** Your API key |
| `year` | string | Filter by year (comma-separated for OR) |
| `year_gte` | integer | Year ≥ value |
| `year_lte` | integer | Year ≤ value |
| `year_gt` | integer | Year > value |
| `year_lt` | integer | Year < value |
| `period` | string | Filter by period identifier (comma-separated for OR) |
| `series_id` | string | Filter by series ID (comma-separated for OR) |
| `area_code` | string | Filter by geographic area code (comma-separated for OR) |
| `item_code` | string | Filter by item category code (comma-separated for OR) |
| `seasonal_code` | string | Filter by seasonal adjustment code (comma-separated for OR) |
| `limit` | integer | Max results (default: 100, max: 1000) |
| `offset` | integer | Records to skip |
| `page` | integer | Page number (1-based) |

#### Response Schema

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Unique record identifier |
| `series_id` | string | BLS series identifier |
| `year` | integer | Data year |
| `period` | string | Period identifier (e.g., "M01", "M02") |
| `period_name` | string | Period name (e.g., "January", "February") |
| `value` | decimal | CPI index value |
| `area_code` | string | Geographic area code |
| `area_name` | string | Geographic area name |
| `item_code` | string | Item category code |
| `item_name` | string | Item category name |
| `seasonal_code` | string | Seasonal adjustment code (S/U) |
| `seasonal_text` | string | Seasonal adjustment description |

#### Request Example

```http
GET /api/v1/cpi?api_key=YOUR_API_KEY&year=2023&area_code=0000&limit=10
```

#### cURL Example

```bash
curl -X GET "https://bls-api-microservice-832081557693.europe-west2.run.app/api/v1/cpi?api_key=YOUR_API_KEY&year=2023&area_code=0000&limit=10"
```

#### Response Example

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
    },
    {
      "id": 2,
      "series_id": "CUSR0000SA0",
      "year": 2023,
      "period": "M02",
      "period_name": "February",
      "value": 300.840,
      "area_code": "0000",
      "area_name": "U.S. city average",
      "item_code": "SA0",
      "item_name": "All items",
      "seasonal_code": "S",
      "seasonal_text": "Seasonally Adjusted"
    }
  ],
  "total": 12,
  "limit": 10,
  "offset": 0,
  "has_more": true
}
```

---

### 2. Current Employment Statistics (CE)

Provides national data on employment, hours, and earnings by industry.

#### Endpoint Details

| Property | Value |
|----------|-------|
| **Path** | `/api/v1/ce` |
| **Method** | `GET` |
| **Table** | `ce_data` |
| **Description** | Current Employment Statistics data |

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `api_key` | string | **Required.** Your API key |
| `year` | string | Filter by year (comma-separated for OR) |
| `year_gte` | integer | Year ≥ value |
| `year_lte` | integer | Year ≤ value |
| `year_gt` | integer | Year > value |
| `year_lt` | integer | Year < value |
| `period` | string | Filter by period identifier (comma-separated for OR) |
| `series_id` | string | Filter by series ID (comma-separated for OR) |
| `industry_code` | string | Filter by industry code (comma-separated for OR) |
| `supersector_code` | string | Filter by supersector code (comma-separated for OR) |
| `datatype_code` | string | Filter by data type code (comma-separated for OR) |
| `seasonal_code` | string | Filter by seasonal adjustment code (comma-separated for OR) |
| `limit` | integer | Max results (default: 100, max: 1000) |
| `offset` | integer | Records to skip |
| `page` | integer | Page number (1-based) |

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
| `footnote_codes` | string | Footnote codes (nullable) |

#### Request Example

```http
GET /api/v1/ce?api_key=YOUR_API_KEY&year=2023&industry_code=05000000&limit=10
```

#### cURL Example

```bash
curl -X GET "https://bls-api-microservice-832081557693.europe-west2.run.app/api/v1/ce?api_key=YOUR_API_KEY&year=2023&industry_code=05000000&limit=10"
```

#### Response Example

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
  "limit": 10,
  "offset": 0,
  "has_more": false
}
```

---

### 3. Producer Price Index (PPI)

Measures average changes in selling prices received by domestic producers for their output.

#### Endpoint Details

| Property | Value |
|----------|-------|
| **Path** | `/api/v1/ppi` |
| **Method** | `GET` |
| **Table** | `ppi_data` |
| **Description** | Producer Price Index data |

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `api_key` | string | **Required.** Your API key |
| `year` | string | Filter by year (comma-separated for OR) |
| `year_gte` | integer | Year ≥ value |
| `year_lte` | integer | Year ≤ value |
| `year_gt` | integer | Year > value |
| `year_lt` | integer | Year < value |
| `period` | string | Filter by period identifier (comma-separated for OR) |
| `series_id` | string | Filter by series ID (comma-separated for OR) |
| `sector_code` | string | Filter by sector code (comma-separated for OR) |
| `class_code` | string | Filter by class code (comma-separated for OR) |
| `measure_code` | string | Filter by measure code (comma-separated for OR) |
| `duration_code` | string | Filter by duration code (comma-separated for OR) |
| `seasonal_code` | string | Filter by seasonal adjustment code (comma-separated for OR) |
| `limit` | integer | Max results (default: 100, max: 1000) |
| `offset` | integer | Records to skip |
| `page` | integer | Page number (1-based) |

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
| `duration_code` | string | Duration code (nullable) |
| `duration_name` | string | Duration name (nullable) |
| `seasonal_code` | string | Seasonal adjustment code |
| `seasonal_name` | string | Seasonal adjustment name |
| `footnote_codes` | string | Footnote codes (nullable) |

#### Request Example

```http
GET /api/v1/ppi?api_key=YOUR_API_KEY&year_gte=2020&year_lte=2023&limit=20
```

#### cURL Example

```bash
curl -X GET "https://bls-api-microservice-832081557693.europe-west2.run.app/api/v1/ppi?api_key=YOUR_API_KEY&year_gte=2020&year_lte=2023&limit=20"
```

#### Response Example

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
  "total": 48,
  "limit": 20,
  "offset": 0,
  "has_more": true
}
```

---

### 4. Job Openings and Labor Turnover (JOLTS)

Measures job vacancies, hires, and separations to gauge labor market dynamics.

#### Endpoint Details

| Property | Value |
|----------|-------|
| **Path** | `/api/v1/jt` |
| **Method** | `GET` |
| **Table** | `jt_data` |
| **Description** | Job Openings and Labor Turnover data |

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `api_key` | string | **Required.** Your API key |
| `year` | string | Filter by year (comma-separated for OR) |
| `year_gte` | integer | Year ≥ value |
| `year_lte` | integer | Year ≤ value |
| `year_gt` | integer | Year > value |
| `year_lt` | integer | Year < value |
| `period` | string | Filter by period identifier (comma-separated for OR) |
| `series_id` | string | Filter by series ID (comma-separated for OR) |
| `state_code` | string | Filter by state code (comma-separated for OR) |
| `industry_code` | string | Filter by industry code (comma-separated for OR) |
| `area_code` | string | Filter by area code (comma-separated for OR) |
| `dataelement_code` | string | Filter by data element code (comma-separated for OR) |
| `sizeclass_code` | string | Filter by establishment size class code (comma-separated for OR) |
| `ratelevel_code` | string | Filter by rate/level indicator code (comma-separated for OR) |
| `seasonal_code` | string | Filter by seasonal adjustment code (comma-separated for OR) |
| `limit` | integer | Max results (default: 100, max: 1000) |
| `offset` | integer | Records to skip |
| `page` | integer | Page number (1-based) |

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
| `footnote_codes` | string | Footnote codes (nullable) |

#### Request Example

```http
GET /api/v1/jt?api_key=YOUR_API_KEY&state_code=00&year=2023&limit=15
```

#### cURL Example

```bash
curl -X GET "https://bls-api-microservice-832081557693.europe-west2.run.app/api/v1/jt?api_key=YOUR_API_KEY&state_code=00&year=2023&limit=15"
```

#### Response Example

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
  "total": 12,
  "limit": 15,
  "offset": 0,
  "has_more": false
}
```

---

### 5. Local Area Unemployment Statistics (LA)

Provides employment and unemployment data for states, counties, and metropolitan areas.

#### Endpoint Details

| Property | Value |
|----------|-------|
| **Path** | `/api/v1/la` |
| **Method** | `GET` |
| **Table** | `la_data` |
| **Description** | Local Area Unemployment Statistics data |

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `api_key` | string | **Required.** Your API key |
| `year` | string | Filter by year (comma-separated for OR) |
| `year_gte` | integer | Year ≥ value |
| `year_lte` | integer | Year ≤ value |
| `year_gt` | integer | Year > value |
| `year_lt` | integer | Year < value |
| `period` | string | Filter by period identifier (comma-separated for OR) |
| `series_id` | string | Filter by series ID (comma-separated for OR) |
| `state_code` | string | Filter by state code (comma-separated for OR) |
| `area_code` | string | Filter by area code (comma-separated for OR) |
| `area_type_code` | string | Filter by area type code (comma-separated for OR) |
| `measure_code` | string | Filter by measure code (comma-separated for OR) |
| `seasonal_code` | string | Filter by seasonal adjustment code (comma-separated for OR) |
| `limit` | integer | Max results (default: 100, max: 1000) |
| `offset` | integer | Records to skip |
| `page` | integer | Page number (1-based) |

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
| `footnote_codes` | string | Footnote codes (nullable) |

#### Request Example

```http
GET /api/v1/la?api_key=YOUR_API_KEY&state_code=06&year=2023&limit=10
```

#### cURL Example

```bash
curl -X GET "https://bls-api-microservice-832081557693.europe-west2.run.app/api/v1/la?api_key=YOUR_API_KEY&state_code=06&year=2023&limit=10"
```

#### Response Example

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
  "total": 12,
  "limit": 10,
  "offset": 0,
  "has_more": true
}
```

---

### 6. Employment Cost Index (CI)

Measures changes in the costs of labor compensation over time.

#### Endpoint Details

| Property | Value |
|----------|-------|
| **Path** | `/api/v1/ci` |
| **Method** | `GET` |
| **Table** | `ci_data` |
| **Description** | Employment Cost Index data |

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `api_key` | string | **Required.** Your API key |
| `year` | string | Filter by year (comma-separated for OR) |
| `year_gte` | integer | Year ≥ value |
| `year_lte` | integer | Year ≤ value |
| `year_gt` | integer | Year > value |
| `year_lt` | integer | Year < value |
| `period` | string | Filter by period identifier (comma-separated for OR) |
| `series_id` | string | Filter by series ID (comma-separated for OR) |
| `industry_code` | string | Filter by industry code (comma-separated for OR) |
| `occupation_code` | string | Filter by occupation code (comma-separated for OR) |
| `area_code` | string | Filter by area code (comma-separated for OR) |
| `owner_code` | string | Filter by owner code (comma-separated for OR) |
| `estimate_code` | string | Filter by estimate code (comma-separated for OR) |
| `periodicity_code` | string | Filter by periodicity code (comma-separated for OR) |
| `seasonal_code` | string | Filter by seasonal adjustment code (comma-separated for OR) |
| `limit` | integer | Max results (default: 100, max: 1000) |
| `offset` | integer | Records to skip |
| `page` | integer | Page number (1-based) |

#### Response Schema

| Field | Type | Description |
|-------|------|-------------|
| `series_id` | string | BLS series identifier |
| `year` | integer | Data year |
| `period` | string | Period identifier (e.g., "Q01", "Q02") |
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
| `footnote_codes` | string | Footnote codes (nullable) |

#### Request Example

```http
GET /api/v1/ci?api_key=YOUR_API_KEY&year=2023&industry_code=000000&limit=10
```

#### cURL Example

```bash
curl -X GET "https://bls-api-microservice-832081557693.europe-west2.run.app/api/v1/ci?api_key=YOUR_API_KEY&year=2023&industry_code=000000&limit=10"
```

#### Response Example

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
  "total": 4,
  "limit": 10,
  "offset": 0,
  "has_more": false
}
```

---

### 7. Major Sector Productivity (MP)

Measures output efficiency per combined labor and capital inputs across major economic sectors.

#### Endpoint Details

| Property | Value |
|----------|-------|
| **Path** | `/api/v1/mp` |
| **Method** | `GET` |
| **Table** | `mp_data` |
| **Description** | Major Sector Productivity data |

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `api_key` | string | **Required.** Your API key |
| `year` | string | Filter by year (comma-separated for OR) |
| `year_gte` | integer | Year ≥ value |
| `year_lte` | integer | Year ≤ value |
| `year_gt` | integer | Year > value |
| `year_lt` | integer | Year < value |
| `period` | string | Filter by period identifier (comma-separated for OR) |
| `series_id` | string | Filter by series ID (comma-separated for OR) |
| `sector_code` | string | Filter by sector code (comma-separated for OR) |
| `measure_code` | string | Filter by measure code (comma-separated for OR) |
| `duration_code` | string | Filter by duration code (comma-separated for OR) |
| `seasonal_code` | string | Filter by seasonal adjustment code (comma-separated for OR) |
| `limit` | integer | Max results (default: 100, max: 1000) |
| `offset` | integer | Records to skip |
| `page` | integer | Page number (1-based) |

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
| `footnote_codes` | string | Footnote codes (nullable) |

#### Request Example

```http
GET /api/v1/mp?api_key=YOUR_API_KEY&year=2022,2023&limit=10
```

#### cURL Example

```bash
curl -X GET "https://bls-api-microservice-832081557693.europe-west2.run.app/api/v1/mp?api_key=YOUR_API_KEY&year=2022,2023&limit=10"
```

#### Response Example

```json
{
  "data": [
    {
      "series_id": "MPU491001",
      "year": 2023,
      "period": "A01",
      "value": 102.5,
      "sector_code": "49",
      "sector_name": "Transportation and warehousing",
      "measure_code": "01",
      "measure_name": "Total Factor Productivity",
      "duration_code": "01",
      "duration_name": "Annual",
      "seasonal_code": "U",
      "seasonal_name": "Not Seasonally Adjusted",
      "footnote_codes": null
    }
  ],
  "total": 24,
  "limit": 10,
  "offset": 0,
  "has_more": true
}
```

---

### 8. Occupational Employment and Wages (OE)

Provides employment and wage estimates by occupation for various geographic areas.

#### Endpoint Details

| Property | Value |
|----------|-------|
| **Path** | `/api/v1/oe` |
| **Method** | `GET` |
| **Table** | `oe_data` |
| **Description** | Occupational Employment and Wages data |

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `api_key` | string | **Required.** Your API key |
| `year` | string | Filter by year (comma-separated for OR) |
| `year_gte` | integer | Year ≥ value |
| `year_lte` | integer | Year ≤ value |
| `year_gt` | integer | Year > value |
| `year_lt` | integer | Year < value |
| `period` | string | Filter by period identifier (comma-separated for OR) |
| `series_id` | string | Filter by series ID (comma-separated for OR) |
| `area_code` | string | Filter by area code (comma-separated for OR) |
| `industry_code` | string | Filter by industry code (comma-separated for OR) |
| `occupation_code` | string | Filter by occupation code (comma-separated for OR) |
| `datatype_code` | string | Filter by data type code (comma-separated for OR) |
| `sector_code` | string | Filter by sector code (comma-separated for OR) |
| `areatype_code` | string | Filter by area type code (comma-separated for OR) |
| `seasonal_code` | string | Filter by seasonal adjustment code (comma-separated for OR) |
| `limit` | integer | Max results (default: 100, max: 1000) |
| `offset` | integer | Records to skip |
| `page` | integer | Page number (1-based) |

#### Response Schema

| Field | Type | Description |
|-------|------|-------------|
| `series_id` | string | BLS series identifier |
| `year` | integer | Data year |
| `period` | string | Period identifier (e.g., "A01" for annual) |
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
| `footnote_codes` | string | Footnote codes (nullable) |

#### Request Example

```http
GET /api/v1/oe?api_key=YOUR_API_KEY&occupation_code=439199&year=2024&limit=10
```

#### cURL Example

```bash
curl -X GET "https://bls-api-microservice-832081557693.europe-west2.run.app/api/v1/oe?api_key=YOUR_API_KEY&occupation_code=439199&year=2024&limit=10"
```

#### Response Example

```json
{
  "data": [
    {
      "series_id": "OEUN0000000000000439199",
      "year": 2024,
      "period": "A01",
      "value": 125000.0,
      "areatype_code": "N",
      "areatype_name": "National",
      "area_code": "00",
      "area_name": "United States",
      "industry_code": "000000",
      "industry_name": "Cross-industry",
      "occupation_code": "439199",
      "occupation_name": "Other Office and Administrative Support Workers",
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
  "limit": 10,
  "offset": 0,
  "has_more": false
}
```

---

### 9. State and Area Employment (SA)

Provides employment data for states and metropolitan statistical areas.

#### Endpoint Details

| Property | Value |
|----------|-------|
| **Path** | `/api/v1/sa` |
| **Method** | `GET` |
| **Table** | `sa_data` |
| **Description** | State and Area Employment data |

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `api_key` | string | **Required.** Your API key |
| `year` | string | Filter by year (comma-separated for OR) |
| `year_gte` | integer | Year ≥ value |
| `year_lte` | integer | Year ≤ value |
| `year_gt` | integer | Year > value |
| `year_lt` | integer | Year < value |
| `period` | string | Filter by period identifier (comma-separated for OR) |
| `series_id` | string | Filter by series ID (comma-separated for OR) |
| `state_code` | string | Filter by state code (comma-separated for OR) |
| `area_code` | string | Filter by area code (comma-separated for OR) |
| `industry_code` | string | Filter by industry code (comma-separated for OR) |
| `data_type_code` | string | Filter by data type code (comma-separated for OR) |
| `detail_code` | string | Filter by detail code (comma-separated for OR) |
| `seasonal_code` | string | Filter by seasonal adjustment code (comma-separated for OR) |
| `limit` | integer | Max results (default: 100, max: 1000) |
| `offset` | integer | Records to skip |
| `page` | integer | Page number (1-based) |

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
| `footnote_codes` | string | Footnote codes (nullable) |

#### Request Example

```http
GET /api/v1/sa?api_key=YOUR_API_KEY&state_code=06&industry_code=000000&limit=10
```

#### cURL Example

```bash
curl -X GET "https://bls-api-microservice-832081557693.europe-west2.run.app/api/v1/sa?api_key=YOUR_API_KEY&state_code=06&industry_code=000000&limit=10"
```

#### Response Example

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
  "total": 12,
  "limit": 10,
  "offset": 0,
  "has_more": true
}
```

---

### 10. State and Metropolitan Employment (SM)

Provides employment data for states and metropolitan areas by industry.

#### Endpoint Details

| Property | Value |
|----------|-------|
| **Path** | `/api/v1/sm` |
| **Method** | `GET` |
| **Table** | `sm_data` |
| **Description** | State and Metropolitan Employment data |

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `api_key` | string | **Required.** Your API key |
| `year` | string | Filter by year (comma-separated for OR) |
| `year_gte` | integer | Year ≥ value |
| `year_lte` | integer | Year ≤ value |
| `year_gt` | integer | Year > value |
| `year_lt` | integer | Year < value |
| `period` | string | Filter by period identifier (comma-separated for OR) |
| `series_id` | string | Filter by series ID (comma-separated for OR) |
| `state_code` | string | Filter by state code (comma-separated for OR) |
| `area_code` | string | Filter by area code (comma-separated for OR) |
| `industry_code` | string | Filter by industry code (comma-separated for OR) |
| `supersector_code` | string | Filter by supersector code (comma-separated for OR) |
| `data_type_code` | string | Filter by data type code (comma-separated for OR) |
| `seasonal_code` | string | Filter by seasonal adjustment code (comma-separated for OR) |
| `limit` | integer | Max results (default: 100, max: 1000) |
| `offset` | integer | Records to skip |
| `page` | integer | Page number (1-based) |

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
| `footnote_codes` | string | Footnote codes (nullable) |

#### Request Example

```http
GET /api/v1/sm?api_key=YOUR_API_KEY&state_code=06&supersector_code=10&limit=10
```

#### cURL Example

```bash
curl -X GET "https://bls-api-microservice-832081557693.europe-west2.run.app/api/v1/sm?api_key=YOUR_API_KEY&state_code=06&supersector_code=10&limit=10"
```

#### Response Example

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
  "total": 12,
  "limit": 10,
  "offset": 0,
  "has_more": true
}
```

---

## Error Handling

### HTTP Status Codes

| Status Code | Description | Cause |
|-------------|-------------|-------|
| `200 OK` | Request successful | Valid request with proper authentication |
| `401 Unauthorized` | Authentication failed | Missing or invalid API key |
| `422 Unprocessable Entity` | Validation error | Invalid query parameter value |
| `500 Internal Server Error` | Server error | Unexpected server-side error |

### Error Response Format

All errors return a standardized JSON object with an `error` field:

```json
{
  "error": {
    "type": "error_type",
    "message": "Error message describing the issue",
    "status_code": 401
  }
}
```

### Common Errors

#### Missing API Key

**Status:** `401 Unauthorized`

```json
{
  "error": {
    "type": "authentication_error",
    "message": "Invalid or missing API key",
    "status_code": 401
  }
}
```

#### Invalid Parameter Value

**Status:** `422 Unprocessable Entity`

```json
{
  "detail": [
    {
      "loc": ["query", "limit"],
      "msg": "ensure this value is less than or equal to 1000",
      "type": "value_error.number.not_le"
    }
  ]
}
```

#### Invalid Year Format

**Status:** `422 Unprocessable Entity`

```json
{
  "detail": [
    {
      "loc": ["query", "year_gte"],
      "msg": "value is not a valid integer",
      "type": "type_error.integer"
    }
  ]
}
```

---

## Rate Limits

| Limit | Value |
|-------|-------|
| Maximum results per request | 1,000 records |
| Default results per request | 100 records |
| Maximum limit value | 1,000 |

---

## Database Schema

### Table: `cpi_data`

| Column | Type | Constraints |
|--------|------|-------------|
| `id` | INTEGER | PRIMARY KEY |
| `series_id` | VARCHAR(20) | |
| `year` | INTEGER | |
| `period` | VARCHAR(5) | |
| `period_name` | VARCHAR(50) | |
| `value` | NUMERIC(15,4) | |
| `area_code` | VARCHAR(10) | |
| `area_name` | VARCHAR(255) | |
| `item_code` | VARCHAR(20) | |
| `item_name` | VARCHAR(500) | |
| `seasonal_code` | VARCHAR(1) | |
| `seasonal_text` | VARCHAR(50) | |

### Table: `ce_data`

| Column | Type | Constraints |
|--------|------|-------------|
| `series_id` | VARCHAR(20) | PRIMARY KEY |
| `year` | INTEGER | PRIMARY KEY |
| `period` | VARCHAR(3) | PRIMARY KEY |
| `period_name` | VARCHAR(20) | |
| `value` | NUMERIC(14,2) | |
| `supersector_code` | VARCHAR(5) | |
| `supersector_name` | VARCHAR(100) | |
| `industry_code` | VARCHAR(10) | |
| `industry_name` | VARCHAR(200) | |
| `datatype_code` | VARCHAR(5) | |
| `datatype_name` | VARCHAR(100) | |
| `seasonal_code` | VARCHAR(1) | |
| `seasonal_name` | VARCHAR(30) | |
| `footnote_codes` | VARCHAR(10) | |

### Table: `ppi_data`

| Column | Type | Constraints |
|--------|------|-------------|
| `series_id` | VARCHAR(20) | PRIMARY KEY |
| `year` | INTEGER | PRIMARY KEY |
| `period` | VARCHAR(3) | PRIMARY KEY |
| `period_name` | VARCHAR(20) | |
| `value` | NUMERIC(12,4) | |
| `measure_code` | VARCHAR(2) | |
| `measure_name` | VARCHAR(100) | |
| `sector_code` | VARCHAR(10) | |
| `sector_name` | VARCHAR(200) | |
| `class_code` | VARCHAR(10) | |
| `class_name` | VARCHAR(200) | |
| `duration_code` | VARCHAR(2) | |
| `duration_name` | VARCHAR(50) | |
| `seasonal_code` | VARCHAR(1) | |
| `seasonal_name` | VARCHAR(20) | |
| `footnote_codes` | VARCHAR(10) | |

### Table: `jt_data`

| Column | Type | Constraints |
|--------|------|-------------|
| `series_id` | VARCHAR(22) | PRIMARY KEY |
| `year` | INTEGER | PRIMARY KEY |
| `period` | VARCHAR(3) | PRIMARY KEY |
| `value` | NUMERIC(14,2) | |
| `industry_code` | VARCHAR(10) | |
| `industry_name` | VARCHAR(200) | |
| `state_code` | VARCHAR(10) | |
| `state_name` | VARCHAR(100) | |
| `area_code` | VARCHAR(10) | |
| `area_name` | VARCHAR(200) | |
| `sizeclass_code` | VARCHAR(10) | |
| `sizeclass_name` | VARCHAR(100) | |
| `dataelement_code` | VARCHAR(10) | |
| `dataelement_name` | VARCHAR(100) | |
| `ratelevel_code` | VARCHAR(10) | |
| `ratelevel_name` | VARCHAR(50) | |
| `seasonal_code` | VARCHAR(10) | |
| `seasonal_name` | VARCHAR(30) | |
| `footnote_codes` | VARCHAR(10) | |

### Table: `la_data`

| Column | Type | Constraints |
|--------|------|-------------|
| `series_id` | VARCHAR(20) | PRIMARY KEY |
| `year` | INTEGER | PRIMARY KEY |
| `period` | VARCHAR(3) | PRIMARY KEY |
| `value` | NUMERIC(14,2) | |
| `area_type_code` | VARCHAR(2) | |
| `area_type_name` | VARCHAR(100) | |
| `area_code` | VARCHAR(20) | |
| `area_name` | VARCHAR(200) | |
| `measure_code` | VARCHAR(2) | |
| `measure_name` | VARCHAR(100) | |
| `seasonal_code` | VARCHAR(1) | |
| `seasonal_name` | VARCHAR(30) | |
| `state_code` | VARCHAR(2) | |
| `state_name` | VARCHAR(100) | |
| `footnote_codes` | VARCHAR(10) | |

### Table: `ci_data`

| Column | Type | Constraints |
|--------|------|-------------|
| `series_id` | VARCHAR(20) | PRIMARY KEY |
| `year` | INTEGER | PRIMARY KEY |
| `period` | VARCHAR(3) | PRIMARY KEY |
| `value` | NUMERIC(14,2) | |
| `owner_code` | VARCHAR(10) | |
| `owner_name` | VARCHAR(100) | |
| `industry_code` | VARCHAR(10) | |
| `industry_name` | VARCHAR(200) | |
| `occupation_code` | VARCHAR(10) | |
| `occupation_name` | VARCHAR(200) | |
| `area_code` | VARCHAR(10) | |
| `area_name` | VARCHAR(200) | |
| `estimate_code` | VARCHAR(10) | |
| `estimate_name` | VARCHAR(200) | |
| `periodicity_code` | VARCHAR(10) | |
| `periodicity_name` | VARCHAR(50) | |
| `seasonal_code` | VARCHAR(10) | |
| `seasonal_name` | VARCHAR(30) | |
| `footnote_codes` | VARCHAR(10) | |

### Table: `mp_data`

| Column | Type | Constraints |
|--------|------|-------------|
| `series_id` | VARCHAR(20) | PRIMARY KEY |
| `year` | INTEGER | PRIMARY KEY |
| `period` | VARCHAR(3) | PRIMARY KEY |
| `value` | NUMERIC(14,2) | |
| `sector_code` | VARCHAR(10) | |
| `sector_name` | VARCHAR(200) | |
| `measure_code` | VARCHAR(10) | |
| `measure_name` | VARCHAR(100) | |
| `duration_code` | VARCHAR(10) | |
| `duration_name` | VARCHAR(100) | |
| `seasonal_code` | VARCHAR(10) | |
| `seasonal_name` | VARCHAR(30) | |
| `footnote_codes` | VARCHAR(10) | |

### Table: `oe_data`

| Column | Type | Constraints |
|--------|------|-------------|
| `series_id` | VARCHAR(35) | PRIMARY KEY |
| `year` | INTEGER | PRIMARY KEY |
| `period` | VARCHAR(10) | PRIMARY KEY |
| `value` | NUMERIC(14,2) | |
| `areatype_code` | VARCHAR(10) | |
| `areatype_name` | VARCHAR(100) | |
| `area_code` | VARCHAR(20) | |
| `area_name` | VARCHAR(200) | |
| `industry_code` | VARCHAR(20) | |
| `industry_name` | VARCHAR(200) | |
| `occupation_code` | VARCHAR(20) | |
| `occupation_name` | VARCHAR(200) | |
| `datatype_code` | VARCHAR(10) | |
| `datatype_name` | VARCHAR(100) | |
| `sector_code` | VARCHAR(20) | |
| `sector_name` | VARCHAR(100) | |
| `seasonal_code` | VARCHAR(10) | |
| `seasonal_name` | VARCHAR(30) | |
| `footnote_codes` | VARCHAR(250) | |

### Table: `sa_data`

| Column | Type | Constraints |
|--------|------|-------------|
| `series_id` | VARCHAR(20) | PRIMARY KEY |
| `year` | INTEGER | PRIMARY KEY |
| `period` | VARCHAR(3) | PRIMARY KEY |
| `value` | NUMERIC(14,2) | |
| `state_code` | VARCHAR(2) | |
| `state_name` | VARCHAR(100) | |
| `area_code` | VARCHAR(10) | |
| `area_name` | VARCHAR(200) | |
| `industry_code` | VARCHAR(10) | |
| `industry_name` | VARCHAR(200) | |
| `detail_code` | VARCHAR(2) | |
| `detail_name` | VARCHAR(100) | |
| `data_type_code` | VARCHAR(2) | |
| `data_type_name` | VARCHAR(100) | |
| `seasonal_code` | VARCHAR(1) | |
| `seasonal_name` | VARCHAR(30) | |
| `footnote_codes` | VARCHAR(10) | |

### Table: `sm_data`

| Column | Type | Constraints |
|--------|------|-------------|
| `series_id` | VARCHAR(22) | PRIMARY KEY |
| `year` | INTEGER | PRIMARY KEY |
| `period` | VARCHAR(3) | PRIMARY KEY |
| `value` | NUMERIC(14,2) | |
| `state_code` | VARCHAR(2) | |
| `state_name` | VARCHAR(100) | |
| `area_code` | VARCHAR(10) | |
| `area_name` | VARCHAR(200) | |
| `supersector_code` | VARCHAR(2) | |
| `supersector_name` | VARCHAR(100) | |
| `industry_code` | VARCHAR(10) | |
| `industry_name` | VARCHAR(200) | |
| `data_type_code` | VARCHAR(2) | |
| `data_type_name` | VARCHAR(100) | |
| `seasonal_code` | VARCHAR(1) | |
| `seasonal_name` | VARCHAR(30) | |
| `footnote_codes` | VARCHAR(10) | |

---

## Appendix: State Codes Reference

Common state FIPS codes used in queries:

| Code | State |
|------|-------|
| `00` | National (all states) |
| `01` | Alabama |
| `02` | Alaska |
| `04` | Arizona |
| `05` | Arkansas |
| `06` | California |
| `08` | Colorado |
| `09` | Connecticut |
| `10` | Delaware |
| `11` | District of Columbia |
| `12` | Florida |
| `13` | Georgia |
| `15` | Hawaii |
| `16` | Idaho |
| `17` | Illinois |
| `18` | Indiana |
| `19` | Iowa |
| `20` | Kansas |
| `21` | Kentucky |
| `22` | Louisiana |
| `23` | Maine |
| `24` | Maryland |
| `25` | Massachusetts |
| `26` | Michigan |
| `27` | Minnesota |
| `28` | Mississippi |
| `29` | Missouri |
| `30` | Montana |
| `31` | Nebraska |
| `32` | Nevada |
| `33` | New Hampshire |
| `34` | New Jersey |
| `35` | New Mexico |
| `36` | New York |
| `37` | North Carolina |
| `38` | North Dakota |
| `39` | Ohio |
| `40` | Oklahoma |
| `41` | Oregon |
| `42` | Pennsylvania |
| `44` | Rhode Island |
| `45` | South Carolina |
| `46` | South Dakota |
| `47` | Tennessee |
| `48` | Texas |
| `49` | Utah |
| `50` | Vermont |
| `51` | Virginia |
| `53` | Washington |
| `54` | West Virginia |
| `55` | Wisconsin |
| `56` | Wyoming |

For a complete list of state and area codes, refer to the [BLS State Code Reference](https://www.bls.gov/sae/additional-resources/state-and-area-code-lists.htm).
