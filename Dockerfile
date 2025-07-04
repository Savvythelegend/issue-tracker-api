FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y gcc libpq-dev curl && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install --no-cache-dir uv

# Copy project files
COPY . .

# Install dependencies
RUN uv pip install --system .[dev]

# Set environment variables
ENV FLASK_APP=run.py
ENV FLASK_CONFIG=production

# Make sure /usr/local/bin is in PATH
ENV PATH="/usr/local/bin:$PATH"

# Run migrations and start server
CMD ["sh", "-c", "flask db upgrade && gunicorn run:app --bind 0.0.0.0:$PORT"]
