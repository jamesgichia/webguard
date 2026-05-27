
WebGuard — API Reference Document
Document: API Reference
Version: 1.0
Status: Draft
Created: May 2026
Author: James Gichia
Repository: docs/technical/api-reference.md

1. Overview
The WebGuard REST API is the backend interface for both the web dashboard and the CLI connected mode. It is built with FastAPI and follows REST conventions throughout.
Base URL (development): http://localhost:8000
Base URL (production): https://api.webguard.io
API version prefix: /api/v1
Full base path: https://api.webguard.io/api/v1
Auto-generated documentation:
FastAPI generates interactive API documentation automatically:

Swagger UI: GET /docs
ReDoc: GET /redoc
OpenAPI JSON: GET /openapi.json


2. Global Conventions
2.1 Request Format
All request bodies are JSON:
Content-Type: application/json
All authenticated requests include a Bearer token:
Authorization: Bearer <access_token>
API key authenticated requests:
Authorization: Bearer <api_key>
The API treats JWT access tokens and API keys identically at the route level — both are validated as Bearer tokens. The authentication middleware determines which type was submitted and validates accordingly.

2.2 Response Format
All responses return JSON. Every response — success or error — follows a consistent envelope structure.
Success response:
json{
  "success": true,
  "data": { },
  "message": "Optional human readable message"
}
Error response:
json{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable description",
    "details": { }
  }
}

2.3 HTTP Status Codes
CodeMeaningWhen Used200OKSuccessful GET, PUT201CreatedSuccessful POST that creates a resource204No ContentSuccessful DELETE400Bad RequestInvalid input, validation failure401UnauthorizedMissing or invalid authentication403ForbiddenAuthenticated but not authorized for resource404Not FoundResource does not exist409ConflictDuplicate resource, business rule violation422Unprocessable EntityRequest body schema validation failure429Too Many RequestsRate limit exceeded500Internal Server ErrorUnexpected server error

2.4 Error Codes
Error CodeHTTP StatusDescriptionVALIDATION_ERROR422Request body failed schema validationINVALID_URL400URL format invalid or target not allowedPRIVATE_TARGET400URL resolves to private IP rangeAUTH_REQUIRED401No authentication providedINVALID_TOKEN401Token malformed, expired, or invalidINVALID_CREDENTIALS401Wrong email or passwordACCOUNT_LOCKED401Too many failed login attemptsACCOUNT_INACTIVE401Account suspendedFORBIDDEN403Not authorized to access this resourceNOT_FOUND404Resource does not existEMAIL_TAKEN409Email address already registeredSCAN_LIMIT_REACHED409Hourly scan limit reachedAPI_KEY_LIMIT409Maximum API keys already createdRATE_LIMITED429Too many requestsINTERNAL_ERROR500Unexpected server error

2.5 Pagination
List endpoints support pagination via query parameters:
GET /api/v1/scans?page=1&page_size=20

Response includes:
{
  "data": {
    "items": [...],
    "total": 87,
    "page": 1,
    "page_size": 20,
    "pages": 5
  }
}
Default page size: 20
Maximum page size: 100

2.6 Rate Limiting
Rate limit headers are returned on every response:
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1716571200
Retry-After: 60  (only on 429 responses)
Rate limits per endpoint group:
Endpoint GroupLimitPOST /auth/register5 per hour per IPPOST /auth/login10 per minute per IPPOST /auth/refresh20 per minute per userPOST /scans/5 per hour per userGET /scans/60 per minute per userGET /reports/{id}/pdf20 per minute per userAll other endpoints60 per minute per user

3. Data Schemas
Pydantic schemas used across multiple endpoints are defined here once and referenced throughout.
3.1 Finding Schema
pythonclass FindingResponse(BaseModel):
    id:                   UUID
    title:                str
    description:          str
    business_impact:      str
    severity:             Literal["critical", "high", "medium", "low", "info"]
    owasp_category:       str
    owasp_id:             str
    dimension:            str
    evidence:             str
    recommendation:       str
    effort:               Literal["low", "medium", "high"]
    references:           list[ReferenceItem]
    false_positive_risk:  Literal["low", "medium", "high"]
    created_at:           datetime
