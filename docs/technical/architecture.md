WebGuard — System Architecture Document
Document: System Architecture
Version: 1.0
Status: Draft
Created: May 2026
Author: James Gichia
Repository: docs/technical/architecture.md

1. Document Purpose
This document describes the complete technical architecture of WebGuard Version 1.0. It defines all system components, their responsibilities, how they communicate, how data flows through the system, and the technology decisions that underpin every layer.
This document is the primary reference for all implementation work. Every module built during Phase 2 through Phase 5 traces back to a specification in this document.

2. Architectural Principles
These principles guided every architectural decision:
Separation of concerns
The core engine has zero knowledge of how its results will be consumed. The CLI, API, and web dashboard are consumers — the engine is the producer. They never mix.
Engine independence
The scanning engine runs identically whether called by the CLI directly or by a Celery worker via the API. No interface-specific logic ever enters the engine.
Graceful degradation
External dependencies — the NVD API, OSV API, DNS resolvers — are optional. If they are unavailable the scan completes with reduced coverage and clearly notes which checks were inconclusive. The system never fails completely because one external service is unavailable.
Async by design
Scans are inherently IO-bound — making HTTP requests, querying DNS, calling CVE APIs. All check modules are async. Concurrency is built in at the architectural level, not added later.
Security of the scanner itself
WebGuard handles URLs submitted by users and makes outbound HTTP requests. The architecture must prevent misuse — scanning internal networks, SSRF via the scan engine itself, and unauthorized access to other users' results.
Simplicity over cleverness
This is a solo developer project. Every architectural choice favors the simplest solution that meets the requirements over the most sophisticated solution that impresses nobody.

3. System Context (Level 0 DFD)
The context diagram shows WebGuard as a single system and its interactions with external entities.
#mermaid-r2bs{font-family:inherit;font-size:16px;fill:#E5E5E5;}@keyframes edge-animation-frame{from{stroke-dashoffset:0;}}@keyframes dash{to{stroke-dashoffset:0;}}#mermaid-r2bs .edge-animation-slow{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 50s linear infinite;stroke-linecap:round;}#mermaid-r2bs .edge-animation-fast{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 20s linear infinite;stroke-linecap:round;}#mermaid-r2bs .error-icon{fill:#CC785C;}#mermaid-r2bs .error-text{fill:#3387a3;stroke:#3387a3;}#mermaid-r2bs .edge-thickness-normal{stroke-width:1px;}#mermaid-r2bs .edge-thickness-thick{stroke-width:3.5px;}#mermaid-r2bs .edge-pattern-solid{stroke-dasharray:0;}#mermaid-r2bs .edge-thickness-invisible{stroke-width:0;fill:none;}#mermaid-r2bs .edge-pattern-dashed{stroke-dasharray:3;}#mermaid-r2bs .edge-pattern-dotted{stroke-dasharray:2;}#mermaid-r2bs .marker{fill:#A1A1A1;stroke:#A1A1A1;}#mermaid-r2bs .marker.cross{stroke:#A1A1A1;}#mermaid-r2bs svg{font-family:inherit;font-size:16px;}#mermaid-r2bs p{margin:0;}#mermaid-r2bs .label{font-family:inherit;color:#E5E5E5;}#mermaid-r2bs .cluster-label text{fill:#3387a3;}#mermaid-r2bs .cluster-label span{color:#3387a3;}#mermaid-r2bs .cluster-label span p{background-color:transparent;}#mermaid-r2bs .label text,#mermaid-r2bs span{fill:#E5E5E5;color:#E5E5E5;}#mermaid-r2bs .node rect,#mermaid-r2bs .node circle,#mermaid-r2bs .node ellipse,#mermaid-r2bs .node polygon,#mermaid-r2bs .node path{fill:transparent;stroke:#A1A1A1;stroke-width:1px;}#mermaid-r2bs .rough-node .label text,#mermaid-r2bs .node .label text,#mermaid-r2bs .image-shape .label,#mermaid-r2bs .icon-shape .label{text-anchor:middle;}#mermaid-r2bs .node .katex path{fill:#000;stroke:#000;stroke-width:1px;}#mermaid-r2bs .rough-node .label,#mermaid-r2bs .node .label,#mermaid-r2bs .image-shape .label,#mermaid-r2bs .icon-shape .label{text-align:center;}#mermaid-r2bs .node.clickable{cursor:pointer;}#mermaid-r2bs .root .anchor path{fill:#A1A1A1!important;stroke-width:0;stroke:#A1A1A1;}#mermaid-r2bs .arrowheadPath{fill:#0b0b0b;}#mermaid-r2bs .edgePath .path{stroke:#A1A1A1;stroke-width:1px;}#mermaid-r2bs .flowchart-link{stroke:#A1A1A1;fill:none;}#mermaid-r2bs .edgeLabel{background-color:transparent;text-align:center;}#mermaid-r2bs .edgeLabel p{background-color:transparent;}#mermaid-r2bs .edgeLabel rect{opacity:0.5;background-color:transparent;fill:transparent;}#mermaid-r2bs .labelBkg{background-color:rgba(0, 0, 0, 0.5);}#mermaid-r2bs .cluster rect{fill:#CC785C;stroke:hsl(15, 12.3364485981%, 48.0392156863%);stroke-width:1px;}#mermaid-r2bs .cluster text{fill:#3387a3;}#mermaid-r2bs .cluster span{color:#3387a3;}#mermaid-r2bs div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:inherit;font-size:12px;background:#CC785C;border:1px solid hsl(15, 12.3364485981%, 48.0392156863%);border-radius:2px;pointer-events:none;z-index:100;}#mermaid-r2bs .flowchartTitleText{text-anchor:middle;font-size:18px;fill:#E5E5E5;}#mermaid-r2bs rect.text{fill:none;stroke-width:0;}#mermaid-r2bs .icon-shape,#mermaid-r2bs .image-shape{background-color:transparent;text-align:center;}#mermaid-r2bs .icon-shape p,#mermaid-r2bs .image-shape p{background-color:transparent;padding:2px;}#mermaid-r2bs .icon-shape .label rect,#mermaid-r2bs .image-shape .label rect{opacity:0.5;background-color:transparent;fill:transparent;}#mermaid-r2bs .label-icon{display:inline-block;height:1em;overflow:visible;vertical-align:-0.125em;}#mermaid-r2bs .node .label-icon path{fill:currentColor;stroke:revert;stroke-width:revert;}#mermaid-r2bs .node .neo-node{stroke:#A1A1A1;}#mermaid-r2bs [data-look="neo"].node rect,#mermaid-r2bs [data-look="neo"].cluster rect,#mermaid-r2bs [data-look="neo"].node polygon{stroke:url(#mermaid-r2bs-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#mermaid-r2bs [data-look="neo"].node path{stroke:url(#mermaid-r2bs-gradient);stroke-width:1px;}#mermaid-r2bs [data-look="neo"].node .outer-path{filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#mermaid-r2bs [data-look="neo"].node .neo-line path{stroke:#A1A1A1;filter:none;}#mermaid-r2bs [data-look="neo"].node circle{stroke:url(#mermaid-r2bs-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#mermaid-r2bs [data-look="neo"].node circle .state-start{fill:#000000;}#mermaid-r2bs [data-look="neo"].icon-shape .icon{fill:url(#mermaid-r2bs-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#mermaid-r2bs [data-look="neo"].icon-shape .icon-neo path{stroke:url(#mermaid-r2bs-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#mermaid-r2bs :root{--mermaid-font-family:inherit;}URL + profile via CLI orAPIURL + profile via WebDashboardURL + profile via CLI orAPIScan results + PDF reportScan results + PDF reportScan results + PDF reportVersion lookupVersion lookupCVE dataCVE dataDNS queriesDNS recordsPassive HTTP requestsHTTP responses + headersDeveloper / DanielBusiness User / SarahConsultant / AmaraNVD APInvd.nist.govOSV APIosv.devDNS ResolversTarget WebsiteWebGuard System

