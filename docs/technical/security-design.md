WebGuard — Security Design Document
Document: Security Design
Version: 1.0
Status: Draft
Created: May 2026
Author: James Gichia
Repository: docs/technical/security-design.md

1. Purpose
This document defines the security architecture of WebGuard itself. It covers the threat model, authentication design, data protection strategy, application security controls, and infrastructure hardening measures.
A security scanning tool that has vulnerabilities is not just a technical failure — it is a fundamental credibility failure. Every security decision in this document exists to ensure WebGuard earns the trust it asks its users to place in it.

2. Security Principles
Defense in depth
No single security control is relied upon exclusively. Multiple independent layers protect every critical asset. If one layer fails the others remain.
Least privilege
Every component, process, and user account has only the permissions it needs to perform its function — nothing more.
Fail securely
When a security control encounters an error it denies access by default. The system never fails open.
Security by design
Security controls are built into the architecture from the beginning — not added as an afterthought. Every feature is designed with its security implications considered first.
Minimal attack surface
Every unnecessary feature, endpoint, port, and permission is removed. The fewer entry points that exist the fewer can be exploited.
Assume breach
The system is designed with the assumption that some component will eventually be compromised. Compartmentalization, monitoring, and incident response capabilities limit the blast radius.

3. Threat Model
3.1 Assets Being Protected
AssetClassificationWhy It MattersUser passwordsCriticalCompromise enables account takeoverUser email addressesSensitivePII — privacy and phishing riskAPI keysCriticalCompromise enables unauthorized scanningJWT secretsCriticalCompromise enables authentication bypassScan resultsSensitiveMay reveal security posture of user's assetsReport filesSensitiveContain detailed vulnerability informationDatabase connection stringsCriticalFull database access if exposedInfrastructure credentialsCriticalFull system access if exposed

3.2 Threat Actors
External attacker — opportunistic
Automated scanners probing for common vulnerabilities. Looking for default credentials, exposed admin panels, SQL injection, and known CVEs. Low sophistication but high volume.
External attacker — targeted
A motivated attacker specifically targeting WebGuard. May attempt to steal user data, access scan results of high-value targets, or abuse the scanning engine for reconnaissance.
Malicious user
A registered user attempting to abuse the platform — scanning targets they do not own, attempting to access other users' results, or probing the API for vulnerabilities.
Compromised dependency
A third-party library or package in the dependency tree is compromised — a supply chain attack. Malicious code executes within the application context.
Insider threat
Minimal for Version 1 as a solo developer project. Documented for completeness and future team growth.

3.3 Threat Scenarios and Mitigations
T-001: Credential stuffing against login endpoint
Attacker uses a list of breached credentials to attempt login against WebGuard accounts.
Mitigations:

Rate limiting: 10 requests per minute per IP on login endpoint
Account lockout: 15 minutes after 5 consecutive failures per IP
bcrypt with 12 rounds: makes each hash comparison slow — reduces brute force viability
Breach detection: future enhancement — HaveIBeenPwned API integration


T-002: JWT token theft and replay
Attacker intercepts or steals a valid JWT access token and uses it to impersonate the user.
Mitigations:

Short access token expiry: 15 minutes limits the window of use after theft
HTTPS only: prevents token interception in transit
Token stored in memory only on client: not localStorage — reduces XSS theft risk
Refresh token rotation: stolen refresh tokens invalidated on next legitimate use


T-003: API key exposure
A developer accidentally commits an API key to a public repository or exposes it in logs.
Mitigations:

Key prefix visible in UI: user can identify which key was exposed
Immediate revocation: DELETE /api/v1/keys/{id} takes effect immediately
Keys hashed in database: exposed database does not reveal key values
User limited to 5 keys: limits blast radius of a compromised account


T-004: SSRF via scan engine
An attacker submits a URL pointing to an internal network resource — attempting to use WebGuard's scanner to probe internal services, cloud metadata endpoints, or other restricted resources.
Mitigations:

URL validation: all submitted URLs validated before scanning
DNS pre-resolution: domain resolved before scanning — result checked against private IP ranges
Private IP blocklist: 10.x.x.x, 192.168.x.x, 172.16.x.x, 127.x.x.x, 169.254.x.x all rejected
Protocol restriction: only http:// and https:// accepted — no file://, ftp://, or other schemes
DNS rebinding protection: IP re-checked during scan if DNS TTL is very short


