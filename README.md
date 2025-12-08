# umami-badge

A simple web service that provides API endpoints for version information and health status checking.

## Features

- API endpoint to retrieve software version information
- Health check endpoint to monitor service status
- Additional status endpoint with timestamp

## API Endpoints

### GET /api/version
Returns the current version of the service.

**Response:**
```json
{
  "version": "0.1.0",
  "service": "umami-badge",
  "python_version": "3.14.0 (main, Oct  7 2025, 16:07:00) [Clang 20.1.4 ]",
  "environment": "development"
}
```

### GET /api/health
Returns the health status of the service.

**Response:**
```json
{
  "status": "healthy",
  "service": "umami-badge",
  "version": "0.1.0"
}
```

### GET /api/status
Returns the combined status information with a timestamp.

**Response:**
```json
{
  "status": "running",
  "version": "0.1.0",
  "service": "umami-badge",
  "timestamp": "2025-12-08T08:32:36.605254"
}
```

## Setup

1. Install dependencies:
   ```bash
   uv sync
   ```

2. Run the service:
   ```bash
   python main.py
   ```

The service will be available at `http://localhost:8000`.

## Environment Variables

- `ENVIRONMENT` (optional): Set to change the environment name (default: "development")