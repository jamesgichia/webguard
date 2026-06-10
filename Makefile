.PHONY: help install lint format test test-engine test-api \
        run-api run-worker docker-up docker-down migrate migration clean

# ---------------------------------------------------------------------------
# Help
# ---------------------------------------------------------------------------
help:
	@echo ""
	@echo "  WebGuard — Developer Commands"
	@echo "  ─────────────────────────────"
	@echo "  install      Install all dependencies (including dev)"
	@echo "  lint         Run Ruff linter and Mypy type checker"
	@echo "  format       Auto-format with Black and Ruff --fix"
	@echo "  test         Run full test suite with coverage"
	@echo "  test-engine  Run engine unit tests only"
	@echo "  test-api     Run API integration tests only"
	@echo "  run-api      Start FastAPI dev server on :8000"
	@echo "  run-worker   Start Celery worker"
	@echo "  docker-up    Start all Docker services (detached)"
	@echo "  docker-down  Stop and remove containers"
	@echo "  migrate      Apply pending Alembic migrations"
	@echo "  migration    Create new migration: make migration msg='...' "
	@echo "  clean        Remove __pycache__, .pytest_cache, .coverage"
	@echo ""

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------
install:
	pip install -e ".[dev]"
	pre-commit install
	@echo "✓ Dependencies installed and pre-commit hooks registered"

# ---------------------------------------------------------------------------
# Code quality
# ---------------------------------------------------------------------------
lint:
	ruff check .
	mypy engine cli api
	@echo "✓ Lint passed"

format:
	black .
	ruff check --fix .
	@echo "✓ Formatting complete"

# ---------------------------------------------------------------------------
# Testing
# ---------------------------------------------------------------------------
test:
	pytest

test-engine:
	pytest tests/unit/ -v \
		--cov=engine \
		--cov-report=term-missing \
		--no-cov-on-fail

test-api:
	pytest tests/integration/ -v \
		--cov=api \
		--cov-report=term-missing

# ---------------------------------------------------------------------------
# Local development servers
# ---------------------------------------------------------------------------
run-api:
	uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

run-worker:
	celery -A api.workers.scan_tasks worker --loglevel=info --concurrency=4

# ---------------------------------------------------------------------------
# Docker
# ---------------------------------------------------------------------------
docker-up:
	docker-compose up -d
	@echo "✓ Services started. API → http://localhost:8000 | Docs → http://localhost:8000/docs"

docker-down:
	docker-compose down
	@echo "✓ Services stopped"

docker-logs:
	docker-compose logs -f

# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------
migrate:
	alembic upgrade head
	@echo "✓ Migrations applied"

migration:
	@test -n "$(msg)" || (echo "ERROR: Provide a message: make migration msg='description'" && exit 1)
	alembic revision --autogenerate -m "$(msg)"

# ---------------------------------------------------------------------------
# Cleanup
# ---------------------------------------------------------------------------
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -name ".coverage" -delete 2>/dev/null || true
	find . -name "coverage.xml" -delete 2>/dev/null || true
	@echo "✓ Cleaned build artifacts"
