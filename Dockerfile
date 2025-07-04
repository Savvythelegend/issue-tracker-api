# syntax=docker/dockerfile:1
FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc libpq-dev
RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock ./
RUN uv pip install .[dev]

COPY . .

EXPOSE 5000

ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

CMD ["uv", "pip", "run", "flask", "run"]