3.2 DimensionScore Schema
pythonclass DimensionScoreResponse(BaseModel):
    dimension_name:   str
    score:            float  # 0.0 to 10.0, one decimal place
    weight:           float  # e.g. 0.25
    grade:            Literal["A", "B", "C", "D", "F"]
    findings_count:   int
3.3 Scan Summary Schema
pythonclass ScanSummaryResponse(BaseModel):
    id:               UUID
    url:              str
    domain:           str
    profile:          Literal["quick", "standard", "deep"]
    status:           Literal["pending", "running", "completed", "failed"]
    overall_score:    float | None
    grade:            str | None
    label:            str | None
    findings_count:   int
    critical_count:   int
    high_count:       int
    medium_count:     int
    low_count:        int
    info_count:       int
    created_at:       datetime
    completed_at:     datetime | None
3.4 Scan Detail Schema
pythonclass ScanDetailResponse(BaseModel):
    id:                 UUID
    url:                str
    domain:             str
    ip_address:         str | None
    profile:            str
    status:             str
    overall_score:      float | None
    grade:              str | None
    label:              str | None
    findings_count:     int
    critical_count:     int
    high_count:         int
    medium_count:       int
    low_count:          int
    info_count:         int
    duration_seconds:   float | None
    error_message:      str | None
    findings:           list[FindingResponse]
    dimension_scores:   list[DimensionScoreResponse]
    created_at:         datetime
    updated_at:         datetime
    completed_at:       datetime | None
3.5 User Schema
pythonclass UserResponse(BaseModel):
    id:           UUID
    email:        str
    full_name:    str
    is_active:    bool
    created_at:   datetime

4. Authentication Endpoints
4.1 Register
Creates a new user account.
POST /api/v1/auth/register
Authentication: None required
Rate limit: 5 per hour per IP
Request body:
json{
  "email": "james@example.com",
  "password": "SecurePassword123",
  "full_name": "James Gichia"
}
Request schema:
pythonclass RegisterRequest(BaseModel):
    email:      EmailStr
    password:   str = Field(min_length=8, max_length=128)
    full_name:  str = Field(min_length=2, max_length=255)

    @validator('password')
    def password_must_contain_number(cls, v):
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one number')
        return v

    @validator('email')
    def email_to_lowercase(cls, v):
        return v.lower()
Success response — 201 Created:
json{
  "success": true,
  "data": {
    "user": {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "email": "james@example.com",
      "full_name": "James Gichia",
      "is_active": true,
      "created_at": "2026-05-24T10:30:00Z"
    }
  },
  "message": "Account created successfully"
}
Error responses:
ConditionStatusError CodeEmail already registered409EMAIL_TAKENPassword too short422VALIDATION_ERRORPassword has no number422VALIDATION_ERRORInvalid email format422VALIDATION_ERRORRate limit exceeded429RATE_LIMITED

4.2 Login
Authenticates a user and returns JWT tokens.
POST /api/v1/auth/login
Authentication: None required
Rate limit: 10 per minute per IP
Request body:
json{
  "email": "james@example.com",
  "password": "SecurePassword123"
}
Request schema:
pythonclass LoginRequest(BaseModel):
    email:    EmailStr
    password: str
Success response — 200 OK:
json{
  "success": true,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "expires_in": 900,
    "refresh_token": "dGhpcyBpcyBhIHJlZnJlc2ggdG9rZW4...",
    "user": {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "email": "james@example.com",
      "full_name": "James Gichia"
    }
  }
}
Response field notes:

access_token — JWT, expires in 15 minutes (900 seconds)
expires_in — seconds until access token expires
refresh_token — opaque token, expires in 7 days
Refresh token also set as httpOnly cookie named wg_refresh

