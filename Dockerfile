# Use official Python slim image
FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app

# Install system dependencies required for psycopg2 and compilation
RUN apt-get update && apt-get install -y gcc libpq-dev curl

# Install uv (Python dependency manager)
RUN pip install --no-cache-dir uv

# Copy the entire project source, including pyproject.toml, app/, README.md, etc.
COPY . .

# Install all dependencies including optional dev dependencies into the system environment
RUN uv pip install --system .[dev]

# Set environment variables
ENV FLASK_APP=run.py
ENV FLASK_CONFIG=production

# Run DB migrations and start the server with Gunicorn
CMD ["sh", "-c", "uv pip run flask db upgrade && uv pip run gunicorn run:app --bind 0.0.0.0:5000"]
