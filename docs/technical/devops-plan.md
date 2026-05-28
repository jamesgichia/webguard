
WebGuard — DevOps and Infrastructure Plan
Document: DevOps and Infrastructure Plan
Version: 1.0
Status: Draft
Created: May 2026
Author: James Gichia
Repository: docs/technical/devops-plan.md

1. Purpose
This document defines the complete DevOps strategy for WebGuard Version 1.0. It covers local development environment setup, CI/CD pipeline design, production infrastructure, deployment procedures, monitoring, and disaster recovery.
This document must be detailed enough that a developer who has never worked on WebGuard before can set up a fully working local environment and understand the complete deployment pipeline by reading it once.

2. Technology Overview
Local Development:    Docker Compose
Version Control:      Git — GitHub
CI/CD:                GitHub Actions
Production Hosting:   DigitalOcean (recommended) or AWS
Web Server:           Nginx
Application Server:   Uvicorn (FastAPI)
Task Workers:         Celery
Container Runtime:    Docker
Database:             PostgreSQL 16 (managed)
Cache/Queue:          Redis 7 (managed)
SSL Certificates:     Let's Encrypt via Certbot
CDN/DDoS Protection:  Cloudflare
Error Tracking:       Sentry
Uptime Monitoring:    UptimeRobot
Log Management:       Application logs via Docker logging driver

3. Repository Structure for DevOps
webguard/
├── .github/
│   └── workflows/
│       ├── test.yml          ← Runs on every push
│       ├── lint.yml          ← Runs on every push
│       ├── security.yml      ← Runs on every push
│       └── deploy.yml        ← Runs on merge to main
│
├── docker/
│   ├── Dockerfile.api        ← FastAPI application image
│   ├── Dockerfile.worker     ← Celery worker image
│   └── Dockerfile.web        ← React frontend build image
│
├── docker-compose.yml        ← Production-like local environment
├── docker-compose.dev.yml    ← Development overrides
├── docker-compose.test.yml   ← Test environment
│
├── nginx/
│   ├── nginx.conf            ← Production Nginx config
│   └── nginx.dev.conf        ← Development Nginx config
│
├── scripts/
│   ├── setup.sh              ← First-time local setup
│   ├── start.sh              ← Start local environment
│   ├── stop.sh               ← Stop local environment
│   ├── migrate.sh            ← Run database migrations
│   ├── test.sh               ← Run test suite
│   └── deploy.sh             ← Production deployment script
│
├── .env.example              ← Environment variable template
└── Makefile                  ← Convenience commands

4. Local Development Environment
4.1 Prerequisites
Before setting up WebGuard locally ensure the following are installed:
Git                 >= 2.40
Docker              >= 26.0
Docker Compose      >= 2.27
Python              >= 3.11
Node.js             >= 20.0
npm                 >= 10.0
Verify on Kali Linux:
bashgit --version
docker --version
docker compose version
python3 --version
node --version
npm --version

4.2 First-Time Setup
Clone the repository and run the setup script:
bash# Clone repository
git clone https://github.com/jamesgichia/webguard.git
cd webguard

# Switch to develop branch
git checkout develop

# Run first-time setup
chmod +x scripts/setup.sh
./scripts/setup.sh
What setup.sh does:
bash#!/bin/bash
set -e

echo "Setting up WebGuard development environment..."

# 1. Copy environment template
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env from template — update values before starting"
fi

# 2. Create Python virtual environment
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 3. Install frontend dependencies
cd web
npm install
cd ..

# 4. Pull Docker images
docker compose pull

# 5. Build custom images
docker compose build

echo "Setup complete. Update .env then run ./scripts/start.sh"

4.3 Environment Configuration
Copy .env.example to .env and fill in values:
bash# .env.example — committed to repository
# .env — never committed, gitignored

# ─── Application ──────────────────────────────────────
ENVIRONMENT=development
DEBUG=true
SECRET_KEY=generate-a-random-32-character-string-here
FRONTEND_URL=http://localhost:3000

# ─── Database ─────────────────────────────────────────
DATABASE_URL=postgresql://webguard:webguard_dev@localhost:5432/webguard
POSTGRES_USER=webguard
POSTGRES_PASSWORD=webguard_dev
POSTGRES_DB=webguard