Error responses:
ConditionStatusError CodeWrong email or password401INVALID_CREDENTIALSAccount locked401ACCOUNT_LOCKEDAccount inactive401ACCOUNT_INACTIVERate limit exceeded429RATE_LIMITED
Security note:
Failed login attempts are tracked per IP address. After 5 consecutive failures the IP is locked for 15 minutes. The error message never reveals whether the email exists — always returns INVALID_CREDENTIALS for both wrong email and wrong password.

4.3 Refresh Token
Exchanges a valid refresh token for a new access token.
POST /api/v1/auth/refresh
Authentication: None required (refresh token in cookie or body)
Rate limit: 20 per minute per user
Request body (optional — cookie is preferred):
json{
  "refresh_token": "dGhpcyBpcyBhIHJlZnJlc2ggdG9rZW4..."
}
The refresh token is accepted either from the wg_refresh httpOnly cookie or from the request body. Cookie is preferred for web dashboard. Request body is used by CLI connected mode.
Success response — 200 OK:
json{
  "success": true,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "expires_in": 900
  }
}
Refresh token rotation:
On every successful refresh the old refresh token is invalidated and a new one is issued. The new refresh token is set in the wg_refresh cookie.
Error responses:
ConditionStatusError CodeRefresh token invalid401INVALID_TOKENRefresh token expired401INVALID_TOKENRefresh token already used401INVALID_TOKEN

4.4 Logout
Invalidates the current session.
POST /api/v1/auth/logout
Authentication: Required (Bearer token)
Rate limit: Standard
Request body: None
Success response — 200 OK:
json{
  "success": true,
  "message": "Logged out successfully"
}
Behavior:

Invalidates the refresh token in the database
Clears the wg_refresh cookie
Access token remains technically valid until expiry — client must discard it
Subsequent requests with the old refresh token return INVALID_TOKEN


5. Scan Endpoints
5.1 Submit Scan
Creates a new scan job and queues it for processing.
POST /api/v1/scans/
Authentication: Required
Rate limit: 5 per hour per user
Request body:
json{
  "url": "https://example.com",
  "profile": "standard"
}
Request schema:
pythonclass ScanCreateRequest(BaseModel):
    url:      HttpUrl
    profile:  Literal["quick", "standard", "deep"] = "standard"

    @validator('url')
    def url_must_be_public(cls, v):
        # Validation performed by engine validator
        # Private IPs, localhost rejected here
        validate_scan_target(str(v))
        return v
Success response — 201 Created:
json{
  "success": true,
  "data": {
    "scan_id": "7f3d9c2e-8b1a-4f5e-9d7c-2a8b3e1f6d4c",
    "status": "pending",
    "url": "https://example.com",
    "profile": "standard",
    "created_at": "2026-05-24T10:30:00Z"
  },
  "message": "Scan queued successfully"
}
Error responses:
ConditionStatusError CodeInvalid URL format400INVALID_URLURL resolves to private IP400PRIVATE_TARGETHourly scan limit reached409SCAN_LIMIT_REACHEDNot authenticated401AUTH_REQUIREDRate limit exceeded429RATE_LIMITED
Post-submit flow:
The client should immediately redirect to the scan progress page and begin polling GET /api/v1/scans/{id}/status every 3 seconds.

5.2 List Scans
Returns a paginated list of the authenticated user's scans.
GET /api/v1/scans/
Authentication: Required
Rate limit: 60 per minute per user
Query parameters:
ParameterTypeDefaultDescriptionpageinteger1Page numberpage_sizeinteger20Results per page (max 100)statusstringallFilter by statusprofilestringallFilter by profiledomainstring—Filter by domain (partial match)
Example request:
GET /api/v1/scans?page=1&page_size=20&status=completed
Success response — 200 OK:
json{
  "success": true,
  "data": {
    "items": [
      {
        "id": "7f3d9c2e-8b1a-4f5e-9d7c-2a8b3e1f6d4c",
        "url": "https://example.com",
        "domain": "example.com",
        "profile": "standard",
        "status": "completed",
        "overall_score": 7.2,
        "grade": "C",
        "label": "Fair",
        "findings_count": 12,
        "critical_count": 0,
        "high_count": 3,
        "medium_count": 5,
        "low_count": 4,
        "info_count": 0,
        "created_at": "2026-05-24T10:30:00Z",
        "completed_at": "2026-05-24T10:32:17Z"
      }
    ],
    "total": 24,
    "page": 1,
    "page_size": 20,
    "pages": 2
  }
}