T-005: Unauthorized access to another user's scan results
A user attempts to access scan results belonging to another user by guessing or enumerating scan IDs.
Mitigations:

UUID primary keys: not guessable or enumerable
User ID enforcement: every database query filters by authenticated user_id
Service layer ownership check: ownership verified before any data is returned
No information leakage: 403 Forbidden returned whether scan exists or not if user does not own it


T-006: SQL injection via API inputs
Attacker submits malicious SQL syntax in API request fields to manipulate database queries.
Mitigations:

ORM only: all database queries use SQLAlchemy ORM — no raw SQL string concatenation
Parameterized queries: ORM generates parameterized queries — input never interpreted as SQL
Input validation: all inputs validated by Pydantic before reaching service layer


T-007: Mass assignment — overprivileged update
Attacker submits extra fields in an update request attempting to modify protected fields such as is_active, is_verified, or user_id.
Mitigations:

Pydantic schemas: explicit schema for every request — only declared fields accepted
No pass-through updates: service layer explicitly maps allowed fields — never passes raw request data to ORM


T-008: Denial of service via scan submission
Attacker submits large numbers of scans to exhaust server resources.
Mitigations:

Rate limiting: 5 scans per hour per user
Celery worker pool: bounded number of concurrent workers — excess jobs queued not executed immediately
Scan timeout: maximum scan duration enforced — hung scans terminated
Authentication required: unauthenticated users cannot submit scans


T-009: Report file path traversal
Attacker manipulates report file path parameters to access files outside the reports directory.
Mitigations:

File paths stored in database: client never supplies file paths — they are looked up by scan ID
Path sanitization: all file paths sanitized before filesystem operations
Reports directory isolated: report files stored in a dedicated directory — application has no access to system files


T-010: Dependency compromise
A package in the dependency tree is compromised and executes malicious code within the application.
Mitigations:

Pinned dependencies: all dependency versions pinned exactly in requirements.txt
Automated scanning: GitHub Actions runs safety and pip-audit on every commit
Regular updates: dependency versions reviewed and updated monthly
Minimal dependencies: only packages that are genuinely needed are included


4. Authentication Design
4.1 Password Security
Hashing algorithm: bcrypt
Cost factor: 12 rounds minimum
bcrypt is chosen over SHA-256 or MD5 because it is intentionally slow. At 12 rounds each hash comparison takes approximately 300 milliseconds. This makes brute force attacks impractical — an attacker can attempt only about 3 guesses per second compared to billions per second with fast algorithms.
python# api/services/auth_service.py

import bcrypt

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )
Password policy:

Minimum 8 characters
Must contain at least one number
Maximum 128 characters — prevents bcrypt DoS via extremely long passwords
Common password list check — future enhancement


4.2 JWT Design
Algorithm: HS256 (HMAC-SHA256)
Secret: Minimum 256-bit random secret — generated at deployment, stored in environment variable
Access token expiry: 15 minutes
Refresh token expiry: 7 days
Access token payload:
json{
  "sub": "550e8400-e29b-41d4-a716-446655440000",
  "type": "access",
  "iat": 1716571200,
  "exp": 1716572100
}
Token validation process:
python# api/services/auth_service.py

from jose import JWTError, jwt

def verify_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        if payload.get("type") != "access":
            raise InvalidTokenError("Wrong token type")
        user_id = payload.get("sub")
        if not user_id:
            raise InvalidTokenError("Missing subject")
        return {"user_id": user_id}
    except JWTError:
        raise InvalidTokenError("Token validation failed")
Why HS256 over RS256?
HS256 uses a single shared secret — simpler to implement and manage for a solo developer project. RS256 uses public/private key pairs — better for distributed systems where multiple services validate tokens independently. HS256 is appropriate for Version 1 where the API is the only token validator.

4.3 Refresh Token Design
Refresh tokens are opaque random strings — not JWTs. This is a deliberate design choice.
Why opaque refresh tokens instead of JWT?
JWT refresh tokens cannot be invalidated before expiry — the token is valid until its expiry date regardless of whether the user logs out or changes their password. Opaque tokens stored in the database can be instantly invalidated by deleting the database record.
Generation:
pythonimport secrets

def generate_refresh_token() -> str:
    return secrets.token_urlsafe(64)
Storage:
python# Stored as SHA-256 hash in database
import hashlib

def hash_refresh_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()
Rotation:
On every refresh token use:

