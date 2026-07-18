# Marketplace Backend API

This repository contains the REST API for the Marketplace application. It handles user authentication, profile management, and order processing using a decoupled, asynchronous architecture.

## Architecture

The backend system consists of four main components running inside isolated containers:
- FastAPI: Manages the HTTP request-response cycle, endpoint routing, and request validation.
- PostgreSQL: Serves as the primary relational database for persistent storage.
- Redis: Functions as the high-speed message broker for distributed task queues.
- Celery: Executes long-running background processes independently from the main web server thread.

## Core Technologies

- Python 3.11
- FastAPI
- SQLAlchemy (Database ORM)
- Alembic (Database Migrations)
- PostgreSQL
- Celery
- Redis
- Docker and Docker Compose

## API Documentation

When the application service is running locally, the interactive API documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Development Setup

1. Create a `.env` file in the root directory and define the following variables:
   DATABASE_URL=postgresql://user:password@db/dbname
   REDIS_URL=redis://redis:6379/0
   SECRET_KEY=your_jwt_signing_key
   SMTP_EMAIL=your_configured_email@gmail.com
   SMTP_PASSWORD=your_email_app_password

2. Build and launch the application infrastructure using Docker Compose:
   docker compose up --build -d

3. Apply database schema migrations:
   docker compose exec web alembic upgrade head