FROM python:3.12-slim

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y gcc libpq-dev curl

# Install uv
RUN pip install --no-cache-dir uv

# Copy only project metadata first
COPY pyproject.toml uv.lock ./

# Install deps before copying rest of code
RUN uv pip install --system .[dev]

# Copy the rest of your codebase
COPY . .

# Environment config
ENV FLASK_APP=run.py
ENV FLASK_CONFIG=production

# CMD that runs migration then starts the app
CMD ["sh", "-c", "uv pip run flask db upgrade && uv pip run gunicorn run:app --bind 0.0.0.0:5000"]