4. System Components (Level 1 Architecture)
The system decomposes into six major components. Each has a single clear responsibility.
#mermaid-r2bt{font-family:inherit;font-size:16px;fill:#E5E5E5;}@keyframes edge-animation-frame{from{stroke-dashoffset:0;}}@keyframes dash{to{stroke-dashoffset:0;}}#mermaid-r2bt .edge-animation-slow{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 50s linear infinite;stroke-linecap:round;}#mermaid-r2bt .edge-animation-fast{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 20s linear infinite;stroke-linecap:round;}#mermaid-r2bt .error-icon{fill:#CC785C;}#mermaid-r2bt .error-text{fill:#3387a3;stroke:#3387a3;}#mermaid-r2bt .edge-thickness-normal{stroke-width:1px;}#mermaid-r2bt .edge-thickness-thick{stroke-width:3.5px;}#mermaid-r2bt .edge-pattern-solid{stroke-dasharray:0;}#mermaid-r2bt .edge-thickness-invisible{stroke-width:0;fill:none;}#mermaid-r2bt .edge-pattern-dashed{stroke-dasharray:3;}#mermaid-r2bt .edge-pattern-dotted{stroke-dasharray:2;}#mermaid-r2bt .marker{fill:#A1A1A1;stroke:#A1A1A1;}#mermaid-r2bt .marker.cross{stroke:#A1A1A1;}#mermaid-r2bt svg{font-family:inherit;font-size:16px;}#mermaid-r2bt p{margin:0;}#mermaid-r2bt .label{font-family:inherit;color:#E5E5E5;}#mermaid-r2bt .cluster-label text{fill:#3387a3;}#mermaid-r2bt .cluster-label span{color:#3387a3;}#mermaid-r2bt .cluster-label span p{background-color:transparent;}#mermaid-r2bt .label text,#mermaid-r2bt span{fill:#E5E5E5;color:#E5E5E5;}#mermaid-r2bt .node rect,#mermaid-r2bt .node circle,#mermaid-r2bt .node ellipse,#mermaid-r2bt .node polygon,#mermaid-r2bt .node path{fill:transparent;stroke:#A1A1A1;stroke-width:1px;}#mermaid-r2bt .rough-node .label text,#mermaid-r2bt .node .label text,#mermaid-r2bt .image-shape .label,#mermaid-r2bt .icon-shape .label{text-anchor:middle;}#mermaid-r2bt .node .katex path{fill:#000;stroke:#000;stroke-width:1px;}#mermaid-r2bt .rough-node .label,#mermaid-r2bt .node .label,#mermaid-r2bt .image-shape .label,#mermaid-r2bt .icon-shape .label{text-align:center;}#mermaid-r2bt .node.clickable{cursor:pointer;}#mermaid-r2bt .root .anchor path{fill:#A1A1A1!important;stroke-width:0;stroke:#A1A1A1;}#mermaid-r2bt .arrowheadPath{fill:#0b0b0b;}#mermaid-r2bt .edgePath .path{stroke:#A1A1A1;stroke-width:1px;}#mermaid-r2bt .flowchart-link{stroke:#A1A1A1;fill:none;}#mermaid-r2bt .edgeLabel{background-color:transparent;text-align:center;}#mermaid-r2bt .edgeLabel p{background-color:transparent;}#mermaid-r2bt .edgeLabel rect{opacity:0.5;background-color:transparent;fill:transparent;}#mermaid-r2bt .labelBkg{background-color:rgba(0, 0, 0, 0.5);}#mermaid-r2bt .cluster rect{fill:#CC785C;stroke:hsl(15, 12.3364485981%, 48.0392156863%);stroke-width:1px;}#mermaid-r2bt .cluster text{fill:#3387a3;}#mermaid-r2bt .cluster span{color:#3387a3;}#mermaid-r2bt div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:inherit;font-size:12px;background:#CC785C;border:1px solid hsl(15, 12.3364485981%, 48.0392156863%);border-radius:2px;pointer-events:none;z-index:100;}#mermaid-r2bt .flowchartTitleText{text-anchor:middle;font-size:18px;fill:#E5E5E5;}#mermaid-r2bt rect.text{fill:none;stroke-width:0;}#mermaid-r2bt .icon-shape,#mermaid-r2bt .image-shape{background-color:transparent;text-align:center;}#mermaid-r2bt .icon-shape p,#mermaid-r2bt .image-shape p{background-color:transparent;padding:2px;}#mermaid-r2bt .icon-shape .label rect,#mermaid-r2bt .image-shape .label rect{opacity:0.5;background-color:transparent;fill:transparent;}#mermaid-r2bt .label-icon{display:inline-block;height:1em;overflow:visible;vertical-align:-0.125em;}#mermaid-r2bt .node .label-icon path{fill:currentColor;stroke:revert;stroke-width:revert;}#mermaid-r2bt .node .neo-node{stroke:#A1A1A1;}#mermaid-r2bt [data-look="neo"].node rect,#mermaid-r2bt [data-look="neo"].cluster rect,#mermaid-r2bt [data-look="neo"].node polygon{stroke:url(#mermaid-r2bt-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#mermaid-r2bt [data-look="neo"].node path{stroke:url(#mermaid-r2bt-gradient);stroke-width:1px;}#mermaid-r2bt [data-look="neo"].node .outer-path{filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#mermaid-r2bt [data-look="neo"].node .neo-line path{stroke:#A1A1A1;filter:none;}#mermaid-r2bt [data-look="neo"].node circle{stroke:url(#mermaid-r2bt-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#mermaid-r2bt [data-look="neo"].node circle .state-start{fill:#000000;}#mermaid-r2bt [data-look="neo"].icon-shape .icon{fill:url(#mermaid-r2bt-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#mermaid-r2bt [data-look="neo"].icon-shape .icon-neo path{stroke:url(#mermaid-r2bt-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#mermaid-r2bt :root{--mermaid-font-family:inherit;}External ServicesData LayerCore EngineTask LayerAPI LayerClient LayerOffline mode: direct callConnected mode: HTTP +API keyHTTP + JWTDispatch scan jobRead/WriteDeliver jobExecute scanRun checksFindingsScored resultsJSON/HTML/PDFStore resultsHTTP requestsCVE queriesCVE queriesDNS queriesCLI ToolTyper + RichWeb DashboardReact + TailwindFastAPI BackendREST API + JWT AuthCelery WorkerRedisMessage BrokerOrchestratorCheck Modulesx10Scoring EngineReporterPostgreSQLDatabaseReport FilesPDF + HTMLNVD APIOSV APIDNS ResolversTarget Website

