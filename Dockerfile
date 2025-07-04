# Use official Python slim image
FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app

# Install system dependencies required for psycopg2 and compilation
RUN apt-get update && apt-get install -y gcc libpq-dev curl && rm -rf /var/lib/apt/lists/*

# Install uv (Python dependency manager)
RUN pip install --no-cache-dir uv

# Copy the entire project source, including pyproject.toml, app/, README.md, etc.
COPY . .

# Install all dependencies including optional dev dependencies into the system environment
RUN uv pip install --system .[dev]

# Set environment variables
ENV FLASK_APP=run.py
ENV FLASK_CONFIG=production

# Expose port
EXPOSE 5000

# Create a startup script
RUN echo '#!/bin/bash\nflask db upgrade\ngunicorn run:app --bind 0.0.0.0:${PORT:-5000}' > /app/start.sh && chmod +x /app/start.sh

# Use the startup script
CMD ["/app/start.sh"]
