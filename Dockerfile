FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc libpq-dev curl

RUN pip install --no-cache-dir uv

# Make sure only deps are copied first
COPY pyproject.toml uv.lock ./

# Correct install
RUN uv pip install --system .[dev]

# Now copy the actual app files
COPY . .

ENV FLASK_APP=run.py
ENV FLASK_CONFIG=production

# Final correct CMD
CMD ["sh", "-c", "uv pip run flask db upgrade && uv pip run gunicorn run:app --bind 0.0.0.0:5000"]