5. Component Specifications
5.1 Core Engine
Location: engine/
Language: Python 3.11+
Purpose: The heart of WebGuard. Performs all passive security checks, scores results, and generates reports. Completely independent of any interface.
Responsibilities:

Accept a ScanTarget object as input
Coordinate execution of all applicable check modules
Collect and aggregate findings from all checks
Pass findings to the scoring engine
Pass scored results to the reporter
Return a complete ScanResult object

Key design constraint:
The engine has no knowledge of HTTP request handling, user authentication, database operations, or interface rendering. It receives a target and returns a result. Nothing else.
Internal components:
engine/
├── models.py          Data classes — ScanTarget, Finding,
│                      ScanResult, Severity, OWASPCategory
│
├── orchestrator.py    Coordinates check execution
│                      Manages concurrency with asyncio
│                      Handles per-check timeouts
│                      Aggregates findings
│
├── scoring.py         Applies severity deductions
│                      Calculates dimension scores
│                      Calculates weighted overall score
│                      Assigns grades
│
├── reporter.py        Renders JSON output
│                      Renders HTML from Jinja2 template
│                      Generates PDF from HTML via WeasyPrint
│
└── checks/
    ├── base_check.py          Abstract base class
    ├── transport_security.py  TLS, HSTS, HTTP redirect
    ├── security_headers.py    CSP, X-Frame-Options, etc.
    ├── cookie_security.py     HttpOnly, Secure, SameSite
    ├── information_disclosure.py  Version, stack traces
    ├── component_safety.py    JS libraries, CVE matching
    ├── cors_config.py         CORS headers
    ├── dns_security.py        SPF, DMARC, DNSSEC, CAA
    ├── sensitive_files.py     robots.txt, .git, etc.
    ├── ssl_certificate.py     Certificate details
    └── content_protocol.py   Mixed content, HTTP/2
Concurrency model:
All checks run concurrently using asyncio.gather(). A shared httpx.AsyncClient is instantiated once per scan and passed to all checks — connection pooling is handled at the orchestrator level.
python# Simplified orchestrator concurrency model
async def run_scan(target: ScanTarget) -> ScanResult:
    async with httpx.AsyncClient(timeout=30.0) as client:
        checks = get_checks_for_profile(target.profile)
        tasks = [check.run(target) for check in checks]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        findings = flatten_and_filter(results)
        score = scoring_engine.calculate(findings)
        report = reporter.generate(target, findings, score)
        return ScanResult(target, findings, score, report)

5.2 CLI Tool
Location: cli/
Language: Python 3.11+
Framework: Typer + Rich
Purpose: Command-line interface for developers and CI/CD pipeline integration.
Responsibilities:

Parse command-line arguments
Validate input
In offline mode — call engine directly and render results
In connected mode — call REST API and render results
Format and display terminal output using Rich
Write output files (JSON, HTML, PDF) on request

Operating modes:
Offline Mode (default)
──────────────────────
User runs: webguard scan https://example.com

CLI validates URL
CLI instantiates engine orchestrator directly
Engine runs locally
Results rendered in terminal
Optional file output saved locally
No API. No database. No authentication required.

Connected Mode (--api-key flag)
────────────────────────────────
User runs: webguard scan https://example.com --api-key KEY

CLI validates URL
CLI sends POST request to API with API key header
API queues scan job
CLI polls GET /api/v1/scans/{id}/status every 3 seconds
On completion CLI fetches and renders results
Scan stored in database and accessible on web dashboard
Command structure:
webguard
├── scan <URL> [OPTIONS]
│   ├── --profile [quick|standard|deep]
│   ├── --format  [terminal|json|html|pdf]
│   ├── --output  PATH
│   ├── --timeout INTEGER
│   ├── --api-key STRING
│   ├── --api-url STRING
│   ├── --verbose
│   └── --no-color
│
├── list-checks
├── version
└── config
    ├── set <key> <value>
    └── get <key>

5.3 REST API Backend
Location: api/
Language: Python 3.11+
Framework: FastAPI
Purpose: HTTP interface enabling the web dashboard and connected CLI mode. Handles authentication, scan job dispatch, result retrieval, and report serving.
Responsibilities:

Authenticate users via JWT
Validate and accept scan requests
Dispatch scan jobs to Celery via Redis
Store and retrieve scan results from PostgreSQL
Serve report files
Enforce rate limiting and input validation
Provide dashboard statistics

Internal structure:
api/
├── main.py            FastAPI application factory
│                      Middleware configuration
│                      Router registration
│
├── config.py          Environment variable loading
│                      Settings management
│
├── database.py        SQLAlchemy session management
│                      Connection pool configuration
│
├── models/            SQLAlchemy ORM models
│   ├── user.py
│   ├── scan.py
│   └── report.py
│
├── routes/            FastAPI route handlers
│   ├── auth.py        Registration, login, refresh, logout
│   ├── scans.py       Submit, list, get, delete scans
│   ├── reports.py     JSON, HTML, PDF retrieval
│   └── dashboard.py   Stats and recent scans
│
├── services/          Business logic layer
│   ├── scan_service.py    Scan creation and retrieval
│   └── report_service.py  Report generation and caching
│
└── workers/
    └── scan_worker.py     Celery task definitions
Request lifecycle:
1. Request arrives at FastAPI
2. Middleware: rate limit check
3. Middleware: JWT validation (authenticated routes)
4. Route handler: input validation via Pydantic
5. Service layer: business logic
6. Database: read or write via SQLAlchemy ORM
7. Response: Pydantic serialization
8. Client receives response

5.4 Task Queue
Components: Celery + Redis
Purpose: Decouple scan execution from API request handling. Scans run in background workers without blocking the API.
Why this matters:
A scan takes up to 5 minutes. An HTTP request cannot stay open for 5 minutes. The task queue pattern solves this:

API accepts the request immediately and returns a scan ID
Scan runs asynchronously in a worker process
Client polls for status updates

