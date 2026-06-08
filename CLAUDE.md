# CLAUDE.md — WebGuard Project Context

> You are an agent running inside Antigravity IDE, working on **WebGuard**: a passive OWASP Top 10
> web vulnerability scanner with a CLI tool and web dashboard. Read this file fully before acting
> on any task. All decisions here are final unless explicitly revised by the developer.

---

## Project overview

**WebGuard** automates OWASP Top 10 2025 vulnerability scanning and turns complex security findings
into clear, actionable reports for developers, SMB owners, and security consultants.

- **Scanning approach:** Passive only — no payload injection, no active probing. This is a
  deliberate strategic and legal decision, not a limitation.
- **Interfaces:** CLI tool + web dashboard, sharing a single core engine.
- **Scan profiles:** Quick (~30–60 s), Standard (~1–3 min), Deep (~3–6 min).
- **Primary audiences:** Daniel (Developer), Sarah (SMB Owner), Amara (Security Consultant).
- **Guiding principles:** Professionalism, logic, realism, idealism.

---

## Repository

- **Platform:** GitHub
- **Branches:** `main` → `develop` → `feature/*` → merge via PR
- **Commit style:** Conventional commits — `feat:`, `fix:`, `refactor:`, `docs:`, `test:`,
  `chore:`, `ci:`
- **Dev environment:** Kali Linux
- **Phase:** Phase 2 — active development (documentation phase complete and merged)

---

## Tech stack

| Layer | Technology |
|---|---|
| Language | Python 3.11+ |
| API framework | FastAPI |
| Task queue | Celery + Redis |
| Database | PostgreSQL |
| ORM / migrations | SQLAlchemy + Alembic |
| CLI | Typer + Rich |
| Frontend | React + Tailwind CSS |
| PDF reports | WeasyPrint + Jinja2 |
| Containerisation | Docker + Docker Compose |
| CI/CD | GitHub Actions |
| Production hosting | DigitalOcean |

---

## Architecture decisions

### ADR-001 — CLI dual-mode design
Full document: `docs/technical/decisions/ADR-001-cli-engine-mode.md`

The CLI operates in two modes:

| Mode | Trigger | Behaviour |
|---|---|---|
| **Offline** | No `--api-key` flag / no env var | Calls the core engine directly in-process |
| **Connected** | `--api-key` provided or `WEBGUARD_API_KEY` set | Calls the FastAPI backend via HTTP |

Both modes produce identical output. The offline mode has no network dependency beyond the target
URL being scanned. Never collapse these two modes into one code path.

---

## Project directory structure

