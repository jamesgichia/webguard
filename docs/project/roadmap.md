# WebGuard v1.0 — Development Roadmap

| | |
|---|---|
| **Document** | Development Roadmap |
| **Version** | 1.0 |
| **Status** | Active |
| **Created** | June 2026 |
| **Author** | James Gichia |
| **Repository** | `docs/project/roadmap.md` |

---

## Phase Overview

| Phase | Focus | Steps | Status |
|---|---|---|---|
| 1 | Project Foundation | 1 | ⏳ Next |
| 2 | Core Engine | 2–5 | ⬜ Pending |
| 3 | CLI Tool | 6 | ⬜ Pending |
| 4 | API Backend | 7 | ⬜ Pending |
| 5 | Web Dashboard | 8 | ⬜ Pending |
| 6 | QA, Hardening & Launch | — | ⬜ Pending |

---

## Phase 1 — Project Foundation

**Branch:** `feature/project-setup`
**Goal:** A working, fully configured Python project that any subsequent step can build on.

### Deliverables
- `pyproject.toml` — package metadata, pinned dependencies, Black/Ruff/Mypy config
- `Makefile` — developer shortcuts (`make lint`, `make test`, `make run`)
- `.env.example` — all environment variables documented
- `docker-compose.yml` — PostgreSQL + Redis + API + Celery + Web
- `Dockerfile` — production image
- `.pre-commit-config.yaml` — Black, Ruff, Mypy hooks
- `.github/workflows/ci.yml` — lint + test on every push and PR
- Package stubs: `engine/__init__.py`, `cli/__init__.py`, `api/__init__.py`

### Acceptance Gate
- [ ] `make lint` passes with zero errors
- [ ] `make test` runs (empty suite passes)
- [ ] `docker-compose up` starts all services without errors
- [ ] Pre-commit hooks fire on a test commit

---

## Phase 2 — Core Engine

> The engine is built in strict sequential order. Each step depends on the previous.

### Step 2 — Data Models
**Branch:** `feature/engine-models`

Defines all shared data structures used by every component:
`ScanTarget`, `Finding`, `ScanResult`, `DimensionScore`, `ScanScore`, and all enums
(`Severity`, `ScanProfile`, `OWASPCategory`, `ScoringDimension`).

**References:** `requirements.md FR-013, FR-014`

**Acceptance Gate:**
- [ ] All dataclasses instantiate without error
- [ ] All enums contain correct values
- [ ] Unit tests pass

---

### Step 3 — BaseCheck + URL Validator
**Branch:** `feature/base-check`

Defines the `BaseCheck` abstract class (the contract every check module must fulfil)
and the `validate_scan_target()` function (applied to all URL inputs across all interfaces).

**References:** `requirements.md FR-001`, `CLAUDE.md — Core engine contracts`

**Acceptance Gate:**
- [ ] `BaseCheck` cannot be instantiated directly
- [ ] 15+ URL validation test cases pass (valid, malformed, private IPs, localhost, protocols)
- [ ] `make lint` passes

---

### Step 4 — The Ten Check Modules
**Branch:** `feature/checks`

Ten passive check modules, each a concrete subclass of `BaseCheck`:

| Module | Profile | Key Requirement |
|---|---|---|
| Transport Security | Quick | FR-003 |
| SSL Certificate | Quick | FR-004 |
| Security Headers | Quick | FR-005 |
| Cookie Security | Standard | FR-006 |
| Information Disclosure | Standard | FR-007 |
| CORS Configuration | Standard | FR-008 |
| DNS Security | Standard | FR-009 |
| Sensitive File Exposure | Standard | FR-010 |
| Content and Protocol | Standard | FR-011 |
| Component Safety (CVE) | Deep | FR-012 |

**Acceptance Gate:**
- [ ] All 10 modules implement `BaseCheck` correctly
- [ ] Every module has pass and fail unit test cases
- [ ] `make test tests/unit/checks/` → 100% pass
- [ ] Zero bare `except` clauses

---

### Step 5 — Orchestrator, Scorer, Reporter
**Branch:** `feature/engine-core`

Completes the engine:
- **Orchestrator** — runs all applicable checks concurrently via `asyncio.gather()`
- **Scorer** — applies severity deductions, computes weighted overall score and grade
- **Reporter** — generates JSON, HTML (Jinja2), and PDF (WeasyPrint) outputs
- **Templates** — `reports/templates/report_html.html.j2` and `report_pdf.html.j2`

**References:** `requirements.md FR-002, FR-013, FR-015, FR-016, FR-017`