Redis role:
Redis acts as the message broker — it holds the queue of pending scan jobs. When the API dispatches a scan job, Redis stores it. When a Celery worker is free, it picks up the next job from Redis.
Worker lifecycle:
1. API creates scan record in DB with status: pending
2. API dispatches Celery task with scan_id to Redis queue
3. API returns { scan_id, status: "pending" } to client
4. Celery worker picks up task from Redis
5. Worker updates scan status: running
6. Worker calls engine orchestrator with scan parameters
7. Engine runs all checks concurrently
8. Engine returns ScanResult
9. Worker stores findings in PostgreSQL
10. Worker generates and stores report files
11. Worker updates scan status: completed
12. Client polling detects completion
13. Client fetches full results
Error handling:
If engine raises exception:
→ Worker catches exception
→ Updates scan status: failed
→ Stores error message in scan record
→ Client polling detects failure
→ Client shows error with retry option

If worker crashes mid-scan:
→ Celery retry mechanism re-queues the task
→ Maximum 3 retries with exponential backoff
→ After 3 failures: status set to failed

5.5 Web Dashboard
Location: web/
Language: JavaScript (React 18)
Framework: React + Tailwind CSS
Purpose: Browser-based interface for scan submission, results viewing, and report management.
Responsibilities:

Authenticate users and manage JWT session
Provide scan submission interface
Display real-time scan progress
Render scan results with finding cards
Serve downloadable reports
Display scan history and dashboard statistics

Internal structure:
web/src/
├── components/
│   ├── common/
│   │   ├── Navbar.jsx
│   │   ├── Sidebar.jsx
│   │   ├── LoadingSpinner.jsx
│   │   ├── ErrorBoundary.jsx
│   │   └── ProtectedRoute.jsx
│   │
│   ├── dashboard/
│   │   ├── ScoreCard.jsx
│   │   ├── ScoreHistoryChart.jsx
│   │   ├── FindingsSummary.jsx
│   │   └── RecentScans.jsx
│   │
│   ├── scan/
│   │   ├── ScanForm.jsx
│   │   ├── ScanProgress.jsx
│   │   ├── FindingCard.jsx
│   │   ├── DimensionScore.jsx
│   │   └── SeverityFilter.jsx
│   │
│   └── report/
│       ├── ReportHeader.jsx
│       ├── ExecutiveSummary.jsx
│       └── DownloadButtons.jsx
│
├── pages/
│   ├── Landing.jsx
│   ├── Dashboard.jsx
│   ├── NewScan.jsx
│   ├── ScanProgress.jsx
│   ├── ScanResults.jsx
│   ├── History.jsx
│   ├── ApiKeys.jsx
│   └── Settings.jsx
│
├── services/
│   └── api.js             Axios instance + all API calls
│
├── hooks/
│   ├── useAuth.js
│   ├── useScan.js
│   └── useDashboard.js
│
└── utils/
    ├── formatters.js      Score, date, severity formatting
    └── validators.js      URL and form validation
State management:

React Query for server state (API data, caching, refetching)
React Context for authentication state
Local component state for UI interactions

Authentication flow:
User logs in
→ POST /api/v1/auth/login
→ Receives access_token (15 min) and refresh_token (7 days)
→ Access token stored in memory (not localStorage)
→ Refresh token stored in httpOnly cookie
→ Axios interceptor attaches access token to every request
→ On 401 response: interceptor requests new access token
→ On refresh failure: redirect to login

5.6 Database
Engine: PostgreSQL
ORM: SQLAlchemy with Alembic migrations
Purpose: Persistent storage for users, scans, findings, dimension scores, reports, and API keys.
Full schema defined in docs/technical/database-schema.md.

6. Data Flow Diagrams
6.1 Level 1 — System Data Flow
Shows how data flows through the complete system for a web dashboard scan:
#mermaid-r2c8{font-family:inherit;font-size:16px;fill:#E5E5E5;}@keyframes edge-animation-frame{from{stroke-dashoffset:0;}}@keyframes dash{to{stroke-dashoffset:0;}}#mermaid-r2c8 .edge-animation-slow{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 50s linear infinite;stroke-linecap:round;}#mermaid-r2c8 .edge-animation-fast{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 20s linear infinite;stroke-linecap:round;}#mermaid-r2c8 .error-icon{fill:#CC785C;}#mermaid-r2c8 .error-text{fill:#3387a3;stroke:#3387a3;}#mermaid-r2c8 .edge-thickness-normal{stroke-width:1px;}#mermaid-r2c8 .edge-thickness-thick{stroke-width:3.5px;}#mermaid-r2c8 .edge-pattern-solid{stroke-dasharray:0;}#mermaid-r2c8 .edge-thickness-invisible{stroke-width:0;fill:none;}#mermaid-r2c8 .edge-pattern-dashed{stroke-dasharray:3;}#mermaid-r2c8 .edge-pattern-dotted{stroke-dasharray:2;}#mermaid-r2c8 .marker{fill:#A1A1A1;stroke:#A1A1A1;}#mermaid-r2c8 .marker.cross{stroke:#A1A1A1;}#mermaid-r2c8 svg{font-family:inherit;font-size:16px;}#mermaid-r2c8 p{margin:0;}#mermaid-r2c8 .label{font-family:inherit;color:#E5E5E5;}#mermaid-r2c8 .cluster-label text{fill:#3387a3;}#mermaid-r2c8 .cluster-label span{color:#3387a3;}#mermaid-r2c8 .cluster-label span p{background-color:transparent;}#mermaid-r2c8 .label text,#mermaid-r2c8 span{fill:#E5E5E5;color:#E5E5E5;}#mermaid-r2c8 .node rect,#mermaid-r2c8 .node circle,#mermaid-r2c8 .node ellipse,#mermaid-r2c8 .node polygon,#mermaid-r2c8 .node path{fill:transparent;stroke:#A1A1A1;stroke-width:1px;}#mermaid-r2c8 .rough-node .label text,#mermaid-r2c8 .node .label text,#mermaid-r2c8 .image-shape .label,#mermaid-r2c8 .icon-shape .label{text-anchor:middle;}#mermaid-r2c8 .node .katex path{fill:#000;stroke:#000;stroke-width:1px;}#mermaid-r2c8 .rough-node .label,#mermaid-r2c8 .node .label,#mermaid-r2c8 .image-shape .label,#mermaid-r2c8 .icon-shape .label{text-align:center;}#mermaid-r2c8 .node.clickable{cursor:pointer;}#mermaid-r2c8 .root .anchor path{fill:#A1A1A1!important;stroke-width:0;stroke:#A1A1A1;}#mermaid-r2c8 .arrowheadPath{fill:#0b0b0b;}#mermaid-r2c8 .edgePath .path{stroke:#A1A1A1;stroke-width:1px;}#mermaid-r2c8 .flowchart-link{stroke:#A1A1A1;fill:none;}#mermaid-r2c8 .edgeLabel{background-color:transparent;text-align:center;}#mermaid-r2c8 .edgeLabel p{background-color:transparent;}#mermaid-r2c8 .edgeLabel rect{opacity:0.5;background-color:transparent;fill:transparent;}#mermaid-r2c8 .labelBkg{background-color:rgba(0, 0, 0, 0.5);}#mermaid-r2c8 .cluster rect{fill:#CC785C;stroke:hsl(15, 12.3364485981%, 48.0392156863%);stroke-width:1px;}#mermaid-r2c8 .cluster text{fill:#3387a3;}#mermaid-r2c8 .cluster span{color:#3387a3;}#mermaid-r2c8 div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:inherit;font-size:12px;background:#CC785C;border:1px solid hsl(15, 12.3364485981%, 48.0392156863%);border-radius:2px;pointer-events:none;z-index:100;}#mermaid-r2c8 .flowchartTitleText{text-anchor:middle;font-size:18px;fill:#E5E5E5;}#mermaid-r2c8 rect.text{fill:none;stroke-width:0;}#mermaid-r2c8 .icon-shape,#mermaid-r2c8 .image-shape{background-color:transparent;text-align:center;}#mermaid-r2c8 .icon-shape p,#mermaid-r2c8 .image-shape p{background-color:transparent;padding:2px;}#mermaid-r2c8 .icon-shape .label rect,#mermaid-r2c8 .image-shape .label rect{opacity:0.5;background-color:transparent;fill:transparent;}#mermaid-r2c8 .label-icon{display:inline-block;height:1em;overflow:visible;vertical-align:-0.125em;}#mermaid-r2c8 .node .label-icon path{fill:currentColor;stroke:revert;stroke-width:revert;}#mermaid-r2c8 .node .neo-node{stroke:#A1A1A1;}#mermaid-r2c8 [data-look="neo"].node rect,#mermaid-r2c8 [data-look="neo"].cluster rect,#mermaid-r2c8 [data-look="neo"].node polygon{stroke:url(#mermaid-r2c8-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#mermaid-r2c8 [data-look="neo"].node path{stroke:url(#mermaid-r2c8-gradient);stroke-width:1px;}#mermaid-r2c8 [data-look="neo"].node .outer-path{filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#mermaid-r2c8 [data-look="neo"].node .neo-line path{stroke:#A1A1A1;filter:none;}#mermaid-r2c8 [data-look="neo"].node circle{stroke:url(#mermaid-r2c8-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#mermaid-r2c8 [data-look="neo"].node circle .state-start{fill:#000000;}#mermaid-r2c8 [data-look="neo"].icon-shape .icon{fill:url(#mermaid-r2c8-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#mermaid-r2c8 [data-look="neo"].icon-shape .icon-neo path{stroke:url(#mermaid-r2c8-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#mermaid-r2c8 :root{--mermaid-font-family:inherit;}URL + profilePOST /api/v1/scansValidate + storeDispatch jobscan_id + pendingPoll statusJobExecuteHTTP requestsDNS queriesCVE lookupHeaders + responsesDNS recordsCVE dataScanResultStore findingsSave filesUpdate status: completedFetch resultsRead resultsFindings + scoreRender resultsUserWeb DashboardFastAPIPostgreSQLRedisCelery WorkerCore EngineTarget WebsiteDNS ResolversNVD / OSV APIReport Files