5.3 Get Scan Status
Returns the current status and progress of a scan. Used for polling during active scans.
GET /api/v1/scans/{scan_id}/status
Authentication: Required
Rate limit: 60 per minute per user
Path parameters:
ParameterTypeDescriptionscan_idUUIDScan identifier
Success response — 200 OK:
json{
  "success": true,
  "data": {
    "scan_id": "7f3d9c2e-8b1a-4f5e-9d7c-2a8b3e1f6d4c",
    "status": "running",
    "progress_percent": 60,
    "current_check": "DNS Security",
    "checks_completed": 6,
    "checks_total": 10,
    "elapsed_seconds": 47
  }
}
Status field values:
StatusMeaningpendingQueued — worker not yet picked uprunningWorker executing checkscompletedAll checks done — results availablefailedScan encountered an error
Progress tracking:
The worker updates scan progress in Redis (not PostgreSQL) for performance — Redis is fast enough for frequent small updates. The status endpoint reads from Redis during active scans and from PostgreSQL for completed or failed scans.
Error responses:
ConditionStatusError CodeScan not found404NOT_FOUNDScan belongs to another user403FORBIDDEN

5.4 Get Scan Detail
Returns the complete scan result including all findings and dimension scores.
GET /api/v1/scans/{scan_id}
Authentication: Required
Rate limit: 60 per minute per user
Path parameters:
ParameterTypeDescriptionscan_idUUIDScan identifier
Query parameters:
ParameterTypeDefaultDescriptionseveritystringallFilter findings by severity
Success response — 200 OK:
json{
  "success": true,
  "data": {
    "id": "7f3d9c2e-8b1a-4f5e-9d7c-2a8b3e1f6d4c",
    "url": "https://example.com",
    "domain": "example.com",
    "ip_address": "93.184.216.34",
    "profile": "standard",
    "status": "completed",
    "overall_score": 7.2,
    "grade": "C",
    "label": "Fair",
    "findings_count": 12,
    "critical_count": 0,
    "high_count": 3,
    "medium_count": 5,
    "low_count": 4,
    "info_count": 0,
    "duration_seconds": 47.3,
    "dimension_scores": [
      {
        "dimension_name": "transport_security",
        "score": 8.5,
        "weight": 0.25,
        "grade": "B",
        "findings_count": 1
      },
      {
        "dimension_name": "header_configuration",
        "score": 4.5,
        "weight": 0.20,
        "grade": "D",
        "findings_count": 3
      }
    ],
    "findings": [
      {
        "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        "title": "Missing Content Security Policy",
        "description": "Your site has no Content Security Policy defined.",
        "business_impact": "Without a CSP, browsers have no instructions on which content sources are trusted.",
        "severity": "high",
        "owasp_category": "A02:2025 - Security Misconfiguration",
        "owasp_id": "A02",
        "dimension": "header_configuration",
        "evidence": "No Content-Security-Policy header found in HTTP response",
        "recommendation": "Add the following header to all HTTP responses: Content-Security-Policy: default-src 'self'",
        "effort": "low",
        "references": [
          {
            "type": "owasp",
            "title": "OWASP CSP Cheat Sheet",
            "url": "https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html"
          }
        ],
        "false_positive_risk": "low",
        "created_at": "2026-05-24T10:32:17Z"
      }
    ],
    "created_at": "2026-05-24T10:30:00Z",
    "updated_at": "2026-05-24T10:32:17Z",
    "completed_at": "2026-05-24T10:32:17Z"
  }
}
Error responses:
ConditionStatusError CodeScan not found404NOT_FOUNDScan belongs to another user403FORBIDDENScan not yet completed200Returns partial data with status field

