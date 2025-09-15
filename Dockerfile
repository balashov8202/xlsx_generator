# syntax=docker/dockerfile:1
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Install build deps for openpyxl if needed (libjpeg/zlib often present). Also add curl for healthchecks.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install python deps first (better layer caching)
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . /app

# Expose Flask port
EXPOSE 8080

# Default to gunicorn for production
# Bind to 0.0.0.0:8080, 2 workers should be enough for this CPU-bound-ish task
CMD gunicorn --bind 0.0.0.0:8080 --workers 2 --threads 4 --timeout 300 app:app