6.2 Level 2 — Core Engine Data Flow
Shows how data flows inside the engine during a scan:
#mermaid-r2c9{font-family:inherit;font-size:16px;fill:#E5E5E5;}@keyframes edge-animation-frame{from{stroke-dashoffset:0;}}@keyframes dash{to{stroke-dashoffset:0;}}#mermaid-r2c9 .edge-animation-slow{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 50s linear infinite;stroke-linecap:round;}#mermaid-r2c9 .edge-animation-fast{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 20s linear infinite;stroke-linecap:round;}#mermaid-r2c9 .error-icon{fill:#CC785C;}#mermaid-r2c9 .error-text{fill:#3387a3;stroke:#3387a3;}#mermaid-r2c9 .edge-thickness-normal{stroke-width:1px;}#mermaid-r2c9 .edge-thickness-thick{stroke-width:3.5px;}#mermaid-r2c9 .edge-pattern-solid{stroke-dasharray:0;}#mermaid-r2c9 .edge-thickness-invisible{stroke-width:0;fill:none;}#mermaid-r2c9 .edge-pattern-dashed{stroke-dasharray:3;}#mermaid-r2c9 .edge-pattern-dotted{stroke-dasharray:2;}#mermaid-r2c9 .marker{fill:#A1A1A1;stroke:#A1A1A1;}#mermaid-r2c9 .marker.cross{stroke:#A1A1A1;}#mermaid-r2c9 svg{font-family:inherit;font-size:16px;}#mermaid-r2c9 p{margin:0;}#mermaid-r2c9 .label{font-family:inherit;color:#E5E5E5;}#mermaid-r2c9 .cluster-label text{fill:#3387a3;}#mermaid-r2c9 .cluster-label span{color:#3387a3;}#mermaid-r2c9 .cluster-label span p{background-color:transparent;}#mermaid-r2c9 .label text,#mermaid-r2c9 span{fill:#E5E5E5;color:#E5E5E5;}#mermaid-r2c9 .node rect,#mermaid-r2c9 .node circle,#mermaid-r2c9 .node ellipse,#mermaid-r2c9 .node polygon,#mermaid-r2c9 .node path{fill:transparent;stroke:#A1A1A1;stroke-width:1px;}#mermaid-r2c9 .rough-node .label text,#mermaid-r2c9 .node .label text,#mermaid-r2c9 .image-shape .label,#mermaid-r2c9 .icon-shape .label{text-anchor:middle;}#mermaid-r2c9 .node .katex path{fill:#000;stroke:#000;stroke-width:1px;}#mermaid-r2c9 .rough-node .label,#mermaid-r2c9 .node .label,#mermaid-r2c9 .image-shape .label,#mermaid-r2c9 .icon-shape .label{text-align:center;}#mermaid-r2c9 .node.clickable{cursor:pointer;}#mermaid-r2c9 .root .anchor path{fill:#A1A1A1!important;stroke-width:0;stroke:#A1A1A1;}#mermaid-r2c9 .arrowheadPath{fill:#0b0b0b;}#mermaid-r2c9 .edgePath .path{stroke:#A1A1A1;stroke-width:1px;}#mermaid-r2c9 .flowchart-link{stroke:#A1A1A1;fill:none;}#mermaid-r2c9 .edgeLabel{background-color:transparent;text-align:center;}#mermaid-r2c9 .edgeLabel p{background-color:transparent;}#mermaid-r2c9 .edgeLabel rect{opacity:0.5;background-color:transparent;fill:transparent;}#mermaid-r2c9 .labelBkg{background-color:rgba(0, 0, 0, 0.5);}#mermaid-r2c9 .cluster rect{fill:#CC785C;stroke:hsl(15, 12.3364485981%, 48.0392156863%);stroke-width:1px;}#mermaid-r2c9 .cluster text{fill:#3387a3;}#mermaid-r2c9 .cluster span{color:#3387a3;}#mermaid-r2c9 div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:inherit;font-size:12px;background:#CC785C;border:1px solid hsl(15, 12.3364485981%, 48.0392156863%);border-radius:2px;pointer-events:none;z-index:100;}#mermaid-r2c9 .flowchartTitleText{text-anchor:middle;font-size:18px;fill:#E5E5E5;}#mermaid-r2c9 rect.text{fill:none;stroke-width:0;}#mermaid-r2c9 .icon-shape,#mermaid-r2c9 .image-shape{background-color:transparent;text-align:center;}#mermaid-r2c9 .icon-shape p,#mermaid-r2c9 .image-shape p{background-color:transparent;padding:2px;}#mermaid-r2c9 .icon-shape .label rect,#mermaid-r2c9 .image-shape .label rect{opacity:0.5;background-color:transparent;fill:transparent;}#mermaid-r2c9 .label-icon{display:inline-block;height:1em;overflow:visible;vertical-align:-0.125em;}#mermaid-r2c9 .node .label-icon path{fill:currentColor;stroke:revert;stroke-width:revert;}#mermaid-r2c9 .node .neo-node{stroke:#A1A1A1;}#mermaid-r2c9 [data-look="neo"].node rect,#mermaid-r2c9 [data-look="neo"].cluster rect,#mermaid-r2c9 [data-look="neo"].node polygon{stroke:url(#mermaid-r2c9-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#mermaid-r2c9 [data-look="neo"].node path{stroke:url(#mermaid-r2c9-gradient);stroke-width:1px;}#mermaid-r2c9 [data-look="neo"].node .outer-path{filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#mermaid-r2c9 [data-look="neo"].node .neo-line path{stroke:#A1A1A1;filter:none;}#mermaid-r2c9 [data-look="neo"].node circle{stroke:url(#mermaid-r2c9-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#mermaid-r2c9 [data-look="neo"].node circle .state-start{fill:#000000;}#mermaid-r2c9 [data-look="neo"].icon-shape .icon{fill:url(#mermaid-r2c9-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#mermaid-r2c9 [data-look="neo"].icon-shape .icon-neo path{stroke:url(#mermaid-r2c9-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#mermaid-r2c9 :root{--mermaid-font-family:inherit;}ScanTargetURL + profile + timestampOrchestratorhttpx AsyncClientshared connection pooltransport_security.pysecurity_headers.pycookie_security.pyinformation_disclosure.pycomponent_safety.pycors_config.pydns_security.pysensitive_files.pyssl_certificate.pycontent_protocol.pyfindings: List of FindingScoring EngineDimensionScore x6Overall Score + GradeReporterJSON OutputHTML ReportPDF Report