5.5 Delete Scan
Permanently deletes a scan and all associated findings and reports.
DELETE /api/v1/scans/{scan_id}
Authentication: Required
Rate limit: Standard
Path parameters:
ParameterTypeDescriptionscan_idUUIDScan identifier
Success response — 204 No Content
No response body on successful deletion.
Behavior:

Cascades to delete all findings, dimension scores, and reports
Deletes report files from disk
Cannot be undone

Error responses:
ConditionStatusError CodeScan not found404NOT_FOUNDScan belongs to another user403FORBIDDENScan currently running409CONFLICT

6. Report Endpoints
6.1 Get JSON Report
Returns the complete scan result as a machine-readable JSON report.
GET /api/v1/reports/{scan_id}/json
Authentication: Required
Rate limit: Standard
Success response — 200 OK:
Content-Type: application/json

{
  "scan_id": "7f3d9c2e-...",
  "generated_at": "2026-05-24T10:32:17Z",
  "target": {
    "url": "https://example.com",
    "domain": "example.com",
    "ip_address": "93.184.216.34",
    "profile": "standard",
    "scanned_at": "2026-05-24T10:30:00Z"
  },
  "score": {
    "overall": 7.2,
    "grade": "C",
    "label": "Fair",
    "dimensions": [ ... ]
  },
  "summary": {
    "total_findings": 12,
    "critical": 0,
    "high": 3,
    "medium": 5,
    "low": 4,
    "info": 0
  },
  "findings": [ ... ],
  "metadata": {
    "duration_seconds": 47.3,
    "webguard_version": "1.0.0",
    "scan_profile": "standard"
  }
}
Note: This endpoint returns the report directly as JSON — not wrapped in the standard API envelope. This is intentional — the JSON report is a standalone document.

6.2 Get HTML Report
Returns the complete styled HTML report.
GET /api/v1/reports/{scan_id}/html
Authentication: Required
Rate limit: Standard
Success response — 200 OK:
Content-Type: text/html; charset=utf-8
Content-Disposition: inline; filename="webguard_example.com_20260524.html"

[Full HTML document]

6.3 Get PDF Report
Returns the professional PDF report as a downloadable file.
GET /api/v1/reports/{scan_id}/pdf
Authentication: Required
Rate limit: 20 per minute per user
Success response — 200 OK:
Content-Type: application/pdf
Content-Disposition: attachment; filename="webguard_example.com_20260524.pdf"
Content-Length: [file size in bytes]

[Binary PDF content]
Report generation behavior:
Reports are generated once when the scan completes and cached as files. Subsequent requests to the report endpoints serve the cached files — they do not regenerate. If the file is missing for any reason it is regenerated on demand.
Error responses (all report endpoints):
ConditionStatusError CodeScan not found404NOT_FOUNDScan belongs to another user403FORBIDDENScan not yet completed409CONFLICTReport file missing500INTERNAL_ERROR

7. Dashboard Endpoints
7.1 Get Dashboard Statistics
Returns aggregated statistics for the authenticated user's dashboard.
GET /api/v1/dashboard/stats
Authentication: Required
Rate limit: 60 per minute per user
Success response — 200 OK:
json{
  "success": true,
  "data": {
    "total_scans": 24,
    "completed_scans": 22,
    "average_score": 7.4,
    "findings_summary": {
      "total": 156,
      "critical": 2,
      "high": 34,
      "medium": 67,
      "low": 45,
      "info": 8
    },
    "score_history": [
      {
        "scan_id": "7f3d9c2e-...",
        "domain": "example.com",
        "overall_score": 7.2,
        "grade": "C",
        "created_at": "2026-05-24T10:30:00Z"
      }
    ],
    "recent_scans": [
      {
        "id": "7f3d9c2e-...",
        "domain": "example.com",
        "overall_score": 7.2,
        "grade": "C",
        "label": "Fair",
        "status": "completed",
        "created_at": "2026-05-24T10:30:00Z"
      }
    ]
  }
}
Response field notes:

