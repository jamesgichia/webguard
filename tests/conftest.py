"""
Pytest configuration and shared fixtures for the WebGuard test suite.

Fixtures defined here are available to all tests without explicit imports.
"""

import os

# ---------------------------------------------------------------------------
# Ensure tests always run with WEBGUARD_ENV=testing so no production
# resources are accidentally touched.
# ---------------------------------------------------------------------------
os.environ.setdefault("WEBGUARD_ENV", "testing")
os.environ.setdefault("WEBGUARD_SECRET_KEY", "test-secret-key-not-for-production")
os.environ.setdefault(
    "DATABASE_URL",
    "postgresql+asyncpg://webguard:webguard_test@localhost:5432/webguard_test",
)
os.environ.setdefault(
    "DATABASE_URL_SYNC",
    "postgresql+psycopg2://webguard:webguard_test@localhost:5432/webguard_test",
)
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")
os.environ.setdefault("CELERY_BROKER_URL", "redis://localhost:6379/0")
os.environ.setdefault("CELERY_RESULT_BACKEND", "redis://localhost:6379/1")
os.environ.setdefault("REPORT_OUTPUT_DIR", "/tmp/webguard-test-reports")
