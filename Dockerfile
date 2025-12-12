FROM python:3.14-slim

WORKDIR /app

# Copy project files
COPY pyproject.toml uv.lock ./

# Install uv package manager
RUN pip install --no-cache-dir --upgrade pip && pip install uv

# Install dependencies
RUN uv sync --no-dev

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uv", "run", "main.py"]