6.3 Level 2 — CLI Offline Mode Data Flow
#mermaid-r2ca{font-family:inherit;font-size:16px;fill:#E5E5E5;}@keyframes edge-animation-frame{from{stroke-dashoffset:0;}}@keyframes dash{to{stroke-dashoffset:0;}}#mermaid-r2ca .edge-animation-slow{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 50s linear infinite;stroke-linecap:round;}#mermaid-r2ca .edge-animation-fast{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 20s linear infinite;stroke-linecap:round;}#mermaid-r2ca .error-icon{fill:#CC785C;}#mermaid-r2ca .error-text{fill:#3387a3;stroke:#3387a3;}#mermaid-r2ca .edge-thickness-normal{stroke-width:1px;}#mermaid-r2ca .edge-thickness-thick{stroke-width:3.5px;}#mermaid-r2ca .edge-pattern-solid{stroke-dasharray:0;}#mermaid-r2ca .edge-thickness-invisible{stroke-width:0;fill:none;}#mermaid-r2ca .edge-pattern-dashed{stroke-dasharray:3;}#mermaid-r2ca .edge-pattern-dotted{stroke-dasharray:2;}#mermaid-r2ca .marker{fill:#A1A1A1;stroke:#A1A1A1;}#mermaid-r2ca .marker.cross{stroke:#A1A1A1;}#mermaid-r2ca svg{font-family:inherit;font-size:16px;}#mermaid-r2ca p{margin:0;}#mermaid-r2ca .label{font-family:inherit;color:#E5E5E5;}#mermaid-r2ca .cluster-label text{fill:#3387a3;}#mermaid-r2ca .cluster-label span{color:#3387a3;}#mermaid-r2ca .cluster-label span p{background-color:transparent;}#mermaid-r2ca .label text,#mermaid-r2ca span{fill:#E5E5E5;color:#E5E5E5;}#mermaid-r2ca .node rect,#mermaid-r2ca .node circle,#mermaid-r2ca .node ellipse,#mermaid-r2ca .node polygon,#mermaid-r2ca .node path{fill:transparent;stroke:#A1A1A1;stroke-width:1px;}#mermaid-r2ca .rough-node .label text,#mermaid-r2ca .node .label text,#mermaid-r2ca .image-shape .label,#mermaid-r2ca .icon-shape .label{text-anchor:middle;}#mermaid-r2ca .node .katex path{fill:#000;stroke:#000;stroke-width:1px;}#mermaid-r2ca .rough-node .label,#mermaid-r2ca .node .label,#mermaid-r2ca .image-shape .label,#mermaid-r2ca .icon-shape .label{text-align:center;}#mermaid-r2ca .node.clickable{cursor:pointer;}#mermaid-r2ca .root .anchor path{fill:#A1A1A1!important;stroke-width:0;stroke:#A1A1A1;}#mermaid-r2ca .arrowheadPath{fill:#0b0b0b;}#mermaid-r2ca .edgePath .path{stroke:#A1A1A1;stroke-width:1px;}#mermaid-r2ca .flowchart-link{stroke:#A1A1A1;fill:none;}#mermaid-r2ca .edgeLabel{background-color:transparent;text-align:center;}#mermaid-r2ca .edgeLabel p{background-color:transparent;}#mermaid-r2ca .edgeLabel rect{opacity:0.5;background-color:transparent;fill:transparent;}#mermaid-r2ca .labelBkg{background-color:rgba(0, 0, 0, 0.5);}#mermaid-r2ca .cluster rect{fill:#CC785C;stroke:hsl(15, 12.3364485981%, 48.0392156863%);stroke-width:1px;}#mermaid-r2ca .cluster text{fill:#3387a3;}#mermaid-r2ca .cluster span{color:#3387a3;}#mermaid-r2ca div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:inherit;font-size:12px;background:#CC785C;border:1px solid hsl(15, 12.3364485981%, 48.0392156863%);border-radius:2px;pointer-events:none;z-index:100;}#mermaid-r2ca .flowchartTitleText{text-anchor:middle;font-size:18px;fill:#E5E5E5;}#mermaid-r2ca rect.text{fill:none;stroke-width:0;}#mermaid-r2ca .icon-shape,#mermaid-r2ca .image-shape{background-color:transparent;text-align:center;}#mermaid-r2ca .icon-shape p,#mermaid-r2ca .image-shape p{background-color:transparent;padding:2px;}#mermaid-r2ca .icon-shape .label rect,#mermaid-r2ca .image-shape .label rect{opacity:0.5;background-color:transparent;fill:transparent;}#mermaid-r2ca .label-icon{display:inline-block;height:1em;overflow:visible;vertical-align:-0.125em;}#mermaid-r2ca .node .label-icon path{fill:currentColor;stroke:revert;stroke-width:revert;}#mermaid-r2ca .node .neo-node{stroke:#A1A1A1;}#mermaid-r2ca [data-look="neo"].node rect,#mermaid-r2ca [data-look="neo"].cluster rect,#mermaid-r2ca [data-look="neo"].node polygon{stroke:url(#mermaid-r2ca-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#mermaid-r2ca [data-look="neo"].node path{stroke:url(#mermaid-r2ca-gradient);stroke-width:1px;}#mermaid-r2ca [data-look="neo"].node .outer-path{filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#mermaid-r2ca [data-look="neo"].node .neo-line path{stroke:#A1A1A1;filter:none;}#mermaid-r2ca [data-look="neo"].node circle{stroke:url(#mermaid-r2ca-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#mermaid-r2ca [data-look="neo"].node circle .state-start{fill:#000000;}#mermaid-r2ca [data-look="neo"].icon-shape .icon{fill:url(#mermaid-r2ca-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#mermaid-r2ca [data-look="neo"].icon-shape .icon-neo path{stroke:url(#mermaid-r2ca-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#mermaid-r2ca :root{--mermaid-font-family:inherit;}webguard scan URL--profile standardvalidateinvalid URLvalid URLpassive HTTP requestsresponsesScanResult JSONformat and renderdisplayDeveloperTerminalCLI ToolURL ValidatorCore EngineTarget WebsiteTerminal Outputor FileError Message

