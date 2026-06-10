# =============================================================================
# WebGuard — Production Dockerfile
# =============================================================================
# Multi-stage build:
#   builder — installs dependencies
#   runtime — lean production image
# =============================================================================

# ---------------------------------------------------------------------------
# Stage 1: Builder
# ---------------------------------------------------------------------------
FROM python:3.11-slim AS builder

WORKDIR /build

# System packages needed to compile some Python dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
# Install all runtime dependencies into a local prefix
RUN pip install --no-cache-dir --prefix=/install .

# ---------------------------------------------------------------------------
# Stage 2: Runtime
# ---------------------------------------------------------------------------
FROM python:3.11-slim AS runtime

# System packages required at runtime:
#   WeasyPrint needs pango, cairo, gdk-pixbuf for PDF generation
#   libpq-dev needed for asyncpg / psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libpangocairo-1.0-0 \
    libcairo2 \
    libgdk-pixbuf-2.0-0 \
    libffi8 \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder /install /usr/local

# Copy application source
COPY engine/ engine/
COPY cli/ cli/
COPY api/ api/
COPY reports/ reports/

# Run as non-root user (per NFR-003 — Docker containers run as non-root)
RUN useradd --create-home --uid 1000 webguard \
    && chown -R webguard:webguard /app
USER webguard

EXPOSE 8000

# Default command — overridden by docker-compose per service
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
