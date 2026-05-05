# BLS API Microservice

A RESTful API microservice that provides programmatic access to 10 Bureau of Labor Statistics (BLS) datasets stored in a PostgreSQL database.

## Features

- **10 BLS Datasets**: CPI, CE, PPI, JOLTS, LA, CI, MP, OE, SA, SM
- **API Key Authentication**: Secure access with API key validation
- **Pagination**: Built-in support for limit/offset and page-based pagination
- **Flexible Filtering**: Year range filters, multi-value filters with OR logic
- **FastAPI Framework**: High performance, automatic OpenAPI documentation
- **Docker Ready**: Containerized for easy deployment

## Datasets

| Code | Dataset | Description |
|------|---------|-------------|
| CPI | Consumer Price Index | Measures price changes in goods and services |
| CE | Current Employment Statistics | Employment, hours, and earnings by industry |
| PPI | Producer Price Index | Measures price changes from sellers' perspective |
| JT | Job Openings and Labor Turnover | Job openings, hires, and separations |
| LA | Local Area Unemployment | Unemployment data for local areas |
| CI | Employment Cost Index | Changes in employer labor costs |
| MP | Major Sector Productivity | Measures output efficiency per combined labor and capital inputs |
| OE | Occupational Employment and Wages | Employment and wages by occupation |
| SA | State and Area Employment | Employment by state and area |
| SM | State and Metropolitan Employment | Employment for states and metros |

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL database
- Docker (optional)

### Environment Variables

Create a `.env` file based on `.env.example`:

```env
DATABASE_URL=postgresql://user:password@host:port/database
APP_NAME=BLS Economic Data API
APP_DEBUG=false
LOG_LEVEL=INFO
API_KEYS=your-api-key-here
```

### Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload
```

### Run with Docker

```bash
# Build and run
docker-compose up --build
```

## API Usage

### Base URL

```
https://bls-api-microservice-832081557693.europe-west2.run.app
```

### Authentication

All requests require an API key:

```bash
curl "https://bls-api-microservice-832081557693.europe-west2.run.app/api/v1/cpi?api_key=YOUR_API_KEY"
```

### Example Requests

```bash
# Get CPI data for 2023
curl "https://bls-api-microservice-832081557693.europe-west2.run.app/api/v1/cpi?api_key=YOUR_KEY&year=2023"

# Get employment data for California
curl "https://bls-api-microservice-832081557693.europe-west2.run.app/api/v1/la?api_key=YOUR_KEY&state_code=06"

# Paginated results
curl "https://bls-api-microservice-832081557693.europe-west2.run.app/api/v1/ce?api_key=YOUR_KEY&page=2&limit=50"

# Advanced: year range + area + seasonal adjustment (CPI)
curl "https://bls-api-microservice-832081557693.europe-west2.run.app/api/v1/cpi?api_key=YOUR_KEY&year_gte=2020&year_lte=2023&area_code=0000&seasonal_code=S&limit=25"

# Advanced: multiple years + multiple states + measure (LA)
curl "https://bls-api-microservice-832081557693.europe-west2.run.app/api/v1/la?api_key=YOUR_KEY&year=2022,2023&state_code=06,36,48&measure_code=03&limit=50"
```

> **Tip:** Different parameters use AND logic; comma-separated values within a parameter use OR logic. See [API.md](API.md) for full advanced query documentation.

### Response Format

```json
{
  "data": [...],
  "total": 15420,
  "limit": 100,
  "offset": 0,
  "has_more": true
}
```

## Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /api/v1/cpi` | Consumer Price Index data |
| `GET /api/v1/ce` | Current Employment Statistics |
| `GET /api/v1/ppi` | Producer Price Index data |
| `GET /api/v1/jt` | Job Openings and Labor Turnover |
| `GET /api/v1/la` | Local Area Unemployment Statistics |
| `GET /api/v1/ci` | Employment Cost Index |
| `GET /api/v1/mp` | Major Sector Productivity |
| `GET /api/v1/oe` | Occupational Employment and Wages |
| `GET /api/v1/sa` | State and Area Employment |
| `GET /api/v1/sm` | State and Metropolitan Employment |

## Common Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `year` | string | Filter by year (comma-separated) |
| `year_gte` | int | Year >= value |
| `year_lte` | int | Year <= value |
| `limit` | int | Max results (default: 100, max: 1000) |
| `offset` | int | Records to skip |
| `page` | int | Page number (1-based) |

## Documentation

Full API documentation is available in [API.md](API.md).

Interactive API docs (Swagger UI) available at `/docs` when running locally.

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Deployment**: Google Cloud Run
- **Containerization**: Docker

## License

MIT