# ─── Redis ────────────────────────────────────────────
REDIS_URL=redis://localhost:6379/0

# ─── JWT ──────────────────────────────────────────────
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# ─── External APIs ────────────────────────────────────
NVD_API_KEY=your-nvd-api-key-here
# Get free key at: https://nvd.nist.gov/developers/request-an-api-key

# ─── Scanning ─────────────────────────────────────────
MAX_CONCURRENT_SCANS=5
SCAN_TIMEOUT_SECONDS=300
MAX_REQUESTS_PER_SCAN=50

# ─── Monitoring ───────────────────────────────────────
SENTRY_DSN=
# Leave empty in development — add in production

# ─── Rate Limiting ────────────────────────────────────
RATE_LIMIT_SCANS_PER_HOUR=5
RATE_LIMIT_LOGIN_PER_MINUTE=10
Generate SECRET_KEY:
bashpython3 -c "import secrets; print(secrets.token_hex(32))"

4.4 Docker Compose Configuration
docker-compose.yml (base configuration):
yamlversion: '3.9'

services:

  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    ports:
      - "6379:6379"

  api:
    build:
      context: .
      dockerfile: docker/Dockerfile.api
    env_file: .env
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    ports:
      - "8000:8000"
    volumes:
      - report_files:/app/reports/generated
    command: >
      sh -c "alembic upgrade head &&
             uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload"

  worker:
    build:
      context: .
      dockerfile: docker/Dockerfile.worker
    env_file: .env
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    volumes:
      - report_files:/app/reports/generated
    command: celery -A api.workers.scan_worker worker
             --loglevel=info
             --concurrency=4

  web:
    build:
      context: .
      dockerfile: docker/Dockerfile.web
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://localhost:8000

volumes:
  postgres_data:
  redis_data:
  report_files:
docker-compose.dev.yml (development overrides):
yamlversion: '3.9'

services:

  api:
    volumes:
      - ./api:/app/api        # Hot reload — code changes reflected immediately
      - ./engine:/app/engine
    environment:
      - DEBUG=true

  worker:
    volumes:
      - ./api:/app/api
      - ./engine:/app/engine
    command: celery -A api.workers.scan_worker worker
             --loglevel=debug
             --concurrency=2

  web:
    volumes:
      - ./web/src:/app/src    # Hot reload for React
    environment:
      - CHOKIDAR_USEPOLLING=true  # Required for file watching in Docker

4.5 Dockerfiles
docker/Dockerfile.api:
dockerfileFROM python:3.11-slim