Validate submitted token against stored hash
If valid — delete old token record
Generate new refresh token
Store new token hash
Return new access token and new refresh token

If an already-used refresh token is submitted — this indicates possible token theft. All refresh tokens for the user are immediately invalidated, forcing full re-authentication.

4.4 API Key Design
Format:
wg_live_{32 random URL-safe characters}

Example:
wg_live_a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
Prefix meaning:

wg_ — WebGuard identifier
live_ — production environment (future: test_ for test keys)
a1b2c3d4 — first 8 characters stored as key_prefix in database

Generation:
pythonimport secrets

def generate_api_key() -> tuple[str, str, str]:
    random_part = secrets.token_urlsafe(32)
    full_key = f"wg_live_{random_part}"
    prefix = full_key[:12]
    key_hash = hashlib.sha256(full_key.encode()).hexdigest()
    return full_key, prefix, key_hash
Authentication flow:
pythonasync def authenticate_api_key(key: str, db: Session) -> User:
    key_hash = hashlib.sha256(key.encode()).hexdigest()
    api_key = db.query(APIKey).filter(
        APIKey.key_hash == key_hash,
        APIKey.is_active == True
    ).first()
    if not api_key:
        raise InvalidTokenError("Invalid API key")
    if not api_key.user.is_active:
        raise InvalidTokenError("Account inactive")
    # Update last_used_at
    api_key.last_used_at = datetime.utcnow()
    db.commit()
    return api_key.user

4.5 Authentication Middleware
The FastAPI dependency that protects all authenticated routes:
python# api/dependencies/auth.py

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    token = credentials.credentials

    # Try JWT first
    try:
        payload = verify_access_token(token)
        user = db.query(User).filter(
            User.id == payload["user_id"],
            User.is_active == True
        ).first()
        if user:
            return user
    except InvalidTokenError:
        pass

    # Try API key
    try:
        user = await authenticate_api_key(token, db)
        return user
    except InvalidTokenError:
        pass

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={"code": "AUTH_REQUIRED", "message": "Authentication required"}
    )

4.6 Account Security Controls
Login attempt tracking:
python# Tracked in Redis for performance
# Key: login_attempts:{ip_address}
# Value: attempt count
# TTL: 15 minutes

async def check_login_attempts(ip: str) -> None:
    key = f"login_attempts:{ip}"
    attempts = await redis.get(key)
    if attempts and int(attempts) >= 5:
        raise AccountLockedException(
            "Too many failed attempts. Try again in 15 minutes."
        )

async def record_failed_login(ip: str) -> None:
    key = f"login_attempts:{ip}"
    await redis.incr(key)
    await redis.expire(key, 900)  # 15 minutes

async def clear_login_attempts(ip: str) -> None:
    await redis.delete(f"login_attempts:{ip}")