score_history — last 10 completed scans ordered by date ascending (for charting)
recent_scans — last 5 scans of any status ordered by date descending
average_score — mean of all completed scan scores, null if no completed scans
Empty state: all counts return 0, arrays return empty


8. API Key Endpoints
8.1 Create API Key
Generates a new API key for the authenticated user.
POST /api/v1/keys/
Authentication: Required (JWT only — not API key)
Rate limit: Standard
Request body:
json{
  "label": "CI Pipeline Production"
}
Request schema:
pythonclass APIKeyCreateRequest(BaseModel):
    label: str = Field(min_length=1, max_length=100)
Success response — 201 Created:
json{
  "success": true,
  "data": {
    "id": "b2c3d4e5-...",
    "key": "wg_live_a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0",
    "key_prefix": "wg_live_a",
    "label": "CI Pipeline Production",
    "created_at": "2026-05-24T10:30:00Z"
  },
  "message": "API key created. Store this key securely — it will not be shown again."
}
Critical security note:
The key field is returned exactly once in this response. It is never returned again from any endpoint. The user must copy it immediately. If lost a new key must be generated.
Error responses:
ConditionStatusError CodeUser already has 5 active keys409API_KEY_LIMITAuthenticated via API key403FORBIDDEN
Why API key creation requires JWT?
Allowing API key creation via API key would mean a compromised key could create unlimited additional keys. JWT authentication requires the user's actual password — providing a higher security guarantee for key creation.

8.2 List API Keys
Returns all API keys for the authenticated user. Key values are never returned.
GET /api/v1/keys/
Authentication: Required
Rate limit: Standard
Success response — 200 OK:
json{
  "success": true,
  "data": {
    "keys": [
      {
        "id": "b2c3d4e5-...",
        "key_prefix": "wg_live_a",
        "label": "CI Pipeline Production",
        "is_active": true,
        "last_used_at": "2026-05-24T08:15:00Z",
        "created_at": "2026-05-01T09:00:00Z"
      }
    ]
  }
}

8.3 Delete API Key
Permanently revokes an API key.
DELETE /api/v1/keys/{key_id}
Authentication: Required
Rate limit: Standard
Path parameters:
ParameterTypeDescriptionkey_idUUIDAPI key identifier
Success response — 204 No Content
Behavior:

Key is immediately invalidated
Any in-flight requests using this key complete normally
Subsequent requests using this key return 401 INVALID_TOKEN
Key record is deleted from database

Error responses:
ConditionStatusError CodeKey not found404NOT_FOUNDKey belongs to another user403FORBIDDEN

9. User Settings Endpoints
9.1 Get Current User
Returns the authenticated user's profile.
GET /api/v1/users/me
Authentication: Required
Rate limit: Standard
Success response — 200 OK:
json{
  "success": true,
  "data": {
    "id": "550e8400-...",
    "email": "james@example.com",
    "full_name": "James Gichia",
    "is_active": true,
    "created_at": "2026-05-01T09:00:00Z"
  }
}

9.2 Update Profile
Updates the user's full name.
PATCH /api/v1/users/me
Authentication: Required
Rate limit: Standard
Request body:
json{
  "full_name": "James K. Gichia"
}
Success response — 200 OK:
json{
  "success": true,
  "data": {
    "id": "550e8400-...",
    "email": "james@example.com",
    "full_name": "James K. Gichia",
    "is_active": true,
    "created_at": "2026-05-01T09:00:00Z"
  },
  "message": "Profile updated successfully"
}