6.4 Level 2 — CLI Connected Mode Data Flow
graph TD
    USER[Developer\nTerminal]
    CLI[CLI Tool]
    API[FastAPI Backend]
    REDIS[(Redis)]
    WORKER[Celery Worker]
    ENGINE[Core Engine]
    DB[(PostgreSQL)]
    TARGET[Target Website]

    USER -->|webguard scan URL --api-key KEY| CLI
    CLI -->|POST /api/v1/scans with API key| API
    API -->|store scan record| DB
    API -->|dispatch job| REDIS
    API -->|scan_id + pending| CLI
    CLI -->|poll GET /scans/id/status every 3s| API
    REDIS -->|deliver job| WORKER
    WORKER -->|execute| ENGINE
    ENGINE -->|passive HTTP requests| TARGET
    TARGET -->|responses| ENGINE
    ENGINE -->|ScanResult| WORKER
    WORKER -->|store findings| DB
    WORKER -->|update status: completed| DB
    CLI -->|detects completion| API
    CLI -->|GET /scans/id| API
    API -->|full results| CLI
    CLI -->|render results| USER

6.5 Level 2 — Authentication Data Flow
graph TD
    USER[User Browser]
    WEB[Web Dashboard]
    API[FastAPI]
    DB[(PostgreSQL)]

    USER -->|email + password| WEB
    WEB -->|POST /auth/login| API
    API -->|lookup user| DB
    DB -->|user record| API
    API -->|verify bcrypt hash| API
    API -->|access_token 15min\nrefresh_token 7days| WEB
    WEB -->|store access_token in memory| WEB
    WEB -->|store refresh_token in httpOnly cookie| WEB

    WEB -->|request with Authorization: Bearer token| API
    API -->|verify JWT signature| API
    API -->|extract user_id| API
    API -->|serve response| WEB

    WEB -->|access_token expires| WEB
    WEB -->|POST /auth/refresh with cookie| API
    API -->|verify refresh token| DB
    API -->|new access_token| WEB

6.6 Level 2 — Report Generation Data Flow
graph TD
    RESULT[ScanResult Object]
    REPORTER[Reporter Engine]
    JINJA[Jinja2 Template Engine]
    TEMPLATE[report.html.jinja2]
    HTML_STR[HTML String]
    WEASY[WeasyPrint]
    JSON_OUT[report.json]
    HTML_OUT[report.html]
    PDF_OUT[report.pdf]
    DB[(PostgreSQL)]
    FILES[File Storage]

    RESULT -->|serialize| JSON_OUT
    RESULT --> REPORTER
    TEMPLATE --> JINJA
    REPORTER -->|pass findings + score| JINJA
    JINJA -->|rendered| HTML_STR
    HTML_STR --> HTML_OUT
    HTML_STR --> WEASY
    WEASY -->|convert| PDF_OUT
    JSON_OUT --> FILES
    HTML_OUT --> FILES
    PDF_OUT --> FILES
    FILES -->|store file paths| DB

7. Sequence Diagrams
7.1 Web Dashboard Scan — Full Sequence
sequenceDiagram
    participant U as User
    participant W as Web Dashboard
    participant A as FastAPI
    participant R as Redis
    participant C as Celery Worker
    participant E as Engine
    participant D as PostgreSQL

    U->>W: Submit URL + profile
    W->>A: POST /api/v1/scans
    A->>A: Validate URL
    A->>D: INSERT scan record (status: pending)
    A->>R: dispatch_scan.delay(scan_id)
    A->>W: { scan_id, status: pending }
    W->>U: Show progress page

    loop Poll every 3 seconds
        W->>A: GET /api/v1/scans/{id}/status
        A->>D: SELECT status WHERE id=scan_id
        A->>W: { status: running, progress: 40% }
        W->>U: Update progress indicator
    end

    R->>C: Deliver scan job
    C->>D: UPDATE status: running
    C->>E: orchestrator.run(target)
    E->>E: Run all checks concurrently
    E->>C: ScanResult
    C->>D: INSERT findings
    C->>D: INSERT dimension_scores
    C->>D: UPDATE scan status: completed
    C->>D: INSERT report file paths

    W->>A: GET /api/v1/scans/{id}/status
    A->>W: { status: completed }
    W->>A: GET /api/v1/scans/{id}
    A->>D: SELECT scan + findings + scores
    A->>W: Full scan result
    W->>U: Render results page

7.2 CLI Offline Mode — Full Sequence
sequenceDiagram
    participant D as Developer
    participant C as CLI
    participant V as Validator
    participant E as Engine
    participant T as Target Website

    D->>C: webguard scan https://example.com
    C->>V: validate_url(url)
    V->>C: valid
    C->>E: orchestrator.run(ScanTarget)
    C->>D: Show progress bar

    par Run checks concurrently
        E->>T: GET / (headers analysis)
        E->>T: TLS handshake
        E->>T: GET /robots.txt
    end

    T->>E: HTTP responses
    E->>E: Calculate scores
    E->>E: Generate reports
    E->>C: ScanResult
    C->>D: Render terminal output
    C->>D: Save report file (if --format specified)

