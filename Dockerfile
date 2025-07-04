FROM python:3.12-slim

WORKDIR /app

# Install system packages
RUN apt-get update && apt-get install -y gcc libpq-dev

# Install uv
RUN pip install --no-cache-dir uv

# Copy project files
COPY . .

# Install dependencies
RUN uv pip install --system .[dev]

# Set environment variables
ENV FLASK_APP=run.py
ENV FLASK_CONFIG=production

# Run migrations and start app
CMD ["sh", "-c", "uv pip run flask db upgrade && uv pip run gunicorn run:app --bind 0.0.0.0:5000"]