```
webguard/
├── CLAUDE.md                    ← this file
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── SECURITY.md
├── .gitignore
│
├── .github/
│   ├── PULL_REQUEST_TEMPLATE.md
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   └── workflows/               ← GitHub Actions CI/CD (to be populated)
│
├── engine/                      ← core scanning engine (shared by CLI + API)
│   ├── __init__.py
│   ├── models.py                ← dataclasses, enums, result types
│   ├── base_check.py            ← BaseCheck abstract class
│   ├── url_validator.py         ← URL normalisation and validation
│   ├── orchestrator.py          ← runs all checks, collects findings
│   ├── scorer.py                ← 6-dimension scoring engine
│   ├── reporter.py              ← JSON / HTML / PDF output
│   └── checks/                  ← one module per OWASP Top 10 2025 item
│       ├── __init__.py
│       ├── a01_broken_access_control.py
│       ├── a02_security_misconfiguration.py
│       ├── a03_supply_chain_failures.py
│       ├── a04_cryptographic_failures.py
│       ├── a05_injection.py
│       ├── a06_insecure_design.py
│       ├── a07_auth_failures.py
│       ├── a08_data_integrity_failures.py
│       ├── a09_logging_failures.py
│       └── a10_exceptional_conditions.py
│
├── cli/                         ← Typer + Rich CLI (ADR-001: offline + connected modes)
│   ├── __init__.py
│   ├── main.py
│   ├── commands/
│   │   ├── scan.py
│   │   ├── report.py
│   │   └── config.py
│   └── display/
│       ├── progress.py
│       └── results.py
│
├── api/                         ← FastAPI backend
│   ├── __init__.py
│   ├── main.py
│   ├── dependencies.py
│   ├── models/                  ← SQLAlchemy ORM models + Alembic migrations
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── session.py
│   │   ├── user.py
│   │   ├── api_key.py
│   │   ├── scan.py
│   │   ├── finding.py
│   │   ├── dimension_score.py
│   │   ├── report.py
│   │   └── migrations/
│   │       ├── env.py
│   │       └── versions/
│   ├── routes/                  ← FastAPI routers
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── scans.py
│   │   ├── reports.py
│   │   ├── keys.py
│   │   ├── dashboard.py
│   │   └── health.py
│   ├── schemas/                 ← Pydantic request/response schemas
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── scan.py
│   │   └── report.py
│   ├── services/                ← business logic layer
│   │   ├── __init__.py
│   │   ├── scan_service.py
│   │   ├── report_service.py
│   │   └── auth_service.py
│   └── workers/                 ← Celery task definitions
│       ├── __init__.py
│       └── scan_tasks.py
│
├── web/                         ← React + Tailwind CSS dashboard
│   └── src/
│       ├── main.jsx
│       ├── App.jsx
│       ├── components/          ← reusable UI components
│       ├── pages/               ← route-level page components
│       ├── services/            ← API client / data-fetching layer
│       └── utils/               ← helper functions, constants
│
├── reports/                     ← generated report output directory (git-ignored)
│   └── templates/               ← Jinja2 templates for HTML + PDF reports
│       ├── report_html.html.j2
│       ├── report_pdf.html.j2
│       └── assets/              ← CSS, images bundled into self-contained reports
│
├── tests/
│   ├── unit/
│   │   └── checks/              ← one test file per check module
│   ├── integration/             ← API endpoint integration tests
│   └── fixtures/
│       └── mock_responses/      ← recorded HTTP response fixtures
│
└── docs/                        ← completed pre-development documentation
    ├── legal/
    │   ├── terms-of-service.md
    │   ├── privacy-policy.md
    │   ├── acceptable-use-policy.md
    │   └── responsible-disclosure.md
    ├── project/
    │   ├── charter.md
    │   ├── vision-and-scope.md
    │   ├── requirements.md      ← authoritative PRD — all features traced here
    │   ├── user-personas.md
    │   ├── roadmap.md
    │   └── risk-register.md
    ├── research/
    │   ├── market-research.md
    │   ├── competitor-analysis.md
    │   ├── technical-feasibility.md
    │   └── owasp/               ← per-category passive signal research
    │       ├── a01-broken-access-control.md
    │       ├── a02-security-misconfiguration.md
    │       ├── a03-software-supply-chain-failures.md
    │       ├── a04-cryptographic-failures.md
    │       ├── a05-injection.md
    │       ├── a06-insecure-design.md
    │       ├── a07-authentication-failures.md
    │       ├── a08-software-data-integrity-failures.md
    │       ├── a09-security-logging-alerting-failures.md
    │       ├── a10-mishandling-exceptional-conditions.md
    │       └── dns-security-supplementary.md
    ├── technical/
    │   ├── architecture.md
    │   ├── database-schema.md
    │   ├── api-reference.md
    │   ├── security-design.md
    │   ├── devops-plan.md
    │   └── decisions/
    │       └── ADR-001-cli-engine-mode.md
    └── user-guides/
        ├── installation.md
        ├── cli-guide.md
        └── web-app-guide.md
```

---

## User personas

| Persona | Role | Primary needs |
|---|---|---|
| **Daniel Ochieng** | Developer | CLI tool, pipeline integration, fast scans, JSON output |
| **Sarah Wanjiku** | SMB Owner | Web dashboard, plain English reports, PDF export, scoring |
| **Amara Diallo** | Security Consultant | Accurate findings, professional PDF, multi-target, CLI |

---

## Scan profiles

