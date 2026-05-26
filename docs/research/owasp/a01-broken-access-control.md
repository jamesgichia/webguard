A01:2025 — Broken Access ControlFile: docs/research/owasp/a01-broken-access-control.md1. DefinitionBroken Access Control occurs when an application fails to properly enforce restrictions on what authenticated or unauthenticated users are permitted to do. Users can act outside their intended permissions — accessing data they should not see, performing actions they should not be allowed to perform, or reaching functionality reserved for other roles.In the OWASP Top 10 2025 this category retains its position at number one and now absorbs Server-Side Request Forgery (SSRF), reflecting how both failures share the same root cause — the application does not adequately control what resources and actions are accessible.OWASP data shows that on average 3.73% of applications tested had one or more of the 40 CWEs in this category.2. How It ManifestsBroken Object Level Authorization
An application returns data based on a user-supplied identifier without checking whether the requesting user is permitted to access that object.# User A's order
GET /api/orders/1042

# User B changes the ID — receives User A's data
GET /api/orders/1041Broken Function Level Authorization
Administrative or privileged functionality is accessible to unprivileged users because the UI hides the link but the endpoint is unprotected.# Admin panel accessible directly
GET /admin/users
GET /admin/delete-user/5Directory Traversal
An application serves files from a path that can be manipulated to access files outside the intended directory.GET /files/../../../etc/passwdCORS Misconfiguration
An overly permissive Cross-Origin Resource Sharing policy allows unauthorized origins to make authenticated requests to the API.Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: trueSSRF (now included in A01:2025)
An application fetches remote resources based on user-supplied URLs without validating that the destination is authorized. An attacker can supply internal network addresses to probe internal services.# Application fetches user-supplied URL
POST /fetch
{ "url": "http://169.254.169.254/latest/meta-data/" }3. Real World ImpactFacebook (2018) — A broken access control vulnerability in the "View As" feature allowed attackers to steal access tokens of other users. Approximately 50 million accounts were affected. Facebook was fined €17 million by the Irish Data Protection Commissioner under GDPR.Optus (2022) — An unauthenticated API endpoint allowed sequential enumeration of customer records including names, dates of birth, phone numbers, email addresses, and identity document numbers. 9.8 million customer records were exposed. The breach triggered Australia's largest ever data breach investigation.US Federal Agency (2022) — CISA reported that attackers exploited broken access control on an internal network to access sensitive systems after pivoting from an internet-facing application. SSRF was the initial access vector used to reach internal metadata services.4. Passive Detection ApproachActive testing of broken access control requires attempting to access protected resources — which is outside WebGuard's passive scope. However several observable indicators are detectable passively:What passive scanning can detect:ObservableWhat It IndicatesSeverityCORS wildcard with credentialsAny origin can make authenticated API callsCriticalCORS wildcard without credentialsOverly permissive cross-origin policyHighMissing X-Frame-Options headerClickjacking risk — UI redressing attacksHighrobots.txt disclosing admin pathsAdmin panel paths revealed to attackersMediumSensitive paths in sitemap.xmlInternal URL structure exposedMediumDirectory listing enabledFile system structure exposedHighOverly permissive Access-Control-Allow-MethodsDangerous HTTP methods permittedMediumWhat passive scanning cannot detect:

IDOR (Insecure Direct Object References) — requires authenticated requests
Privilege escalation — requires testing with different user roles
Function level authorization failures — requires knowing what endpoints exist
5. WebGuard Implementation ScopeCheck module: engine/checks/cors_config.pyChecks implemented:CORS-001: Access-Control-Allow-Origin: * present
          → Severity: High
          → Evidence: Header value

CORS-002: Access-Control-Allow-Origin: * with Access-Control-Allow-Credentials: true
          → Severity: Critical
          → Evidence: Both header values

CORS-003: Access-Control-Allow-Methods includes unsafe methods (PUT, DELETE, PATCH)
          on non-API pages
          → Severity: Medium
          → Evidence: Header value and page type

CORS-004: X-Frame-Options missing
          → Severity: High
          → Evidence: Absence of header
          → Note: Also checked in security_headers.py

CORS-005: CORS headers present on non-API HTML pages
          → Severity: Low
          → Evidence: Header presence on content pageLimitation note:
Document clearly in report output that WebGuard's A01 coverage is limited to observable CORS and header indicators. Full access control testing requires authenticated active scanning.6. ScoringDimension: Header Configuration (CORS findings) and Transport Security (X-Frame-Options)FindingSeverityScore DeductionCORS wildcard with credentialsCritical−3.0CORS wildcard without credentialsHigh−2.0X-Frame-Options missingHigh−2.0Unsafe CORS methods on non-API pageMedium−1.0CORS headers on content pagesLow−0.57. Remediation GuidanceCORS wildcard fix:
# Replace wildcard with specific allowed origins
Access-Control-Allow-Origin: https://yourdomain.com

# If multiple origins needed — validate server-side and reflect dynamically
# Never use * with Allow-Credentials: trueX-Frame-Options fix:
# Prevent all framing
X-Frame-Options: DENY

# Allow framing from same origin only
X-Frame-Options: SAMEORIGINEffort: Low — HTTP header configuration change
Impact of fix: High — eliminates clickjacking and CORS-based attack surface8. References
OWASP A01:2025 — https://owasp.org/Top10/2025/A01_2025-Broken_Access_Control/
OWASP CORS Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/CORS_Cheat_Sheet.html
OWASP Clickjacking Defense — https://cheatsheetseries.owasp.org/cheatsheets/Clickjacking_Defense_Cheat_Sheet.html
CWE-284: Improper Access Control
CWE-352: Cross-Site Request Forgery
CWE-918: Server-Side Request Forgery