8. Technology Stack
8.1 Complete Stack
LayerTechnologyVersionPurposeEngine languagePython3.11+Core scanning logicAsync HTTP clienthttpx0.27+All outbound HTTP requestsCLI frameworkTyper0.12+Argument parsingCLI outputRich13+Terminal formattingAPI frameworkFastAPI0.111+REST APIAPI serverUvicorn0.29+ASGI serverTask queueCelery5.4+Background workersMessage brokerRedis7+Task queue backendDatabasePostgreSQL16+Persistent storageORMSQLAlchemy2.0+Database abstractionMigrationsAlembic1.13+Schema versioningPassword hashingbcrypt4+Credential securityJWTpython-jose3.3+Token handlingTemplate engineJinja23.1+Report HTML templatesPDF generationWeasyPrint62+HTML to PDFFrontendReact18+Web dashboardCSS frameworkTailwind CSS3+StylingHTTP client (web)Axios1.6+API calls from browserChartsRecharts2.12+Dashboard chartsServer stateReact Query5+API data managementContainerizationDocker26+Environment isolationOrchestrationDocker Compose2.27+Local developmentCI/CDGitHub Actions—Automated pipelineError trackingSentry—Production monitoring

8.2 Dependency Decisions
Why httpx over requests?
httpx is async-native. Since all check modules are async, using requests would require running it in a thread executor — adding complexity and overhead. httpx provides the same API as requests with full async support.
Why FastAPI over Flask or Django?
FastAPI is async-native, matching the engine's async design. It auto-generates OpenAPI documentation from type hints — saving significant documentation effort. Pydantic validation is built in. Performance is significantly higher than Flask for IO-bound workloads.
Why Celery + Redis over FastAPI BackgroundTasks?
FastAPI BackgroundTasks run in the same process as the API. A scan that takes 5 minutes would tie up an API worker. Celery workers are separate processes that scale independently. Redis as the broker is lightweight and fast.
Why PostgreSQL over SQLite?
SQLite is single-writer. Concurrent scan workers writing results simultaneously would cause lock contention. PostgreSQL handles concurrent writes correctly and scales to production volumes.
Why WeasyPrint over ReportLab?
WeasyPrint generates PDF from HTML — meaning the HTML report template is the single source of truth for both the HTML and PDF outputs. ReportLab requires building the PDF programmatically — a separate code path to maintain. One template, two outputs.

9. Security Architecture
9.1 Input Validation and URL Safety
All URLs submitted to WebGuard — whether via CLI, API, or web dashboard — pass through the same validation function before any scan begins:
python# engine/validators.py

PRIVATE_IP_RANGES = [
    ipaddress.ip_network('10.0.0.0/8'),
    ipaddress.ip_network('172.16.0.0/12'),
    ipaddress.ip_network('192.168.0.0/16'),
    ipaddress.ip_network('127.0.0.0/8'),
    ipaddress.ip_network('169.254.0.0/16'),
    ipaddress.ip_network('::1/128'),
]

def validate_scan_target(url: str) -> ValidationResult:
    # Must be valid URL format
    # Must be http:// or https:// only
    # Must not be localhost or 127.x.x.x
    # Must not resolve to private IP range
    # Must not exceed 2048 characters
    # Must resolve in DNS before scan begins
Why DNS pre-resolution?
Resolving the domain before scanning catches cases where an attacker submits a domain that initially resolves to a public IP but is configured to switch to a private IP mid-request (DNS rebinding attack).

9.2 Authentication Architecture
Password storage:    bcrypt with minimum 12 rounds
Access token:        JWT, 15 minute expiry, signed with HS256
Refresh token:       Opaque random token, 7 day expiry,
                     stored as hash in database
Token storage:       Access token in memory only (not localStorage)
                     Refresh token in httpOnly cookie
API keys:            SHA-256 hash stored, plaintext shown once
Rate limiting:       5 failed logins → 15 minute lockout per IP

9.3 Data Isolation
Every database query that returns user data includes a user_id filter:
python# Users can only access their own scans
scan = db.query(Scan).filter(
    Scan.id == scan_id,
    Scan.user_id == current_user.id  # Always enforced
).first()
This is enforced at the service layer — never relying on route-level checks alone.

9.4 WebGuard as a Scan Origin
The engine makes outbound HTTP requests to target websites. From the target's perspective WebGuard is a client. The engine must:

Identify itself honestly in the User-Agent header:
WebGuard-Scanner/1.0 (+https://webguard.io/scanner)
Respect robots.txt for file existence checks
Never make more than a defined maximum number of requests per scan
Implement per-request timeouts — never hang indefinitely


10. Error Handling Architecture
Every layer has a defined error handling strategy:
Engine checks
Each check module catches all exceptions internally. A check that fails returns an empty findings list and logs the error — never propagates an exception to the orchestrator.
Orchestrator
Uses asyncio.gather(*tasks, return_exceptions=True) — exceptions from individual checks are captured as results, not raised. The scan continues with available results.
Celery workers
Catch all exceptions from the engine. Update scan status to failed with an error message. Never leave a scan in running state indefinitely.
FastAPI routes
Global exception handler catches unhandled exceptions and returns 500 with a safe generic message. Never exposes stack traces in API responses.
Web dashboard
React Error Boundary components wrap all major sections. A failing component renders an error card — never crashes the entire page.

11. Configuration Management
All configuration is environment-variable driven. No secrets in code. No secrets in version control.
# .env.example — committed to repository
# .env — never committed, in .gitignore

DATABASE_URL=postgresql://user:password@localhost:5432/webguard
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
NVD_API_KEY=your-nvd-api-key
SENTRY_DSN=your-sentry-dsn
ENVIRONMENT=development
MAX_CONCURRENT_SCANS=10
SCAN_TIMEOUT_SECONDS=300

12. Deployment Architecture
12.1 Local Development
docker-compose up

Services started:
├── webguard-api        FastAPI on port 8000
├── webguard-worker     Celery worker
├── webguard-web        React dev server on port 3000
├── postgres            PostgreSQL on port 5432
└── redis               Redis on port 6379
12.2 Production
Cloud Infrastructure:

├── Web Server (Nginx)
│   ├── Serves React build (static files)
│   ├── Reverse proxy to FastAPI
│   └── SSL termination
│
├── Application Server
│   ├── FastAPI (Uvicorn, multiple workers)
│   └── Celery workers (multiple processes)
│
├── Managed PostgreSQL
│   └── Automated backups enabled
│
├── Managed Redis
│   └── Persistence enabled for job durability
│
└── File Storage
    └── Report files (PDF, HTML, JSON)

13. Document Relationships
This document (architecture.md)
    ├── Implemented by → engine/, cli/, api/, web/
    ├── Data structures → database-schema.md
    ├── API contracts  → api-reference.md
    ├── Security detail → security-design.md
    └── Deployment detail → devops-plan.md

This document is version controlled. All changes must be committed with a descriptive message and reviewed before merging. Any architectural decision that deviates from this document must first be recorded as an ADR in docs/technical/decisions/.
Last updated: May 2026
