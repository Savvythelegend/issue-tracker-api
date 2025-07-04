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

# Debug: Check what's installed and where
RUN which python
RUN which pip
RUN pip list | grep gunicorn || echo "gunicorn not found in pip list"
RUN find / -name gunicorn -type f 2>/dev/null || echo "gunicorn executable not found"

# Set environment variables
ENV FLASK_APP=run.py
ENV FLASK_CONFIG=production

# Try running gunicorn directly to see the error
CMD ["python", "-m", "gunicorn", "run:app", "--bind", "0.0.0.0:5000"]