| Profile | Scope | Target duration |
|---|---|---|
| **Quick** | Transport security, security headers, SSL certificate | 30–60 seconds |
| **Standard** | All Quick + cookie security, info disclosure, CORS, DNS, sensitive files, content/protocol | 1–3 minutes |
| **Deep** | All Standard + component safety (CVE API lookup) | 3–6 minutes |

Default profile when none specified: **Standard**.

---

## Database schema

All tables use UUID primary keys. Never use integer IDs.
Alembic migrations live in `api/models/migrations/`.

| Table | Purpose |
|---|---|
| `users` | Dashboard accounts |
| `api_keys` | CLI connected-mode authentication |
| `scans` | Scan job records |
| `findings` | Individual vulnerability findings |
| `dimension_scores` | Per-dimension scores for a scan |
| `reports` | Generated report metadata |

---

## Scoring system

Scores range **0.0 – 10.0** (one decimal place). Higher = more secure. Grades A–F.
Each dimension starts at 10.0; deductions are applied per finding; the floor is 0.0.

### Severity deductions

| Severity | Deduction |
|---|---|
| Critical | −3.0 |
| High | −2.0 |
| Medium | −1.0 |
| Low | −0.5 |
| Info | 0.0 |

### Dimension weights

| Dimension | Weight |
|---|---|
| Transport Security | 25% |
| Header Configuration | 20% |
| Cookie Security | 20% |
| Component Safety | 15% |
| Information Exposure | 10% |
| DNS Security | 10% |

### Grade thresholds

| Grade | Label | Score range |
|---|---|---|
| A | Excellent | 9.0 – 10.0 |
| B | Good | 7.5 – 8.9 |
| C | Fair | 6.0 – 7.4 |
| D | Poor | 4.0 – 5.9 |
| F | Critical | 0.0 – 3.9 |

---

## OWASP Top 10 2025 check mapping

Each check module is passive — it inspects HTTP responses, headers, cookies, TLS metadata,
DNS records, and public component manifests. No payloads are injected. No forms are submitted.

| ID | Category | Passive signals inspected |
|---|---|---|
| A01 | Broken Access Control | Security headers, directory listing indicators, overly permissive CORS |
| A02 | Security Misconfiguration | Server headers, error page verbosity, default files, missing security headers |
| A03 | Software Supply Chain Failures | Detectable library versions, SRI absence on external scripts |
| A04 | Cryptographic Failures | TLS version, cipher suites, HSTS, mixed content, HTTP→HTTPS redirect |
| A05 | Injection | CSP header quality, response content sniffing signals |
| A06 | Insecure Design | Missing security headers, permissive CORS, weak cookie policy patterns |
| A07 | Authentication Failures | Cookie flags (Secure, HttpOnly, SameSite), login page signals |
| A08 | Software and Data Integrity Failures | SRI missing on external scripts, CSP lacks integrity directive |
| A09 | Security Logging and Alerting Failures | No observable signal (noted in report as unverifiable passively) |
| A10 | Mishandling of Exceptional Conditions | Open redirect indicators in response headers, error verbosity |

Research notes for each category: `docs/research/owasp/`

---

## Functional check modules

The engine implements named functional checks (not one-to-one with OWASP IDs). Each maps to one
or more OWASP categories and one scoring dimension:

| Check | Profile | Scoring dimension | Key OWASP categories |
|---|---|---|---|
| Transport Security | Quick | Transport Security | A04 |
| SSL Certificate | Quick | Transport Security | A04 |
| Security Headers | Quick | Header Configuration | A02, A06 |
| Cookie Security | Standard | Cookie Security | A07 |
| Information Disclosure | Standard | Information Exposure | A02, A05 |
| CORS Configuration | Standard | Header Configuration | A01, A06 |
| DNS Security | Standard | DNS Security | A02 |
| Sensitive File Exposure | Standard | Information Exposure | A02 |
| Content and Protocol | Standard | Transport Security | A04, A08 |
| Component Safety | Deep | Component Safety | A03 |

---

## Core engine contracts

### BaseCheck (engine/base_check.py)
Every check module must implement this interface:

