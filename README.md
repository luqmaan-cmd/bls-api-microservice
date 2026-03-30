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
| MP | Mass Layoff Statistics | Large-scale layoff events |
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
https://bls-api-microservice-2r464mi4sq-nw.a.run.app
```

### Authentication

All requests require an API key:

```bash
curl "https://bls-api-microservice-2r464mi4sq-nw.a.run.app/cpi?api_key=YOUR_API_KEY"
```

### Example Requests

```bash
# Get CPI data for 2023
curl "https://bls-api-microservice-2r464mi4sq-nw.a.run.app/cpi?api_key=YOUR_KEY&year=2023"

# Get employment data for California
curl "https://bls-api-microservice-2r464mi4sq-nw.a.run.app/la?api_key=YOUR_KEY&state_code=06"

# Paginated results
curl "https://bls-api-microservice-2r464mi4sq-nw.a.run.app/ce?api_key=YOUR_KEY&page=2&limit=50"
```

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
| `GET /cpi` | Consumer Price Index data |
| `GET /ce` | Current Employment Statistics |
| `GET /ppi` | Producer Price Index data |
| `GET /jt` | Job Openings and Labor Turnover |
| `GET /la` | Local Area Unemployment Statistics |
| `GET /ci` | Employment Cost Index |
| `GET /mp` | Mass Layoff Statistics |
| `GET /oe` | Occupational Employment and Wages |
| `GET /sa` | State and Area Employment |
| `GET /sm` | State and Metropolitan Employment |

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
