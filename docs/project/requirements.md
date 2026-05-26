# WebGuard — Product Requirements Document (PRD)

| | |
|---|---|
| **Document** | Product Requirements Document |
| **Version** | 1.0 |
| **Status** | Draft |
| **Created** | May 2026 |
| **Author** | James Gichia |
| **Repository** | `docs/project/requirements.md` |

---

## 1. Purpose
This document defines the complete functional and non-functional requirements for WebGuard Version 1.0. It is the authoritative reference for what the product must do, how well it must do it, and what criteria determine that each requirement has been successfully met.
Every feature built, every module written, and every design decision made during development must trace back to a requirement in this document. If a requirement is not here, it is not in Version 1.0.

## 2. Document Scope
This PRD covers WebGuard Version 1.0 exclusively. Requirements for Version 2.0 and beyond are noted where relevant but are explicitly out of scope for this document.

## 3. Stakeholder Reference

| Persona | Role | Primary Requirements |
|---|---|---|
| Daniel Ochieng | Developer | CLI tool, pipeline integration, fast scans, JSON output |
| Sarah Wanjiku | SMB Owner | Web dashboard, plain English reports, PDF export, scoring |
| Amara Diallo | Security Consultant | Accurate findings, professional PDF, multi-target, CLI |

## 4. Functional Requirements
Functional requirements define what the system must do. Each requirement has a unique ID, a description, a priority, and acceptance criteria.
Priority levels:

- **P1 — Critical:** Product cannot launch without this
- **P2 — High:** Significantly impacts core value proposition
- **P3 — Medium:** Adds meaningful value but not blocking
- **P4 — Low:** Nice to have in Version 1.0


### 4.1 Core Engine Requirements

FR-001 — URL Acceptance and Validation
Priority: P1
The system must accept a URL as the primary input for a scan.
Acceptance criteria:

