import os
import sys
from datetime import datetime
from typing import Any, Dict

from fastapi import FastAPI

app = FastAPI(
    title="umami-badge API", description="Simple API for version and health checks"
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


# Optional: Basic home endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to umami-badge API", "status": "running"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