Session invalidation on password change:
When a user changes their password all existing refresh tokens are deleted from the database. Active access tokens remain valid for up to 15 minutes — acceptable given the short expiry window.
pythonasync def change_password(user_id: UUID, new_password: str, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    user.password_hash = hash_password(new_password)
    # Invalidate all refresh tokens
    db.query(RefreshToken).filter(
        RefreshToken.user_id == user_id
    ).delete()
    db.commit()

5. Data Protection
5.1 Data at Rest
Database encryption:
PostgreSQL database encrypted at rest using the cloud provider's managed encryption (AES-256). This is handled at the infrastructure level — the database files on disk are encrypted.
Sensitive field handling:
FieldStorageNotesPasswordsbcrypt hashNever plaintextAPI keysSHA-256 hashPlaintext shown once onlyRefresh tokensSHA-256 hashNever plaintextJWT secretEnvironment variableNever in database or codeEmail addressesPlaintextRequired for loginScan resultsPlaintextNot classified as sensitive PIIReport filesPlaintext on diskAccess controlled by application
What is never stored:

Target website content beyond header values
Target website credentials or form data
Payment information (no billing in Version 1)
Government identification numbers


5.2 Data in Transit
TLS enforcement:
All communication uses TLS 1.2 or higher. HTTP requests are redirected to HTTPS. HSTS header enforced with a one-year max-age.
Internal service communication:
In production, internal communication between API, workers, PostgreSQL, and Redis uses private network interfaces — not exposed to the public internet. TLS used for database connections.
Certificate management:
Let's Encrypt certificates with automatic renewal via Certbot. Certificate expiry monitored and alerted 30 days before expiry.

5.3 Data Retention
Scan data:
Retained until the user explicitly deletes it or deletes their account. No automatic expiry in Version 1.
Report files:
Retained alongside scan records. Deleted when the scan is deleted.
Authentication logs:
Login attempt records in Redis expire automatically after 15 minutes. Failed login events logged to application logs retained for 30 days.
Application logs:
Retained for 30 days in production. No user passwords or API key values ever written to logs.
Account deletion:
On account deletion all user data is permanently deleted within 24 hours. No soft delete. No backup retention of deleted user data beyond the standard database backup window (7 days for database-level backups).

5.4 Sensitive Data Handling in Code
Logging rules — never log:
python# NEVER log these values
# passwords (plain or hashed)
# API keys (full value)
# JWT tokens
# Refresh tokens
# Database connection strings
# Any value from request.headers["Authorization"]

# SAFE to log
# user_id (UUID)
# scan_id (UUID)
# API key prefix (first 12 characters)
# Request method and path
# Response status code
# Error messages (without sensitive context)
Environment variable validation on startup:
python# api/config.py

class Settings(BaseSettings):
    SECRET_KEY: str
    DATABASE_URL: str
    REDIS_URL: str

    @validator('SECRET_KEY')
    def secret_key_must_be_strong(cls, v):
        if len(v) < 32:
            raise ValueError('SECRET_KEY must be at least 32 characters')
        return v

    class Config:
        env_file = ".env"

# Application fails to start if required secrets are missing
settings = Settings()

6. Application Security
6.1 Input Validation Strategy
All input is validated at three layers:
Layer 1 — Network layer (Nginx)
Request size limits enforced at reverse proxy level:

Maximum request body: 1MB
Maximum URL length: 8KB
Maximum header size: 8KB

Layer 2 — API layer (Pydantic)
Every request body validated against an explicit Pydantic schema before reaching any business logic. Unknown fields are ignored — never passed through.
Layer 3 — Service layer
Business rule validation beyond schema — URL safety checks, ownership verification, rate limit enforcement.
Validation principle:
Validate everything. Trust nothing from the network. Reject early — invalid input should fail at the outermost layer before reaching business logic.

6.2 URL Validation — SSRF Prevention
This is the most security-critical validation in WebGuard given that the core function of the application is making outbound HTTP requests.
python# engine/validators.py

import ipaddress
import socket
from urllib.parse import urlparse

BLOCKED_SCHEMES = {'file', 'ftp', 'gopher', 'dict', 'ldap', 'ldaps'}

PRIVATE_NETWORKS = [
    ipaddress.ip_network('10.0.0.0/8'),
    ipaddress.ip_network('172.16.0.0/12'),
    ipaddress.ip_network('192.168.0.0/16'),
    ipaddress.ip_network('127.0.0.0/8'),
    ipaddress.ip_network('169.254.0.0/16'),  # Link-local
    ipaddress.ip_network('100.64.0.0/10'),   # Shared address space
    ipaddress.ip_network('::1/128'),          # IPv6 loopback
    ipaddress.ip_network('fc00::/7'),         # IPv6 unique local
    ipaddress.ip_network('fe80::/10'),        # IPv6 link-local
]

BLOCKED_HOSTS = {
    'localhost',
    'metadata.google.internal',
    '169.254.169.254',  # AWS metadata
    'metadata.azure.com',
}

def validate_scan_target(url: str) -> ValidationResult:
    # Parse URL
    parsed = urlparse(url)

    # Scheme check
    if parsed.scheme not in {'http', 'https'}:
        raise InvalidURLError(f"Scheme '{parsed.scheme}' not allowed")

    # Host extraction
    host = parsed.hostname
    if not host:
        raise InvalidURLError("No host in URL")

    # Blocked host check
    if host.lower() in BLOCKED_HOSTS:
        raise PrivateTargetError(f"Host '{host}' is not allowed")

    # DNS resolution
    try:
        addr_infos = socket.getaddrinfo(host, None)
    except socket.gaierror:
        raise InvalidURLError(f"Could not resolve host '{host}'")

    # IP range check on all resolved addresses
    for addr_info in addr_infos:
        ip_str = addr_info[4][0]
        try:
            ip = ipaddress.ip_address(ip_str)
            for network in PRIVATE_NETWORKS:
                if ip in network:
                    raise PrivateTargetError(
                        f"Host resolves to private IP range"
                    )
        except ValueError:
            continue

    return ValidationResult(valid=True, resolved_ip=addr_infos[0][4][0])

6.3 Output Encoding
All data returned in API responses is serialized through Pydantic models — which handle JSON encoding automatically. No raw string interpolation in response construction.
HTML reports are generated through Jinja2 templates with autoescaping enabled:
python# engine/reporter.py

from jinja2 import Environment, FileSystemLoader

env = Environment(
    loader=FileSystemLoader('reports/templates'),
    autoescape=True  # Prevents XSS in generated HTML reports
)

6.4 Security Headers on API Responses
The FastAPI application adds security headers to all responses via middleware:
python# api/middleware/security_headers.py

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains"
        )
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Cache-Control"] = "no-store"
        # Remove server identification
        response.headers.pop("server", None)
        return response