9.3 Update Password
Changes the user's password. Requires current password for verification.
POST /api/v1/users/me/password
Authentication: Required (JWT only)
Rate limit: 5 per hour per user
Request body:
json{
  "current_password": "OldPassword123",
  "new_password": "NewSecurePassword456"
}
Success response — 200 OK:
json{
  "success": true,
  "message": "Password updated successfully"
}
Behavior:
After a successful password change all existing refresh tokens for the user are invalidated. The user remains logged in with their current access token until it expires.
Error responses:
ConditionStatusError CodeCurrent password incorrect401INVALID_CREDENTIALSNew password too weak422VALIDATION_ERRORAuthenticated via API key403FORBIDDEN

9.4 Delete Account
Permanently deletes the user account and all associated data.
DELETE /api/v1/users/me
Authentication: Required (JWT only)
Rate limit: 2 per day per user
Request body:
json{
  "password": "CurrentPassword123",
  "confirmation": "DELETE MY ACCOUNT"
}
Request schema:
pythonclass DeleteAccountRequest(BaseModel):
    password:     str
    confirmation: Literal["DELETE MY ACCOUNT"]
Success response — 204 No Content
Behavior:

Verifies password before deletion
Requires exact string "DELETE MY ACCOUNT" as confirmation
Permanently deletes user record
CASCADE deletes all scans, findings, dimension scores, reports, and API keys
Deletes all report files from disk
Cannot be undone

Error responses:
ConditionStatusError CodeWrong password401INVALID_CREDENTIALSConfirmation string wrong422VALIDATION_ERRORAuthenticated via API key403FORBIDDEN

10. Health Check Endpoint
10.1 Health Check
Returns the health status of the API and its dependencies. Used by monitoring and deployment systems.
GET /api/v1/health
Authentication: None required
Rate limit: None
Success response — 200 OK:
json{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2026-05-24T10:30:00Z",
  "dependencies": {
    "database": "healthy",
    "redis": "healthy",
    "worker": "healthy"
  }
}
Degraded response — 200 OK:
json{
  "status": "degraded",
  "version": "1.0.0",
  "timestamp": "2026-05-24T10:30:00Z",
  "dependencies": {
    "database": "healthy",
    "redis": "healthy",
    "worker": "unhealthy"
  }
}
Unhealthy response — 503 Service Unavailable:
json{
  "status": "unhealthy",
  "version": "1.0.0",
  "timestamp": "2026-05-24T10:30:00Z",
  "dependencies": {
    "database": "unhealthy",
    "redis": "healthy",
    "worker": "unknown"
  }
}

11. WebSocket Endpoint
11.1 Scan Progress WebSocket
Real-time scan progress updates via WebSocket. An alternative to polling the status endpoint.
WS /api/v1/ws/scans/{scan_id}
Authentication: JWT token as query parameter
Connection URL:
wss://api.webguard.io/api/v1/ws/scans/7f3d9c2e-...?token=eyJhbGci...
Server messages:
json{
  "type": "progress",
  "data": {
    "status": "running",
    "progress_percent": 60,
    "current_check": "DNS Security",
    "checks_completed": 6,
    "checks_total": 10
  }
}
json{
  "type": "completed",
  "data": {
    "scan_id": "7f3d9c2e-...",
    "overall_score": 7.2,
    "grade": "C"
  }
}
json{
  "type": "failed",
  "data": {
    "error": "Connection timeout reaching target"
  }
}
Behavior:

Server closes connection on scan completion or failure
Client should fall back to polling if WebSocket connection fails
Token validated on connection — invalid token closes connection immediately

Note: The web dashboard uses polling by default in Version 1.0. WebSocket support is implemented but marked as an enhancement. Polling every 3 seconds is acceptable for Version 1 and avoids WebSocket connection management complexity on the frontend.

12. Changelog
VersionDateChanges1.0May 2026Initial API specification

This document is version controlled. Any change to the API must be reflected here before implementation. Breaking changes require a version increment.
Last updated: May 2026