**Acceptance Gate:**
- [ ] Orchestrator runs all 10 checks against a test fixture without crashing
- [ ] Scorer results verified against 3+ manual calculation cases
- [ ] JSON report is valid and contains all required fields
- [ ] HTML report renders in Chrome without external dependencies
- [ ] PDF generates successfully under 30 seconds
- [ ] Engine test coverage ≥ 80%

---

## Phase 3 — CLI Tool

**Branch:** `feature/cli`
**References:** `requirements.md FR-018 through FR-021`, `ADR-001`

Installable CLI tool with offline mode (calls engine directly) and connected mode
(calls API via `--api-key`). Full Rich terminal output.

### Key Commands
```bash
webguard scan <URL> [--profile quick|standard|deep] [--format json|html|pdf]
webguard scan <URL> --api-key KEY    # connected mode
webguard list-checks
webguard config set <key> <value>
webguard --version
```

### Acceptance Gate
- [ ] `pip install -e .` then `webguard --version` works
- [ ] All commands in FR-019 execute without error
- [ ] Offline mode completes a scan against a real test URL
- [ ] `--no-color` produces clean CI-safe output
- [ ] Unit tests pass

---

## Phase 4 — API Backend

**Branch:** `feature/api`
**References:** `requirements.md FR-022 through FR-030`, `architecture.md §5.3, §5.4`

Complete FastAPI backend with JWT authentication, Celery scan workers, PostgreSQL
storage, and all 17 required API endpoints.

### Endpoints Summary
- Auth: register, login, refresh, logout
- Scans: submit, list, get, status, delete
- Reports: JSON, HTML, PDF download
- Dashboard: statistics
- Keys: generate, list, revoke
- Health check

### Acceptance Gate
- [ ] All services healthy via `docker-compose up`
- [ ] `alembic upgrade head` runs without error
- [ ] All 17 endpoints return correct responses per integration tests
- [ ] JWT authentication enforced on protected routes
- [ ] Rate limiting tested (429 on exceeded limits)
- [ ] Scan job completes end-to-end via API
- [ ] Swagger docs at `/docs`

---

## Phase 5 — Web Dashboard

**Branch:** `feature/frontend`
**References:** `requirements.md FR-031 through FR-039`, `architecture.md §5.5`

React + Tailwind CSS dashboard with all 10 required pages.

### Pages
| Page | Route |
|---|---|
| Landing | `/` |
| Register / Login | `/register`, `/login` |
| Dashboard | `/dashboard` |
| New Scan | `/scan/new` |
| Scan Progress | `/scan/:id/progress` |
| Scan Results | `/scan/:id` |
| Scan History | `/history` |
| API Keys | `/keys` |
| Settings | `/settings` |

### Acceptance Gate
- [ ] All 10 pages render without errors
- [ ] Full scan completable end-to-end from the browser
- [ ] Scan progress polls automatically — no manual refresh
- [ ] PDF and HTML report download works
- [ ] All pages responsive at 375px minimum
- [ ] Tested in Chrome and Firefox

---

## Phase 6 — QA, Hardening & Launch

**Branch:** `feature/qa` → `develop` → `main`

### QA Checklist
- [ ] All 10 checks tested against OWASP Juice Shop
- [ ] All 10 checks tested against DVWA
- [ ] Zero confirmed false positives
- [ ] Engine test coverage ≥ 80% confirmed
- [ ] WebGuard scanned against its own domain — zero critical self-findings
- [ ] All P1 requirements from PRD met
- [ ] All P2 requirements from PRD met
- [ ] Sentry error monitoring active

### Deployment
- [ ] DigitalOcean infrastructure provisioned (per `docs/technical/devops-plan.md`)
- [ ] HTTPS enforced in production
- [ ] PostgreSQL automated backups enabled (7-day retention)
- [ ] Dependabot enabled
- [ ] Package published to PyPI as `webguard`

---

## Dependency Chain

```
Phase 1 (Foundation)
    └── Step 2 (Data Models)
            └── Step 3 (BaseCheck + Validator)
                    └── Step 4 (Ten Check Modules)
                            └── Step 5 (Orchestrator + Scorer + Reporter)
                                    ├── Phase 3 (CLI)
                                    └── Phase 4 (API)
                                                └── Phase 5 (Web Dashboard)
                                                            └── Phase 6 (QA + Launch)
```

Each step is a gate. Nothing downstream starts until the upstream step is committed,
tested, and merged.

---

*This roadmap is version controlled. Update status markers as each step completes.*
*Last updated: June 2026*