6.5 CORS Configuration
CORS is configured to allow only the WebGuard web dashboard origin:
python# api/main.py

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],  # e.g. https://app.webguard.io
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)
In development:
FRONTEND_URL=http://localhost:3000
In production:
FRONTEND_URL=https://app.webguard.io
Wildcard origins are never used — not even in development.

6.6 Rate Limiting Implementation
Rate limiting implemented using Redis with sliding window counters:
python# api/middleware/rate_limiter.py

import redis.asyncio as redis
import time

class RateLimiter:
    def __init__(self, redis_client, limit: int, window: int):
        self.redis = redis_client
        self.limit = limit      # Max requests
        self.window = window    # Window in seconds

    async def is_allowed(self, key: str) -> tuple[bool, int]:
        now = time.time()
        window_start = now - self.window

        pipe = self.redis.pipeline()
        pipe.zremrangebyscore(key, 0, window_start)
        pipe.zadd(key, {str(now): now})
        pipe.zcard(key)
        pipe.expire(key, self.window)
        results = await pipe.execute()

        request_count = results[2]
        remaining = max(0, self.limit - request_count)

        if request_count > self.limit:
            return False, remaining
        return True, remaining

6.7 Scanner Self-Security
The scanner makes outbound HTTP requests. It must not be weaponized:
User-Agent identification:
pythonSCANNER_USER_AGENT = (
    "WebGuard-Scanner/1.0 "
    "(+https://webguard.io/scanner; "
    "security@webguard.io)"
)
Request limits per scan:
pythonMAX_REQUESTS_PER_SCAN = 50
The orchestrator tracks request count across all checks. If the limit is reached scanning stops and results so far are returned.
Timeout enforcement:
python# Per-request timeout
httpx.AsyncClient(timeout=httpx.Timeout(
    connect=10.0,
    read=30.0,
    write=10.0,
    pool=5.0
))
No credential handling:
The scanner never sends authentication credentials to target sites. It makes only unauthenticated passive requests.

7. Infrastructure Security
7.1 Container Security
Non-root execution:
dockerfile# All Dockerfiles end with non-root user
RUN addgroup --system webguard && \
    adduser --system --ingroup webguard webguard
USER webguard
Minimal base images:
dockerfile# Use slim variants — fewer packages means smaller attack surface
FROM python:3.11-slim
No secrets in images:
dockerfile# NEVER in Dockerfile:
ENV DATABASE_URL=postgresql://...  # WRONG

# Always via environment variables at runtime
# docker-compose.yml references .env file
# Production uses secrets manager
Read-only filesystem where possible:
yaml# docker-compose.yml
services:
  api:
    read_only: true
    tmpfs:
      - /tmp

7.2 Secrets Management
Development:
Environment variables loaded from .env file. .env is in .gitignore and never committed.
Production:
Secrets stored in cloud provider secrets manager (AWS Secrets Manager or similar). Injected as environment variables at container startup. Never in configuration files, never in container images, never in logs.
Secret rotation:
JWT secret rotation requires restarting the API service. All active sessions are invalidated on rotation — users must re-login. Acceptable given the security benefit.
Required secrets:
SECRET_KEY              JWT signing secret (min 32 chars random)
DATABASE_URL            PostgreSQL connection string with credentials
REDIS_URL               Redis connection string
NVD_API_KEY             NVD API key for CVE lookups
SENTRY_DSN              Error tracking endpoint

