"""
WebGuard REST API backend.

Built with FastAPI. Handles user authentication, scan job dispatch via
Celery, result storage in PostgreSQL, and report file serving.

Internal structure:
  api.main        — FastAPI application factory
  api.config      — environment-variable-driven settings
  api.database    — SQLAlchemy async session management
  api.models      — ORM models and Alembic migrations
  api.routes      — FastAPI route handlers
  api.schemas     — Pydantic request/response schemas
  api.services    — business logic layer
  api.workers     — Celery task definitions
"""
