FROM python:3.14-slim

# For health check
RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends curl ; \
    apt-get dist-clean

WORKDIR /app

# Copy project files
COPY . .

# Install the application and its dependencies using pip install .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir .

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "main.py"]