# Security — run as non-root
RUN addgroup --system webguard && \
    adduser --system --ingroup webguard webguard

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libcairo2 \
    libgdk-pixbuf2.0-0 \
    && rm -rf /var/lib/apt/lists/*
# Note: pango/cairo required by WeasyPrint for PDF generation

WORKDIR /app

# Install Python dependencies first (cached layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY api/ ./api/
COPY engine/ ./engine/
COPY reports/ ./reports/
COPY alembic/ ./alembic/
COPY alembic.ini .

# Create reports directory
RUN mkdir -p reports/generated && \
    chown -R webguard:webguard /app

USER webguard

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
docker/Dockerfile.worker:
dockerfileFROM python:3.11-slim

RUN addgroup --system webguard && \
    adduser --system --ingroup webguard webguard

RUN apt-get update && apt-get install -y \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libcairo2 \
    libgdk-pixbuf2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY api/ ./api/
COPY engine/ ./engine/
COPY reports/ ./reports/

RUN mkdir -p reports/generated && \
    chown -R webguard:webguard /app

USER webguard

CMD ["celery", "-A", "api.workers.scan_worker", "worker",
     "--loglevel=info", "--concurrency=4"]
docker/Dockerfile.web:
dockerfile# Build stage
FROM node:20-alpine AS builder

WORKDIR /app
COPY web/package*.json ./
RUN npm ci --only=production

COPY web/ .
RUN npm run build

# Production stage — Nginx serves static files
FROM nginx:alpine

COPY --from=builder /app/build /usr/share/nginx/html
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

4.6 Starting and Stopping Local Environment
Start everything:
bash# Development mode with hot reload
docker compose -f docker-compose.yml -f docker-compose.dev.yml up

# Or using Makefile shortcut
make dev
Start in background:
bashdocker compose -f docker-compose.yml -f docker-compose.dev.yml up -d
Stop everything:
bashdocker compose down

# Stop and remove volumes (clean slate)
docker compose down -v
View logs:
bash# All services
docker compose logs -f

# Specific service
docker compose logs -f api
docker compose logs -f worker
Access services:
Web Dashboard:  http://localhost:3000
API:            http://localhost:8000
API Docs:       http://localhost:8000/docs
PostgreSQL:     localhost:5432
Redis:          localhost:6379

4.7 Database Migrations
bash# Run all pending migrations
docker compose exec api alembic upgrade head

# Create a new migration
docker compose exec api alembic revision --autogenerate -m "description"

# View migration history
docker compose exec api alembic history

# Rollback one migration
docker compose exec api alembic downgrade -1

# Or using Makefile
make migrate
make migrate-down

4.8 Makefile — Convenience Commands
makefile# Makefile

.PHONY: dev stop logs migrate test lint format clean

dev:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up

stop:
	docker compose down

logs:
	docker compose logs -f

migrate:
	docker compose exec api alembic upgrade head

migrate-new:
	docker compose exec api alembic revision --autogenerate -m "$(name)"

test:
	./scripts/test.sh

lint:
	black --check engine/ api/ cli/
	flake8 engine/ api/ cli/
	mypy engine/ api/ cli/

format:
	black engine/ api/ cli/

clean:
	docker compose down -v
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

shell-api:
	docker compose exec api bash

shell-db:
	docker compose exec postgres psql -U webguard -d webguard

install:
	./scripts/setup.sh

5. CI/CD Pipeline
5.1 Pipeline Overview
Every push to any branch:
    → Lint and type check
    → Security scan (dependencies)
    → Unit tests

Every pull request to develop or main:
    → All above
    → Integration tests
    → Build Docker images (verify they build)

Merge to develop:
    → All above
    → Deploy to staging environment

Merge to main:
    → All above
    → Deploy to production
    → Post-deploy health check
    → Notify on failure

5.2 GitHub Actions Workflows
.github/workflows/test.yml
Runs on every push to any branch:
yamlname: Tests

on:
  push:
    branches: ['**']
  pull_request:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_USER: webguard_test
          POSTGRES_PASSWORD: test_password
          POSTGRES_DB: webguard_test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

      redis:
        image: redis:7-alpine
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      - name: Run database migrations
        env:
          DATABASE_URL: postgresql://webguard_test:test_password@localhost:5432/webguard_test
        run: alembic upgrade head

      - name: Run unit tests
        env:
          DATABASE_URL: postgresql://webguard_test:test_password@localhost:5432/webguard_test
          REDIS_URL: redis://localhost:6379/0
          SECRET_KEY: test-secret-key-for-ci-only-32chars
          ENVIRONMENT: test
        run: |
          pytest tests/unit/ \
            --cov=engine \
            --cov=api \
            --cov-report=xml \
            --cov-report=term-missing \
            -v

      - name: Run integration tests
        env:
          DATABASE_URL: postgresql://webguard_test:test_password@localhost:5432/webguard_test
          REDIS_URL: redis://localhost:6379/0
          SECRET_KEY: test-secret-key-for-ci-only-32chars
          ENVIRONMENT: test
        run: |
          pytest tests/integration/ -v

      - name: Upload coverage report
        uses: codecov/codecov-action@v4
        with:
          file: ./coverage.xml
          fail_ci_if_error: false

.github/workflows/lint.yml
Runs on every push:
yamlname: Lint and Type Check

on:
  push:
    branches: ['**']

jobs:
  lint:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install linting tools
        run: |
          pip install black flake8 mypy
          pip install -r requirements.txt

      - name: Check formatting with black
        run: black --check engine/ api/ cli/

      - name: Lint with flake8
        run: |
          flake8 engine/ api/ cli/ \
            --max-line-length=100 \
            --exclude=__pycache__,migrations

      - name: Type check with mypy
        run: |
          mypy engine/ api/ cli/ \
            --ignore-missing-imports \
            --strict

.github/workflows/security.yml
Runs on every push — dependency vulnerability scanning:
yamlname: Security Scan

on:
  push:
    branches: ['**']
  schedule:
    - cron: '0 8 * * 1'  # Every Monday morning

jobs:
  dependency-scan:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install safety and pip-audit
        run: pip install safety pip-audit

      - name: Run pip-audit
        run: pip-audit -r requirements.txt

      - name: Run safety check
        run: safety check -r requirements.txt --full-report

      - name: Scan for secrets
        uses: trufflesecurity/trufflehog@main
        with:
          path: ./
          base: ${{ github.event.repository.default_branch }}
          head: HEAD

.github/workflows/deploy.yml
Deploys on merge to main or develop:
yamlname: Deploy

on:
  push:
    branches:
      - main      # → Production
      - develop   # → Staging

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Determine environment
        id: env
        run: |
          if [ "${{ github.ref }}" == "refs/heads/main" ]; then
            echo "environment=production" >> $GITHUB_OUTPUT
            echo "server=${{ secrets.PROD_SERVER_IP }}" >> $GITHUB_OUTPUT
          else
            echo "environment=staging" >> $GITHUB_OUTPUT
            echo "server=${{ secrets.STAGING_SERVER_IP }}" >> $GITHUB_OUTPUT
          fi

      - name: Build and push Docker images
        env:
          DOCKER_USERNAME: ${{ secrets.DOCKER_USERNAME }}
          DOCKER_PASSWORD: ${{ secrets.DOCKER_PASSWORD }}
        run: |
          echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin

          docker build -t webguard/api:${{ github.sha }} \
            -f docker/Dockerfile.api .
          docker push webguard/api:${{ github.sha }}

          docker build -t webguard/worker:${{ github.sha }} \
            -f docker/Dockerfile.worker .
          docker push webguard/worker:${{ github.sha }}

          docker build -t webguard/web:${{ github.sha }} \
            -f docker/Dockerfile.web .
          docker push webguard/web:${{ github.sha }}

      - name: Deploy to server
        uses: appleboy/ssh-action@v1
        with:
          host: ${{ steps.env.outputs.server }}
          username: deploy
          key: ${{ secrets.DEPLOY_SSH_KEY }}
          script: |
            cd /opt/webguard
            export IMAGE_TAG=${{ github.sha }}
            docker compose pull
            docker compose up -d --no-deps api worker web
            docker compose exec -T api alembic upgrade head

      - name: Health check
        run: |
          sleep 15  # Wait for containers to start
          curl --fail https://${{ steps.env.outputs.server }}/api/v1/health \
            || (echo "Health check failed" && exit 1)

      - name: Notify on failure
        if: failure()
        uses: rtCamp/action-slack-notify@v2
        env:
          SLACK_WEBHOOK: ${{ secrets.SLACK_WEBHOOK }}
          SLACK_MESSAGE: "Deployment to ${{ steps.env.outputs.environment }} FAILED"
          SLACK_COLOR: danger

5.3 Required GitHub Secrets
Configure these in GitHub repository Settings → Secrets:
PROD_SERVER_IP          Production server IP address
STAGING_SERVER_IP       Staging server IP address
DEPLOY_SSH_KEY          SSH private key for deploy user
DOCKER_USERNAME         Docker Hub username
DOCKER_PASSWORD         Docker Hub password or access token
SLACK_WEBHOOK           Slack webhook URL for notifications (optional)

5.4 Branch Protection Rules
main branch:
✅ Require pull request before merging
✅ Require 1 approval
✅ Require status checks to pass:
   - Tests / test
   - Lint and Type Check / lint
   - Security Scan / dependency-scan
✅ Require branches to be up to date before merging
✅ Restrict direct pushes — nobody pushes directly to main
develop branch:
✅ Require pull request before merging
✅ Require status checks to pass:
   - Tests / test
   - Lint and Type Check / lint
✅ Allow direct pushes for repository owner only

6. Production Infrastructure
6.1 Recommended Server Configuration
For Version 1.0 launch:
Provider:     DigitalOcean (recommended) or AWS EC2
Droplet:      4GB RAM, 2 vCPUs, 80GB SSD
OS:           Ubuntu 24.04 LTS
Location:     Choose closest to primary user base

Managed Services:
  PostgreSQL: DigitalOcean Managed Database — PostgreSQL 16
              1GB RAM / 1 vCPU to start — scales independently
  Redis:      DigitalOcean Managed Redis
              1GB RAM to start
Why managed database and Redis?
Managed services handle backups, updates, failover, and scaling automatically. For a solo developer maintaining infrastructure manually while also building the product is unsustainable. The cost difference at small scale is minimal compared to the time saved.

6.2 Production Server Setup
Initial server configuration:
bash# Connect to server
ssh root@SERVER_IP

# Update packages
apt-get update && apt-get upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
apt-get install docker-compose-plugin

# Install Nginx
apt-get install nginx certbot python3-certbot-nginx

# Create deploy user (non-root for deployments)
adduser deploy
usermod -aG docker deploy
usermod -aG sudo deploy

# Create application directory
mkdir -p /opt/webguard
chown deploy:deploy /opt/webguard

# Configure firewall
ufw allow OpenSSH
ufw allow 'Nginx Full'
ufw enable

6.3 Nginx Configuration
/etc/nginx/sites-available/webguard:
nginx# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name webguard.io www.webguard.io api.webguard.io;
    return 301 https://$server_name$request_uri;
}

# Web Dashboard
server {
    listen 443 ssl http2;
    server_name webguard.io www.webguard.io;

    ssl_certificate /etc/letsencrypt/live/webguard.io/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/webguard.io/privkey.pem;

    # Mozilla Modern SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_timeout 1d;
    ssl_session_cache shared:MozSSL:10m;
    ssl_stapling on;
    ssl_stapling_verify on;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self';" always;

    # Serve React build
    root /opt/webguard/web/build;
    index index.html;

    # SPA routing — all routes serve index.html
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Cache static assets
    location /static/ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Gzip compression
    gzip on;
    gzip_types text/plain text/css application/javascript application/json;
}

# API Backend
server {
    listen 443 ssl http2;
    server_name api.webguard.io;

    ssl_certificate /etc/letsencrypt/live/api.webguard.io/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.webguard.io/privkey.pem;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;

    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # Request size limit
    client_max_body_size 1m;

    # Proxy to FastAPI
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 120s;
        proxy_connect_timeout 10s;
    }

    # WebSocket support for scan progress
    location /api/v1/ws/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_read_timeout 300s;
    }
}

6.4 SSL Certificate Setup
bash# Obtain certificates for all domains
certbot --nginx \
  -d webguard.io \
  -d www.webguard.io \
  -d api.webguard.io \
  --email security@webguard.io \
  --agree-tos \
  --non-interactive

# Verify auto-renewal
certbot renew --dry-run

# Certbot installs a systemd timer for automatic renewal
systemctl status certbot.timer

6.5 Production Docker Compose
/opt/webguard/docker-compose.yml (on production server):
yamlversion: '3.9'

services:

  api:
    image: webguard/api:${IMAGE_TAG}
    env_file: .env.production
    restart: unless-stopped
    volumes:
      - report_files:/app/reports/generated
    ports:
      - "127.0.0.1:8000:8000"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    logging:
      driver: "json-file"
      options:
        max-size: "50m"
        max-file: "5"

  worker:
    image: webguard/worker:${IMAGE_TAG}
    env_file: .env.production
    restart: unless-stopped
    volumes:
      - report_files:/app/reports/generated
    logging:
      driver: "json-file"
      options:
        max-size: "50m"
        max-file: "5"

volumes:
  report_files:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /opt/webguard/reports
Note: PostgreSQL and Redis are managed services in production — not Docker containers. The api and worker services connect to them via the environment variables in .env.production.

7. Deployment Procedure
7.1 First Deployment
Performed once when setting up the production server:
bash# On production server as deploy user
cd /opt/webguard

# Create production environment file
cp .env.example .env.production
nano .env.production
# Fill in all production values

# Create reports directory
mkdir -p reports

# Pull and start services
export IMAGE_TAG=latest
docker compose pull
docker compose up -d

# Run initial migrations
docker compose exec api alembic upgrade head

# Verify health
curl https://api.webguard.io/api/v1/health

7.2 Ongoing Deployments
Handled automatically by GitHub Actions deploy.yml on merge to main.
Manual deployment (if needed):
bash# On production server
cd /opt/webguard
export IMAGE_TAG=<commit-sha>

# Pull new images
docker compose pull

# Update services with zero downtime
docker compose up -d --no-deps api
docker compose up -d --no-deps worker

# Run migrations if any
docker compose exec api alembic upgrade head

# Verify
curl https://api.webguard.io/api/v1/health
docker compose ps

7.3 Rollback Procedure
If a deployment causes issues:
bash# On production server
cd /opt/webguard
export IMAGE_TAG=<previous-commit-sha>

# Roll back to previous image
docker compose up -d --no-deps api worker

# If migrations need rollback (only if the new migration was the problem)
docker compose exec api alembic downgrade -1

# Verify
curl https://api.webguard.io/api/v1/health

8. Monitoring and Observability
8.1 Application Health Monitoring
UptimeRobot (free tier):
Configure monitors for:
https://webguard.io                    ← Web dashboard
https://api.webguard.io/api/v1/health  ← API health check
Settings:

Check interval: 5 minutes
Alert contacts: email notification to security@webguard.io
Status page: public status page at status.webguard.io


8.2 Error Tracking — Sentry
Backend (FastAPI):
python# api/main.py

import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from sentry_sdk.integrations.celery import CeleryIntegration

if settings.SENTRY_DSN:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        integrations=[
            FastApiIntegration(),
            SqlalchemyIntegration(),
            CeleryIntegration(),
        ],
        traces_sample_rate=0.1,
        environment=settings.ENVIRONMENT,
        # Never send sensitive data to Sentry
        before_send=scrub_sensitive_data,
    )
Frontend (React):
javascript// web/src/index.js

import * as Sentry from "@sentry/react";

if (process.env.NODE_ENV === 'production') {
    Sentry.init({
        dsn: process.env.REACT_APP_SENTRY_DSN,
        environment: 'production',
        tracesSampleRate: 0.1,
    });
}
Sensitive data scrubbing:
pythondef scrub_sensitive_data(event, hint):
    # Remove Authorization headers from Sentry events
    if 'request' in event:
        headers = event['request'].get('headers', {})
        if 'Authorization' in headers:
            headers['Authorization'] = '[Filtered]'
    return event

8.3 Log Management
Log structure:
All application logs use structured JSON format:
python# api/config.py

import logging
import json

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            'timestamp': self.formatTime(record),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'environment': settings.ENVIRONMENT,
        }
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        return json.dumps(log_data)
Log levels by environment:
Development:  DEBUG  — all logs
Staging:      INFO   — info and above
Production:   WARNING — warnings and errors only
Log retention:
Docker logging driver retains 50MB per file, 5 files per container. Logs rotate automatically. For production applications requiring longer retention a log aggregation service (Papertrail, Logtail) can be added later.
What is always logged:
Security events     (login, logout, failures, key operations)
Scan submissions    (scan_id, user_id, url, profile)
Scan completions    (scan_id, duration, score, finding counts)
API errors          (status code, path, error code)
Worker errors       (scan_id, error message)
What is never logged:
Passwords (plain or hashed)
API key values
JWT tokens
Full Authorization header values
Database connection strings

8.4 Performance Monitoring
Key metrics to watch:
MetricThresholdActionAPI response time p95> 1 secondInvestigate slow queriesScan queue depth> 20 jobsScale worker countWorker scan duration> 10 minutesCheck for hanging scansDatabase connection pool> 80% utilizedScale databaseRedis memory> 80% utilizedIncrease Redis sizeDisk usage (reports)> 80%Archive or delete old reportsContainer memory> 85%Scale server
Check metrics:
bash# Container resource usage
docker stats

# Database connections
docker compose exec api python3 -c "
from api.database import engine
print(engine.pool.status())
"

# Redis info
docker compose exec redis redis-cli info memory
docker compose exec redis redis-cli llen celery

9. Backup and Recovery
9.1 Database Backup Strategy
Managed PostgreSQL automated backups:
DigitalOcean Managed Database performs daily automated backups with 7-day retention. These are point-in-time recovery backups managed entirely by the provider.
Manual backup (on demand):
bash# Create manual backup
pg_dump $DATABASE_URL \
  --format=custom \
  --compress=9 \
  --file=webguard_backup_$(date +%Y%m%d_%H%M%S).dump

# Verify backup integrity
pg_restore --list webguard_backup_*.dump | head -20
Backup storage:
Store manual backups in a separate location from the production server — object storage (DigitalOcean Spaces or AWS S3).

9.2 Report Files Backup
Report files (PDF, HTML, JSON) generated by scans are stored on the production server volume. Back up the /opt/webguard/reports directory:
bash# Daily rsync to backup storage
rsync -avz /opt/webguard/reports/ \
  backup-server:/backups/webguard/reports/

9.3 Disaster Recovery Procedure
Scenario: Production server completely lost
Recovery Time Objective (RTO): 4 hours
Recovery Point Objective (RPO): 24 hours (last backup)

Steps:

1. Provision new server (15 minutes)
   - Create new DigitalOcean Droplet
   - Run server setup script

2. Restore application (30 minutes)
   - Clone repository
   - Copy .env.production from secure storage
   - Pull latest Docker images
   - Start services

3. Restore database (30 minutes)
   - Managed PostgreSQL service is unaffected
   - Update DATABASE_URL in .env.production
   - Run alembic upgrade head

4. Restore report files (variable)
   - rsync from backup storage

5. Update DNS (15 minutes)
   - Point domain to new server IP
   - Obtain new SSL certificates

6. Verify (15 minutes)
   - Health check all endpoints
   - Test scan submission
   - Test report download

Total estimated recovery: 2-4 hours

9.4 Backup Testing
Backups are worthless if they cannot be restored. Test restoration monthly:
bash# Monthly backup restoration test procedure
# Run on staging environment — never on production

# 1. Create test database
createdb webguard_restore_test

# 2. Restore backup
pg_restore \
  --dbname=webguard_restore_test \
  --clean \
  --if-exists \
  webguard_backup_latest.dump

# 3. Verify row counts match production
psql webguard_restore_test -c "
SELECT
  (SELECT COUNT(*) FROM users) as users,
  (SELECT COUNT(*) FROM scans) as scans,
  (SELECT COUNT(*) FROM findings) as findings;
"

# 4. Drop test database
dropdb webguard_restore_test

10. Scaling Strategy
10.1 Vertical Scaling Triggers
Scale up the server when:
CPU sustained > 70% for 30 minutes
Memory sustained > 80%
Database connections > 80% of pool
10.2 Horizontal Scaling Path
When vertical scaling reaches its limits:
Phase 1 (Current)
└── Single server
    ├── API (Uvicorn, 4 workers)
    └── Celery (4 concurrent workers)

Phase 2 (When needed)
├── Load balancer
├── API server 1
├── API server 2
└── Worker server (dedicated)

Phase 3 (Future)
├── Load balancer
├── API server cluster (auto-scaling)
├── Worker cluster (scales with queue depth)
└── Read replica database

11. Development Workflow Summary
Daily workflow for a developer:

1. Start local environment
   make dev

2. Work on a feature
   git checkout -b feature/your-feature develop

3. Make changes — hot reload active in dev mode

4. Run tests locally before pushing
   make test

5. Push to GitHub
   git push origin feature/your-feature

6. GitHub Actions runs automatically
   → Lint check
   → Unit tests
   → Security scan

7. Open pull request to develop
   → Integration tests run
   → Code review (self-review for solo project)

8. Merge to develop
   → Automatically deployed to staging

9. Verify on staging

10. Open pull request from develop to main
    → Full test suite runs

11. Merge to main
    → Automatically deployed to production
    → Health check runs
    → Done

This document is version controlled. Infrastructure changes must be reflected here. Deployment procedure changes must be tested on staging before updating this document.
Last updated: May 2026
