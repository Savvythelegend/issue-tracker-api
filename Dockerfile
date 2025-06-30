# syntax=docker/dockerfile:1
FROM python:3.12-slim

# Set work directory inside container
WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y gcc libpq-dev

# Copy files
COPY . .

# Install Python deps
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the Flask port
EXPOSE 5000

# Set env variables
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

# Run the app
CMD ["flask", "run"]