```python
from abc import ABC, abstractmethod
from engine.models import CheckResult, ScanTarget

class BaseCheck(ABC):
    owasp_id: str        # e.g. "A04"
    owasp_name: str      # e.g. "Cryptographic Failures"
    dimension: str       # one of the 6 scoring dimensions

    @abstractmethod
    def run(self, target: ScanTarget) -> CheckResult:
        ...
```

### ScanTarget (engine/models.py)
Passed to every check. Contains the full HTTP response data — never re-fetches.

```python
@dataclass
class ScanTarget:
    url: str
    response_headers: dict[str, str]
    cookies: list[dict]
    tls_info: TLSInfo | None
    dns_records: dict[str, list[str]]
    response_body_snippet: str   # first 4KB only
    status_code: int
```

### CheckResult (engine/models.py)

```python
@dataclass
class CheckResult:
    owasp_id: str
    owasp_name: str
    dimension: str
    passed: bool
    severity: Severity        # INFO, LOW, MEDIUM, HIGH, CRITICAL
    title: str
    description: str
    business_impact: str
    recommendation: str
    effort: str               # Low, Medium, High
    evidence: dict            # raw values that triggered the finding
    references: list[str]     # OWASP links
```

---

## Code style and conventions

- **Formatter:** Black (line length 88)
- **Linter:** Ruff
- **Type checker:** Mypy (strict mode)
- **All public functions and classes must have docstrings**
- **Type hints on every function signature — no bare `Any`**
- **No print statements** — use Rich console in CLI, Python `logging` in engine and API
- **No hardcoded secrets** — all config via environment variables, loaded through `config.py`
- **Test file naming:** `test_<module>.py`, one test file per source module
- **Imports:** absolute imports only; no relative imports outside the same package
- **Test coverage target:** minimum 80% on core engine modules

---

## Build order (Phase 2)

Complete and commit each step before starting the next. Each step maps to a feature branch.

| Step | Deliverable | Branch |
|---|---|---|
| 1 | Python env and project config (`pyproject.toml`, `Makefile`, `.env.example`, `docker-compose.yml`) | `feature/project-setup` |
| 2 | Base data models (`engine/models.py`) | `feature/engine-models` |
| 3 | BaseCheck abstract class (`engine/base_check.py`) | `feature/base-check` |
| 4 | URL validator (`engine/url_validator.py`) | `feature/url-validator` |
| 5 | Check modules × 10 (A01–A10) + orchestrator | `feature/checks` |
| 6 | Scoring engine (`engine/scorer.py`) | `feature/scorer` |
| 7 | Reporter — JSON, HTML, PDF (`engine/reporter.py` + `reports/templates/`) | `feature/reporter` |
| 8 | CLI tool (`cli/`) | `feature/cli` |
| 9 | API backend (`api/`) | `feature/api` |
| 10 | Web dashboard (`web/`) | `feature/frontend` |

---

## Environment variables

All configuration is loaded from environment variables. Never hardcode values.

```
# Core
WEBGUARD_ENV=development          # development | production
WEBGUARD_SECRET_KEY=              # JWT signing key
WEBGUARD_API_KEY=                 # CLI connected-mode key (client-side)

# Database
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/webguard

# Redis / Celery
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/1

# Scanning limits
MAX_SCAN_TIMEOUT=30               # seconds
MAX_RESPONSE_BODY_BYTES=4096

# Reporting
REPORT_OUTPUT_DIR=./reports

# External APIs (Deep profile only)
NVD_API_KEY=                      # optional — increases NVD rate limit
```

---

## What to never do

- **Never inject payloads** into target URLs, forms, or parameters — passive scanning only.
- **Never use integer primary keys** — all database IDs are UUIDs.
- **Never hardcode secrets, URLs, or credentials** in source files.
- **Never collapse CLI offline and connected modes** into a single code path (ADR-001).
- **Never use `print()`** in engine, API, or CLI code — use logging or Rich.
- **Never skip type hints** on public interfaces.
- **Never skip `business_impact` or `effort`** on a CheckResult — both are required fields.
- **Never start the next build step** until the current step is committed and tests pass.
- **Never scan private IP ranges** (10.x, 192.168.x, 172.16–31.x) or localhost.
