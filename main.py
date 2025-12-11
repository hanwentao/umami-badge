import os
import sys
import time
from datetime import datetime
from typing import Any, Dict

import httpx
import toml
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query

# Load environment variables from .env file
load_dotenv()

# Load website configuration from TOML file
config_file = os.environ.get("CONFIG_FILE", "config.toml")
try:
    with open(config_file, "r") as f:
        config = toml.load(f)
except FileNotFoundError:
    # If config file doesn't exist, create a default config
    config = {"domains": []}

app = FastAPI(
    title="umami-badge API", description="Simple API for getting visit data from Umami"
)


# Get the current version from the project configuration
def get_version():
    # In a real implementation, this could read from package metadata
    return "0.1.0"


@app.get("/api/version", response_model=Dict[str, Any])
async def api_version():
    """Return the current version of the service"""
    version_info = {
        "version": get_version(),
        "service": "umami-badge",
        "python_version": sys.version,
        "environment": os.environ.get("ENVIRONMENT", "development"),
    }
    return version_info


@app.get("/api/health", response_model=Dict[str, Any])
async def api_health():
    """Return the health status of the service"""
    health_status = {
        "status": "healthy",
        "service": "umami-badge",
        "version": get_version(),
    }
    return health_status


@app.get("/api/status", response_model=Dict[str, Any])
async def api_status():
    """Return a combined status response"""
    status_info = {
        "status": "running",
        "version": get_version(),
        "service": "umami-badge",
        "timestamp": datetime.now().isoformat(),
    }
    return status_info


# Function to fetch visit data from Umami API
async def fetch_umami_visits(website_id: str) -> Dict[str, Any]:
    """
    Fetch visit data from Umami API for a given website ID
    This function requires Umami API settings to be configured as environment variables
    """
    # Check for Umami configuration in environment variables
    umami_url = os.environ.get("UMAMI_URL", "")
    umami_token = os.environ.get("UMAMI_TOKEN", "")

    if not all([umami_url, umami_token, website_id]):
        raise HTTPException(
            status_code=500,
            detail="Umami configuration not found. Please set UMAMI_URL and UMAMI_TOKEN environment variables.",
        )

    # Make request to Umami API using the pre-obtained token
    async with httpx.AsyncClient() as client:
        # Fetch stats for the website using the token
        # For all-time visits, we set startAt to a very early timestamp (Unix epoch)
        # and endAt to the current time
        start_at = 0  # Beginning of time (Unix epoch in milliseconds would be 0)
        end_at = int(time.time() * 1000)  # Current time in milliseconds

        headers = {"Authorization": f"Bearer {umami_token}"}
        stats_response = await client.get(
            f"{umami_url.rstrip('/')}/api/websites/{website_id}/stats",
            headers=headers,
            params={
                "startAt": start_at,  # Beginning of time in milliseconds
                "endAt": end_at,  # Current time in milliseconds
            },
        )

        if stats_response.status_code != 200:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to fetch stats from Umami API: {stats_response.text}",
            )

        return stats_response.json()


@app.get("/api/visits", response_model=Dict[str, Any])
async def api_visits(
    domain: str = Query(..., description="The domain to fetch visit data for"),
):
    """
    Fetch visit count from Umami for a given domain and return in shields.io format
    """
    try:
        # Find the website ID and bias_count for the given domain from the TOML configuration
        website_id = None
        bias_count = 0  # Default bias is 0 if not specified in config

        for domain_config in config.get("domains", []):
            if domain_config.get("domain") == domain:
                website_id = domain_config.get("website_id")
                bias_count = domain_config.get("bias_count", 0)  # Default to 0 if not specified
                break

        # If no mapping found in TOML config, try to use domain as websiteId directly
        # (this is a fallback and not recommended for production)
        if not website_id:
            website_id = domain

        # Fetch visit data from Umami
        umami_data = await fetch_umami_visits(website_id)

        # Extract visit count - adjust based on the actual Umami API response format
        visits = umami_data.get("visits", 0)

        # Apply the bias count to the visit count
        adjusted_visits = visits + bias_count

        # Format response in shields.io compatible format
        shields_io_format = {
            "schemaVersion": 1,
            "label": "visits",
            "message": f"{adjusted_visits}",
            "color": "green",
            "isError": False,
            "cacheSeconds": 300,  # Cache for 5 minutes
        }

        return shields_io_format
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching visit data: {str(e)}"
        )


# Optional: Basic home endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to umami-badge API", "status": "running"}


if __name__ == "__main__":
    import uvicorn

    # Check if we're in development mode
    environment = os.environ.get("ENVIRONMENT", "production")

    if environment.lower() == "development":
        # For development with reload, we need to pass the module as a string
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    else:
        # For production, run the app directly
        uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