Accepts HTTP and HTTPS URLs
Validates URL format before scan begins
Rejects malformed URLs with a clear error message
Rejects private IP ranges (10.x.x.x, 192.168.x.x, 172.16.x.x–172.31.x.x)
Rejects localhost and loopback addresses (127.0.0.1, ::1)
Rejects non-HTTP/HTTPS protocols (ftp://, file://, etc.)
Normalizes URLs — strips trailing slashes, handles www vs non-www consistently
Maximum URL length of 2,048 characters enforced


FR-002 — Scan Profiles
Priority: P1
The system must support three scan profiles with defined scope and approximate duration.
Acceptance criteria:

Quick profile completes in under 60 seconds on a standard broadband connection
Standard profile completes in under 3 minutes on a standard broadband connection
Deep profile completes in under 6 minutes on a standard broadband connection
Profile selection is available in both CLI and web dashboard
Default profile when none specified is Standard
Each profile's scope is clearly documented in help text and UI

Profile definitions:
Quick Profile
→ Transport security check
→ Security headers check
→ SSL certificate check
→ Approximate duration: 30–60 seconds

Standard Profile
→ All Quick checks
→ Cookie security check
→ Information disclosure check
→ CORS configuration check
→ DNS security check
→ Sensitive file exposure check
→ Content and protocol check
→ Approximate duration: 1–3 minutes

Deep Profile
→ All Standard checks
→ Component safety check (includes CVE API lookup)
→ Approximate duration: 3–6 minutes

FR-003 — Transport Security Check
Priority: P1
The system must passively analyze the TLS and transport security configuration of the target.
Acceptance criteria:

Detects TLS 1.0 support and flags as Critical
Detects TLS 1.1 support and flags as High
Confirms TLS 1.2 and 1.3 availability
Checks HSTS header presence — missing flagged as High
Checks HSTS max-age value — under 6 months flagged as Medium
Checks HSTS includeSubDomains directive
Checks HTTP to HTTPS redirect — missing flagged as High
Verifies redirect does not loop or fail
All findings include evidence of what was observed


FR-004 — SSL Certificate Check
Priority: P1
The system must analyze the SSL certificate of the target.
Acceptance criteria:

Detects expired certificates and flags as Critical
Detects certificates expiring within 30 days and flags as High
Detects certificates expiring within 60 days and flags as Medium
Detects self-signed certificates and flags as High
Verifies certificate chain completeness
Checks certificate covers the scanned domain
Checks for wildcard certificate usage and notes it as Info
All findings include certificate expiry date as evidence


FR-005 — Security Headers Check
Priority: P1
The system must analyze HTTP security headers in the target's response.
Acceptance criteria:

Checks Content-Security-Policy — missing flagged as High
Checks X-Frame-Options — missing flagged as Medium
Checks X-Content-Type-Options — missing flagged as Medium
Checks Referrer-Policy — missing flagged as Low
Checks Permissions-Policy — missing flagged as Low
Checks Cross-Origin-Opener-Policy — missing flagged as Low
Detects overly permissive CSP (unsafe-inline, unsafe-eval) — flagged as Medium
Each finding includes the actual header value observed as evidence
Each finding specifies recommended header value in remediation


FR-006 — Cookie Security Check
Priority: P1
The system must analyze the security attributes of cookies set by the target.
Acceptance criteria:

Detects cookies missing HttpOnly flag — flagged as Medium
Detects cookies missing Secure flag on HTTPS sites — flagged as High
Detects cookies missing SameSite attribute — flagged as Medium
Detects SameSite=None without Secure flag — flagged as High
Reports total number of cookies analyzed
Each finding identifies the specific cookie name affected
Handles multiple cookies correctly — reports each affected cookie


FR-007 — Information Disclosure Check
Priority: P1
The system must detect information the target is unnecessarily exposing in HTTP responses.
Acceptance criteria:

Detects Server header with version information — flagged as Medium
Detects X-Powered-By header with framework/version — flagged as Medium
Detects X-AspNet-Version or similar framework headers — flagged as Medium
Detects verbose error pages returning stack traces — flagged as High
Detects debug mode indicators in headers — flagged as High
Detects internal IP addresses disclosed in headers — flagged as Medium
All findings include the exact disclosed value as evidence


FR-008 — CORS Configuration Check
Priority: P1
The system must analyze Cross-Origin Resource Sharing headers for misconfigurations.
Acceptance criteria:

Detects Access-Control-Allow-Origin: * — flagged as High
Detects Access-Control-Allow-Credentials: true with wildcard origin — flagged as Critical
Detects overly permissive CORS policy — flagged as Medium
Only checks CORS headers that are actually present in the response
Does not flag CORS absence on non-API endpoints as a vulnerability
Includes the exact CORS header values as evidence


FR-009 — DNS Security Check
Priority: P2
The system must analyze DNS security records for the target domain.
Acceptance criteria:

Checks for SPF record presence — missing flagged as Medium
Validates SPF record syntax — invalid flagged as Medium
Checks for DMARC record presence — missing flagged as Medium
Checks DMARC policy strength — none policy flagged as Low
Checks for DKIM selector indicators — absence noted as Info
Checks for CAA records — absence noted as Info
All findings include the actual DNS record value or absence as evidence


FR-010 — Sensitive File Exposure Check
Priority: P2
The system must detect indicators of sensitive file or path exposure using passive methods only.
Acceptance criteria:

Fetches and analyzes robots.txt for sensitive path disclosure — flagged as Info or Low
Checks /.well-known/security.txt presence — absence noted as Info (positive if present)
Performs HEAD request only for .git/HEAD — 200 response flagged as Critical
Performs HEAD request only for .env — 200 response flagged as Critical
Performs HEAD request only for common backup extensions — 200 response flagged as High
No brute-force path enumeration — maximum 10 passive indicator checks
All findings include the URL checked and response code as evidence


FR-011 — Content and Protocol Check
Priority: P2
The system must analyze content security and protocol configuration.
Acceptance criteria:

Detects mixed content (HTTP resources on HTTPS pages) — flagged as Medium
Checks HTTP/2 support — absence noted as Info
Checks www vs non-www consistency — inconsistency flagged as Low
Analyzes redirect chain for security issues — insecure redirects flagged as Medium
Checks Subresource Integrity on externally loaded scripts — missing flagged as Low
All findings include the specific URL or resource affected as evidence


FR-012 — Component Safety Check
Priority: P2
The system must detect outdated or vulnerable JavaScript libraries and components.
Acceptance criteria:

Detects jQuery version from script tags or response content
Detects Bootstrap version from script/link tags
Detects other common library versions via signature patterns
Queries NVD API for known CVEs against detected versions
Queries OSV API as fallback if NVD is unavailable
Flags components with known Critical CVEs as Critical
Flags components with known High CVEs as High
Flags end-of-life components regardless of CVE status as Medium
Gracefully handles API unavailability — completes scan without CVE data
All findings include detected version and CVE IDs as evidence
Deep profile only — not run in Quick or Standard


FR-013 — Multi-Dimensional Scoring
Priority: P1
The system must calculate a multi-dimensional security score for every completed scan.
Acceptance criteria:

Six dimensions scored independently: Transport Security, Header Configuration, Cookie Security, Component Safety, Information Exposure, DNS Security
Each dimension starts at 10.0
Severity deductions applied per finding: Critical -3.0, High -2.0, Medium -1.0, Low -0.5, Info 0.0
Dimension floor is 0.0 — never negative
Each dimension score rounded to one decimal place
Overall score calculated as weighted average of dimension scores
Weights: Transport Security 25%, Header Configuration 20%, Cookie Security 20%, Component Safety 15%, Information Exposure 10%, DNS Security 10%
Overall score rounded to one decimal place
Grade assigned: A (9.0–10.0), B (7.5–8.9), C (6.0–7.4), D (4.0–5.9), F (0.0–3.9)
Label assigned: Excellent, Good, Fair, Poor, Critical


FR-014 — Finding Structure
Priority: P1
Every finding produced by the system must contain a complete and consistent set of fields.
Acceptance criteria:
Every finding must include:

Unique finding ID
Title (short, plain English)
Severity (Critical, High, Medium, Low, Info)
OWASP Top 10 category mapping
Scoring dimension
Description — what was found in plain English
Business impact — what this means for the organization
Evidence — exactly what the scanner observed
Recommendation — specific actionable fix
Effort estimate — Low, Medium, or High
Reference links — minimum one OWASP or authoritative source


FR-015 — Report Generation — JSON
Priority: P1
The system must generate a complete machine-readable JSON report for every scan.
Acceptance criteria:

JSON output contains complete scan metadata (URL, timestamp, profile, duration)
JSON output contains complete score object with overall and all dimensions
JSON output contains complete findings array with all fields per FR-014
JSON is valid and parseable by standard JSON parsers
JSON structure is consistent across all scans
Available immediately on scan completion
CLI outputs JSON to stdout when --format json specified
API returns JSON via GET /api/v1/reports/{scan_id}/json


FR-016 — Report Generation — HTML
Priority: P1
The system must generate a styled human-readable HTML report for every scan.
Acceptance criteria:

HTML report includes cover section with domain, score, grade, date, profile
HTML report includes executive summary section
HTML report includes dimension score breakdown with visual bars
HTML report includes findings grouped by severity
HTML report includes remediation roadmap section
HTML report is self-contained — no external CSS or JS dependencies
HTML report renders correctly in Chrome, Firefox, and Safari
HTML report is mobile responsive
Available on scan completion
CLI saves HTML file when --format html specified
API returns HTML via GET /api/v1/reports/{scan_id}/html


FR-017 — Report Generation — PDF
Priority: P1
The system must generate a professional PDF report for every scan.
Acceptance criteria:

PDF generated from HTML report via WeasyPrint
PDF includes all sections present in HTML report
PDF is formatted for A4 paper
PDF includes page numbers
PDF includes WebGuard branding (logo, footer)
PDF is readable and professional enough for direct client delivery
PDF file size under 5MB for a standard scan
Available on scan completion
CLI saves PDF file when --format pdf specified
API returns PDF via GET /api/v1/reports/{scan_id}/pdf


### 4.2 CLI Tool Requirements

FR-018 — CLI Installation
Priority: P1
The CLI tool must be installable via pip from PyPI.
Acceptance criteria:

Package published to PyPI under the name webguard
Installation via pip install webguard succeeds on Python 3.11+
Installation succeeds on Linux, macOS, and Windows
CLI available as webguard command after installation
Version verifiable via webguard --version


FR-019 — CLI Scan Command
Priority: P1
The CLI must provide a scan command that accepts a URL and options.
Acceptance criteria:
bash# These commands must all work correctly

webguard scan https://example.com
webguard scan https://example.com --profile quick
webguard scan https://example.com --profile standard
webguard scan https://example.com --profile deep
webguard scan https://example.com --format json
webguard scan https://example.com --format html --output ./reports/
webguard scan https://example.com --format pdf --output ./reports/
webguard scan https://example.com --verbose
webguard scan https://example.com --timeout 120
webguard scan https://example.com --no-color
webguard list-checks
webguard --version
webguard --help
webguard scan --help

URL is a required positional argument
All options have sensible defaults
Help text is clear and complete
Error messages are human-readable


FR-020 — CLI Terminal Output
Priority: P1
The CLI must produce clear, well-formatted terminal output during and after a scan.
Acceptance criteria:

Displays tool name and version at scan start
Displays target URL and selected profile
Shows real-time progress — each check updates as it completes
Progress display uses rich formatting with color and progress indicators
Displays overall score prominently on completion
Displays dimension breakdown table on completion
Displays findings summary (count by severity) on completion
Displays top findings (up to five) by severity on completion
Displays scan duration on completion
Color coding: Critical = red, High = orange, Medium = yellow, Low = blue, Info = white
--no-color flag disables all color for CI/CD pipeline output
--verbose flag shows additional detail per check as it runs


FR-021 — CLI Configuration
Priority: P3
The CLI must support persistent configuration for user preferences.
Acceptance criteria:

webguard config set timeout 120 persists timeout preference
webguard config set profile deep persists default profile preference
webguard config get timeout returns current value
Configuration stored in user home directory (~/.webguard/config.json)
Configuration values overridden by explicit command-line flags


### 4.3 API Backend Requirements

FR-022 — User Registration
Priority: P1
The API must support user account creation.
Acceptance criteria:

POST /api/v1/auth/register accepts email and password
Email must be valid format and unique in the system
Password minimum 8 characters, must contain letters and numbers
Password stored as bcrypt hash — never plaintext
Returns JWT access token and refresh token on success
Returns clear error message on validation failure
Returns 409 Conflict if email already registered


FR-023 — User Authentication
Priority: P1
The API must support secure user login.
Acceptance criteria:

POST /api/v1/auth/login accepts email and password
Returns JWT access token (15-minute expiry) and refresh token (7-day expiry)
Returns 401 Unauthorized on invalid credentials
Rate limited to 10 attempts per 15 minutes per IP
Account locked for 15 minutes after 5 failed attempts
POST /api/v1/auth/refresh accepts refresh token and returns new access token
POST /api/v1/auth/logout invalidates refresh token


FR-024 — Scan Submission
Priority: P1
The API must accept scan job submissions from authenticated users.
Acceptance criteria:

POST /api/v1/scans/ accepts URL and profile
Validates URL per FR-001 rules before accepting
Creates scan record in database with status: pending
Dispatches scan job to Celery queue
Returns scan ID and pending status immediately — does not wait for scan to complete
Authenticated requests only — returns 401 if no valid JWT
Rate limited to 10 scan submissions per hour per user


FR-025 — Scan Status Polling
Priority: P1
The API must allow clients to check the status of a running scan.
Acceptance criteria:

GET /api/v1/scans/{id}/status returns current status
Status values: pending, running, completed, failed
Returns progress percentage (0–100) when status is running
Returns 404 if scan ID does not exist
Returns 403 if scan belongs to different user
Polling interval recommended in response headers


FR-026 — Scan Results Retrieval
Priority: P1
The API must return complete scan results for a completed scan.
Acceptance criteria:

GET /api/v1/scans/{id} returns full scan result when completed
Response includes scan metadata, score object, all findings
Response includes dimension scores
Returns 404 if scan not found
Returns 403 if scan belongs to different user
Returns 202 Accepted with status if scan still running


FR-027 — Scan History
Priority: P1
The API must return a paginated list of scans for the authenticated user.
Acceptance criteria:

GET /api/v1/scans/ returns list of user's scans
Results paginated — default 20 per page
Results sorted by creation date descending
Each item includes scan ID, URL, domain, profile, status, score, grade, date
Supports page and per_page query parameters
Supports domain filter query parameter


FR-028 — Report Download
Priority: P1
The API must serve completed scan reports in all three formats.
Acceptance criteria:

GET /api/v1/reports/{scan_id}/json returns JSON report
GET /api/v1/reports/{scan_id}/html returns HTML file
GET /api/v1/reports/{scan_id}/pdf returns PDF file with correct Content-Type
Returns 404 if scan not found
Returns 403 if scan belongs to different user
Returns 425 Too Early if scan not yet completed


FR-029 — Dashboard Statistics
Priority: P2
The API must return summary statistics for the authenticated user's dashboard.
Acceptance criteria:

GET /api/v1/dashboard/stats returns:

Total scans performed
Average overall score across all scans
Total findings by severity (Critical, High, Medium, Low, Info)
Score history for last 10 scans (scan date + overall score)
Most frequently found finding titles (top 5)


Returns 200 with empty/zero values if user has no scans yet


FR-030 — API Key Management
Priority: P2
The API must allow users to generate and manage API keys for pipeline integration.
Acceptance criteria:

POST /api/v1/keys/ generates a new API key
API key shown once on creation — never retrievable again
Stored as hashed value only
GET /api/v1/keys/ returns list of user's keys (label, created date, last used — never the key itself)
DELETE /api/v1/keys/{id} revokes a key
API key accepted as Bearer token in Authorization header
API key grants same permissions as the user's JWT for scan submission and retrieval


### 4.4 Web Dashboard Requirements

FR-031 — Landing Page
Priority: P1
The web application must have a professional landing page that communicates the product's value clearly.
Acceptance criteria:

Hero section with headline, subheadline, and primary CTA
How It Works section — three steps maximum
What We Check section — six dimension cards with plain English descriptions
Sample report preview section
Who It Is For section — three audience cards
Footer with links and legal pages
Page loads in under 3 seconds on standard broadband
Fully mobile responsive


FR-032 — User Registration and Login
Priority: P1
The web application must support user account creation and authentication.
Acceptance criteria:

Registration form accepts name, email, and password
Validates all fields with clear inline error messages
Login form accepts email and password
Password reset via email link
JWT stored securely in memory — not localStorage
Authenticated session persists across page refreshes via refresh token
Redirect to dashboard on successful login
Redirect to login on access to protected route without session


FR-033 — Dashboard Page
Priority: P1
The web application must provide a dashboard overview for authenticated users.
Acceptance criteria:

Displays total scans, average score, and total open findings as stat cards
Displays score history line chart for last 10 scans
Displays findings by severity donut chart
Displays list of recent scans (last 5) with domain, score, grade, date, and view link
Displays prominent New Scan button
All data loaded from API — no hardcoded values
Shows empty state with helpful CTA when user has no scans
Page loads dashboard data within 2 seconds


FR-034 — New Scan Page
Priority: P1
The web application must provide a scan submission interface.
Acceptance criteria:

URL input field with https:// prefix hint
Profile selector with three options and duration estimates
Clear description of what each profile checks
Submit button triggers scan via API
Validates URL format before submission
Shows inline error for invalid URL
Redirects to scan progress page on successful submission
Disabled state on submit button while request is processing


FR-035 — Scan Progress Page
Priority: P1
The web application must show real-time scan progress while a scan is running.
Acceptance criteria:

Displays target URL and selected profile
Shows animated progress indicator
Polls GET /api/v1/scans/{id}/status every 5 seconds
Updates progress percentage display as scan runs
Automatically redirects to scan results page on completion
Shows error state with retry option if scan fails
Does not require manual page refresh at any point


FR-036 — Scan Results Page
Priority: P1
The web application must display complete scan results in a clear, structured format.
Acceptance criteria:

Displays overall score (large, prominent), grade, and label
Displays domain, scan date, and profile used
Displays dimension score breakdown with visual progress bars and grades
Displays findings grouped by severity with filter tabs (All, Critical, High, Medium, Low, Info)
Each finding card displays: severity badge, OWASP category, title, description, business impact, evidence, recommendation, effort
Displays total findings count per severity
Download PDF button triggers PDF report download
Download HTML button triggers HTML report download
Rescan button submits new scan for same URL and profile
Page is fully mobile responsive
Findings are expandable/collapsible for cleaner viewing


FR-037 — Scan History Page
Priority: P1
The web application must display a complete history of the user's scans.
Acceptance criteria:

Displays paginated table of all scans
Columns: Domain, Score, Grade, Profile, Date, Status, Actions
Sortable by date and score
Filterable by domain
Each row has View and Delete actions
Delete prompts confirmation before removing
Pagination controls (previous, next, page numbers)
Empty state when no scans exist


FR-038 — API Keys Page
Priority: P2
The web application must allow users to manage API keys for pipeline integration.
Acceptance criteria:

Displays list of existing API keys (label, created date, last used)
Generate New Key button opens modal with label input
New key displayed once in modal with copy button
Clear warning that key will not be shown again
Revoke button on each key with confirmation
Instructions for using the key in CLI and CI/CD pipelines


FR-039 — Settings Page
Priority: P3
The web application must allow users to manage their account settings.
Acceptance criteria:

Update display name
Update email address (requires password confirmation)
Change password (requires current password)
Delete account (requires password confirmation, shows warning about data loss)
All updates call corresponding API endpoints
Success and error states clearly communicated


## 5. Non-Functional Requirements

Non-functional requirements define how well the system must perform its functions.

### NFR-001 — Performance

| Metric | Target |
|---|---|
| Quick scan completion | Under 60 seconds |
| Standard scan completion | Under 3 minutes |
| Deep scan completion | Under 6 minutes |
| API response time (non-scan endpoints) | Under 500ms at p95 |
| Web dashboard page load | Under 3 seconds on standard broadband |
| PDF report generation | Under 30 seconds |
| Concurrent scans supported | Minimum 10 simultaneous |

### NFR-002 — Accuracy

| Metric | Target |
|---|---|
| False positive rate | Zero confirmed false positives in first 30 days post-launch |
| False negative rate (passive checks) | Under 5% on verified test targets |
| CVE matching accuracy | Verified against NVD ground truth |
| Scoring consistency | Same URL scanned twice within 10 minutes produces identical score |

> [!IMPORTANT]
> Accuracy is the single most important non-functional requirement. One confirmed false positive that affects a production deployment destroys user trust permanently.

### NFR-003 — Security

The tool that finds security vulnerabilities must itself be secure.

| Requirement | Specification |
|---|---|
| Password hashing | bcrypt with minimum 12 rounds |
| JWT expiry | Access token: 15 minutes. Refresh token: 7 days |
| API rate limiting | 10 scan submissions per hour per user. 10 auth attempts per 15 minutes per IP |
| Input validation | All API inputs validated and sanitized before processing |
| SQL injection prevention | ORM only — no raw SQL queries |
| Private IP blocking | Scan engine rejects all private IP ranges and localhost |
| Secret management | All secrets via environment variables — never in codebase |
| HTTPS | Production deployment serves only HTTPS — no HTTP |
| Dependency security | All dependencies pinned to exact versions and scanned for vulnerabilities |
| Container security | Docker containers run as non-root user |

### NFR-004 — Reliability

| Metric | Target |
|---|---|
| Web application uptime | 99.5% monthly |
| Scan failure rate | Under 2% of submitted scans fail due to system error |
| Scan timeout handling | Graceful timeout returns partial results rather than complete failure |
| Database backup | Daily automated backups with 7-day retention |
| Error monitoring | All unhandled exceptions captured in Sentry within 60 seconds |

### NFR-005 — Usability

| Requirement | Specification |
|---|---|
| CLI setup time | Developer operational within 5 minutes of pip install |
| Web app onboarding | User completes first scan within 3 minutes of registration |
| Finding comprehension | Non-technical user can understand every finding without external research |
| Report shareability | PDF report understandable by a non-technical manager without explanation |
| Mobile responsiveness | All web dashboard pages fully functional on 375px viewport width |

### NFR-006 — Maintainability

| Requirement | Specification |
|---|---|
| Test coverage | Minimum 80% on core engine modules |
| Module independence | Each check module operable in isolation without engine dependencies |
| Configuration | Scoring weights and severity deductions configurable in single file |
| Documentation | Every public function and class has a docstring |
| Code style | Black formatting, flake8 linting, mypy type checking enforced in CI |
| Dependency updates | Automated dependency vulnerability alerts via GitHub Dependabot |

### NFR-007 — Scalability

| Requirement | Specification |
|---|---|
| Scan queue | Celery queue handles backlog gracefully — no scan dropped under normal load |
| Worker scaling | Additional Celery workers can be added without code changes |
| Database | PostgreSQL schema supports millions of scans without redesign |
| API | FastAPI async architecture handles concurrent requests without blocking |

## 6. Constraints

These constraints are absolute. They are not requirements to be met — they are boundaries that cannot be crossed.

| Constraint | Description |
|---|---|
| Passive scanning only | The engine must never send payloads intended to exploit vulnerabilities. No SQL injection probes. No XSS payloads. No command injection attempts. |
| No private IP scanning | The engine must never scan internal network addresses, cloud metadata endpoints, or localhost under any circumstances. |
| Legal compliance | All functionality must be achievable without violating computer access laws in Kenya, the EU, the US, or the UK. |
| Version 1.0 scope | No features outside the defined Version 1.0 scope may be built or merged. |
| Open source dependencies | All dependencies must have licenses compatible with MIT. |

## 7. Acceptance Criteria Summary
The following conditions must all be true for WebGuard Version 1.0 to be considered complete and ready for launch:
### Engine

 All 10 passive check modules implemented and tested
 Scoring engine produces correct results verified against manual calculation
 JSON, HTML, and PDF reports generated correctly for all scan profiles
 Engine tested against OWASP Juice Shop with known findings verified
 Engine tested against DVWA with known findings verified
 Zero confirmed false positives in pre-launch testing

### CLI

 Package installable via pip install webguard on Python 3.11+
 All commands in FR-019 work correctly
 Terminal output matches design specification in FR-020
 Tested on Linux, macOS, and Windows

### API

 All endpoints in Section 4.3 implemented and returning correct responses
 JWT authentication working correctly
 Rate limiting enforced and tested
 All endpoints covered by integration tests
 Swagger documentation accessible at /docs

### Web Dashboard

 All pages in Section 4.4 implemented
 All pages mobile responsive at 375px minimum
 First scan completable within 3 minutes of registration
 PDF and HTML report download working
 Tested in Chrome, Firefox, and Safari

### Quality

 80% or above test coverage on engine modules
 Zero critical security vulnerabilities in WebGuard itself (verified by running WebGuard against its own domain)
 All P1 requirements met
 All P2 requirements met
 Sentry error monitoring active and verified

### Documentation

 README complete with installation and usage instructions
 API reference complete
 CLI user guide complete
 Web app user guide complete


## 8. Out of Scope — Version 1.0
The following are explicitly excluded from this document and this version. They are acknowledged as future requirements and will be addressed in subsequent PRDs.

Active scanning of any kind
Scheduled and recurring scans
Compliance mapping (GDPR, PCI-DSS, ISO 27001)
White-label reporting
Team workspaces and multi-user organizations
Billing and subscription management
Slack and email alerting
Browser extension
Mobile application
Verified security badge system
CI/CD pipeline plugins (GitHub Actions, GitLab CI)
Score trend charts and historical analysis (web dashboard)


## 9. Dependencies and Assumptions

### External Dependencies

NVD API (National Vulnerability Database) — required for FR-012. Failure handled gracefully.
OSV API (Open Source Vulnerabilities) — fallback for FR-012. Failure handled gracefully.
WeasyPrint — required for FR-017. Must be installable in deployment environment.

### Assumptions

Target websites are publicly accessible over HTTP or HTTPS
Users have legal authorization to scan any URL they submit
Python 3.11+ is available in all target development environments
PostgreSQL 14+ available in deployment environment
Redis 7+ available for Celery task queue


## 10. Revision History

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | May 2026 | James Gichia | Initial document |

This document is version controlled. All changes require a new version entry in the revision history, a descriptive commit message, and review before merging to the docs branch.
Last updated: May 2026