7.3 Database Security
Connection:
Database accessible only from application servers — not exposed to public internet.
Credentials:
Dedicated database user with minimum required permissions:
sql-- Create application user
CREATE USER webguard_app WITH PASSWORD 'strong-random-password';

-- Grant only what is needed
GRANT CONNECT ON DATABASE webguard TO webguard_app;
GRANT USAGE ON SCHEMA public TO webguard_app;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO webguard_app;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO webguard_app;

-- Application user cannot DROP tables or ALTER schema
-- DDL operations only via migration user
Backups:
Automated daily backups with 7-day retention. Backup files encrypted at rest. Restore procedure documented and tested monthly.

7.4 Network Security
Production network topology:
Internet
    │
    ▼
Cloudflare (DDoS protection, WAF, CDN)
    │
    ▼
Nginx (reverse proxy, SSL termination)
    │
    ├──► FastAPI (internal network only)
    │
    └──► React static files (served directly by Nginx)

Internal network (not internet-accessible):
├── FastAPI ◄──► PostgreSQL
├── FastAPI ◄──► Redis
└── Celery Workers ◄──► Redis
Firewall rules:
Public internet → Port 80 (HTTP)  → Nginx (redirects to HTTPS)
Public internet → Port 443 (HTTPS) → Nginx
All other ports → BLOCKED from public internet

Internal network:
API → PostgreSQL port 5432 → ALLOWED
API → Redis port 6379      → ALLOWED
Workers → Redis port 6379  → ALLOWED

7.5 Monitoring and Incident Response
Error tracking:
Sentry configured for both API and frontend. All unhandled exceptions captured with context. PII scrubbed from error reports — user passwords and API keys never appear in Sentry events.
Security event logging:
The following events are logged with timestamp, user ID, and IP address:
SECURITY_EVENT_LOGIN_SUCCESS
SECURITY_EVENT_LOGIN_FAILURE
SECURITY_EVENT_LOGIN_LOCKOUT
SECURITY_EVENT_PASSWORD_CHANGED
SECURITY_EVENT_API_KEY_CREATED
SECURITY_EVENT_API_KEY_DELETED
SECURITY_EVENT_ACCOUNT_DELETED
SECURITY_EVENT_INVALID_SCAN_TARGET
SECURITY_EVENT_RATE_LIMIT_EXCEEDED
Anomaly indicators to monitor:

Unusual spike in scan submissions from one IP
Multiple failed logins across different accounts from same IP
API key used from unusual geographic location
Large number of 403 responses from one user

Incident response procedure:
1. Detection
   Alert fires in monitoring system

2. Assessment
   Determine scope and severity

3. Containment
   Suspend affected account or block IP as appropriate
   Rotate compromised secrets if applicable

4. Investigation
   Review security event logs
   Determine root cause

5. Remediation
   Fix the vulnerability
   Deploy patch

6. Communication
   Notify affected users if their data was accessed
   Follow responsible disclosure if a third party reported

8. Security Testing Requirements
Before Version 1.0 launch WebGuard must pass its own security checks:
Self-scan:
Run a WebGuard standard scan against the production WebGuard web application. Score must be 9.0 or above. Any Critical or High findings must be remediated before launch.
Dependency audit:
bashpip-audit --requirement requirements.txt
safety check --full-report
Zero high or critical vulnerabilities in dependencies at launch.
OWASP ZAP scan:
Run an OWASP ZAP baseline scan against the staging API and web dashboard. All High and Critical findings remediated before launch.
Manual review checklist:

 All endpoints require authentication where specified
 No endpoint returns another user's data
 Rate limits enforced and tested
 All inputs validated — fuzzing attempted
 Error responses contain no stack traces
 No secrets in repository — truffleHog scan passed
 Docker containers run as non-root
 HTTPS enforced — HTTP redirects verified
 Security headers present on all responses
 CORS restricted to own domain


9. Vulnerability Disclosure
WebGuard maintains a responsible disclosure policy documented at docs/legal/responsible-disclosure.md.
Security researchers who discover vulnerabilities in WebGuard are encouraged to report them via:

Email: security@webguard.io
security.txt: https://webguard.io/.well-known/security.txt

Commitment to researchers:

Acknowledgement within 48 hours
Assessment and triage within 7 days
Fix timeline communicated within 14 days
Credit given in changelog unless anonymity requested


This document is version controlled. Security design changes require review and approval before implementation. Any deviation from this document must be recorded as an ADR.
Last updated: May 2026
