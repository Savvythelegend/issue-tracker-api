# Issue Tracker API

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/Savvythelegend/issue-tracker-api/actions)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Dockerized](https://img.shields.io/badge/docker-ready-blue)](https://www.docker.com/)
[![Flask](https://img.shields.io/badge/flask-2.x-orange.svg)](https://flask.palletsprojects.com/)

A secure, production-ready, and Dockerized backend API to manage issue tickets. It supports JWT auth, RBAC, Alembic migrations, and is built with a focus on modularity and testability.

---

## 📑 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Setup](#setup)
  - [Environment Variables](#environment-variables)
  - [Running Locally](#running-locally)
  - [Running with Docker](#running-with-docker)
- [Testing](#testing)
- [Linting & Formatting](#linting--formatting)
- [Deployment](#deployment)
- [Project Status](#project-status)

---

## ✅ Features

- JWT authentication (access & refresh tokens)
- Role-Based Access Control (Admin/User)
- Issue ticket CRUD operations
- Token revocation (logout functionality)
- Alembic for DB migrations
- Pytest test suite
- Dockerized development & production setup
- Pre-commit hooks (Black, isort, flake8)
- Pydantic for request validation

---

## 🛠 Tech Stack

| Category       | Tools & Libraries                                                  |
|----------------|---------------------------------------------------------------------|
| **Framework**  | [Flask](https://flask.palletsprojects.com/)                        |
| **ORM**        | [SQLAlchemy](https://www.sqlalchemy.org/)                          |
| **Auth**       | JWT (with blacklist support)                                       |
| **Database**   | [PostgreSQL](https://www.postgresql.org/)                          |
| **Migrations** | [Alembic](https://alembic.sqlalchemy.org/)                         |
| **Testing**    | [Pytest](https://docs.pytest.org/)                                 |
| **Dev Tools**  | Docker, Docker Compose, [uv](https://pypi.org/project/uv/), Black, isort, pre-commit |

---

## 📐 Architecture

```text
             ┌────────────┐
             │  Client    │
             └────┬───────┘
                  │
          HTTP API Requests
                  │
             ┌────▼──────┐
             │ Flask App │
             └────┬──────┘
      ┌────────────┴────────────┐
      │                         │
┌─────▼─────┐           ┌───────▼────────┐
│ Auth Layer│           │ Issue Routes   │
└─────┬─────┘           └────────┬───────┘
      │                          │
┌─────▼───────┐         ┌────────▼────────┐
│JWT & RBAC   │         │CRUD + Validation│
└─────┬───────┘         └────────┬────────┘
      │                          │
  ┌───▼────┐               ┌─────▼─────┐
  │Database│ ◄──────────── │ SQLAlchemy│
  └────────┘               └───────────┘
````

---

## 📂 Project Structure

```text
issue-tracker-api/
├── app/
│   ├── core/           # Config & extensions
│   ├── models/         # SQLAlchemy models
│   ├── routes/         # Flask blueprints
│   └── __init__.py     # App factory
├── tests/              # Pytest test cases
├── migrations/         # Alembic migrations
├── Dockerfile
├── docker-compose.dev.yml
├── docker-compose.prod.yml
├── .pre-commit-config.yaml
├── .gitignore
├── pyproject.toml
├── run.py
└── README.md
```

---

## ⚙️ Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Savvythelegend/issue-tracker-api.git
cd issue-tracker-api
```

### 2. Install Dependencies (Dev)

```bash
uv pip install .[dev]
```

---

## 🧪 Environment Variables

Create a `.env` file in the project root:

```ini
FLASK_CONFIG=development
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/issue_tracker
JWT_SECRET_KEY=your-secret-key
```

---

## ▶️ Running Locally (without Docker)

```bash
flask db upgrade
flask run
```

---

## 🐳 Running with Docker

```bash
docker compose -f docker-compose.dev.yml up --build
```

---

## ✅ Testing

```bash
pytest
```

---

## 🧹 Linting & Formatting

```bash
pre-commit run --all-files
```

---

## 🚀 Deployment

Use `docker-compose.prod.yml` or a PaaS provider like Render, Railway, or Northflank.

Ensure production environment variables are set:

```ini
FLASK_CONFIG=production
DATABASE_URL=<your-production-db-url>
JWT_SECRET_KEY=<your-secure-key>
```

---

## 📈 Project Status

Actively maintained with regular updates and improvements. Open to issues and contributions!
