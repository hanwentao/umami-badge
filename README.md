# umami-badge

A simple web service that provides API endpoints for version information, health status checking, and Umami visit statistics, built with FastAPI.

## Features

- API endpoint to retrieve software version information
- Health check endpoint to monitor service status
- Endpoint to fetch website visit counts from Umami
- Additional status endpoint with timestamp
- Automatic interactive API documentation with Swagger UI

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
  "timestamp": "2025-12-08T10:59:02.112085"
}
```

### GET /api/visits
Fetch visit count from Umami for a given domain and return in shields.io format.

**Parameters:**
- `domain` (required): The domain to fetch visit data for

**Example:**
```bash
curl "http://localhost:8000/api/visits?domain=example.com"
```

**Response (shields.io format):**
```json
{
  "schemaVersion": 1,
  "label": "visits",
  "message": "123",
  "color": "green",
  "isError": false,
  "cacheSeconds": 300
}
```

## Setup

1. Install dependencies:
   ```bash
   uv sync
   ```

2. Create a .env file with your environment configuration (see .env.example for the format):
   ```bash
   cp .env.example .env
   # Edit .env with your actual values
   ```

3. Create a config.toml file with your website configuration (see config.toml.example for the format):
   ```bash
   cp config.toml.example config.toml
   # Edit config.toml with your actual values
   ```

4. Run the service:
   ```bash
   python main.py
   ```

The service will be available at `http://localhost:8000`.

## API Documentation

FastAPI automatically provides interactive API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Deployment

### Docker

You can deploy the application using Docker or Docker Compose.

#### Using Docker

Build the image:
```bash
docker build -t umami-badge .
```

Run the container:
```bash
docker run -p 8000:8000 \
  -v $(pwd)/config.toml:/app/config.toml \
  -v $(pwd)/.env:/app/.env \
  --env ENVIRONMENT=production \
  umami-badge
```

#### Using Docker Compose

```bash
docker-compose up -d
```

### Configuration

#### Environment Variables (.env file)

- `ENVIRONMENT` (optional): Set to change the environment name (default: "development"). When set to "development", enables auto-reload.
- `UMAMI_URL` (required for /api/visits): URL of your Umami instance
- `UMAMI_TOKEN` (required for /api/visits): Pre-obtained Umami API token for authentication
- `BADGE_COLOR` (optional): Color of the badge (default: "brightgreen"). Common values include "brightgreen", "green", "red", "blue", "yellow", "orange", etc.
- `CONFIG_FILE` (optional): Path to the configuration TOML file (default: "config.toml")

### Website Configuration (config.toml file)

Website-specific settings are stored in a TOML file:

```toml
# Configuration for umami-badge
# Website-specific settings go here

# Domain to website ID mappings with bias count
[[domains]]
domain = "example.com"
website_id = "12345"
bias_count = 100

[[domains]]
domain = "another-domain.com"
website_id = "67890"
bias_count = 50

# Additional domains can be added as needed
# [[domains]]
# domain = "third-domain.com"
# website_id = "11111"
# bias_count = 0
```

The `bias_count` field allows you to add a fixed number to the actual visit count returned by Umami for each domain.