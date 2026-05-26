A06:2025 — Insecure Design
File: docs/research/owasp/a06-insecure-design.md

1. Definition
Insecure Design refers to risks stemming from missing or ineffective security controls in the architecture and design of a system. This is distinct from insecure implementation — it is not about code bugs but about fundamental design decisions that never considered security as a requirement.
This category was introduced in 2021 and fell two spots from fourth to sixth in 2025, reflecting that the industry has made noticeable improvements in threat modeling and secure design practices. However it remains a critical category because design flaws are the hardest to fix — they often require architectural changes rather than simple patches.

2. How It Manifests
No Rate Limiting on Sensitive Endpoints
Login, password reset, and OTP verification endpoints that accept unlimited requests — enabling brute force and credential stuffing attacks.
Predictable Resource Identifiers
Sequential integer IDs for users, orders, or sensitive records — enabling enumeration attacks.
Missing Business Logic Controls
A ticket booking system that does not prevent a user from booking a negative quantity. A discount system that can be abused to generate unlimited discounts. Logic that was designed for normal use cases but never threat-modeled for abuse cases.
Insecure Password Recovery
Password reset flows that use security questions with guessable answers, or that send passwords in plaintext via email.
Absent Defense in Depth
Systems designed with a single security boundary — if that boundary is breached there is nothing else stopping full compromise.

3. Real World Impact
Panera Bread (2018) — Customer data including names, email addresses, physical addresses, and partial credit card numbers was exposed through an unauthenticated API endpoint. The API used sequential customer IDs enabling enumeration of all records. The researcher who discovered and reported the issue was initially ignored for eight months.
Peloton (2021) — An API endpoint returned private user data including age, city, gender, and workout statistics without authentication. The insecure design meant any user ID could be queried without credentials.
Instagram (2019) — A brute force vulnerability in the password reset flow (no rate limiting on SMS OTP verification) allowed attackers to take over any account given sufficient time and requests.

4. Passive Detection Approach
Insecure design is primarily detected through active testing and manual review. However several design weakness indicators are passively observable.
What passive scanning detects:
ObservableWhat It IndicatesSeverityNo rate limiting headers on login pageBrute force may be possibleMediumSequential or predictable URL patternsObject enumeration may be possibleLowSecurity.txt absentNo responsible disclosure process definedInfoPassword field autocomplete not disabledCredential caching riskLowLogin form served over HTTPCredentials transmitted in plaintextCritical
Important limitation:
Insecure design detection through passive scanning is inherently limited. The indicators above are weak signals. A professional security review or threat modeling exercise is required for meaningful insecure design assessment.

5. WebGuard Implementation Scope
Check module: Handled within engine/checks/security_headers.py and engine/checks/sensitive_files.py
DES-001: Login page served over HTTP
         → Severity: Critical
         → Evidence: Login form detected on HTTP page

DES-002: Security.txt not found at /.well-known/security.txt
         → Severity: Info
         → Evidence: 404 response at security.txt path
         → Note: Positive finding — presence is good practice

DES-003: Cache-Control headers missing on apparent login or account pages
         → Severity: Medium
         → Evidence: Page URL pattern and missing Cache-Control: no-store

DES-004: X-Frame-Options missing — enables UI redressing attacks
         → Severity: High
         → Note: Also captured in A01 and security headers check
Critical documentation requirement:
The A06 section of every WebGuard report must include:

Insecure design vulnerabilities require architectural review and threat modeling to detect comprehensively. Passive scanning reveals observable indicators only. A full security design review is recommended for critical applications.


6. Scoring
Dimension: Header Configuration
FindingSeverityScore DeductionLogin page on HTTPCritical−3.0Missing Cache-Control on sensitive pageMedium−1.0Security.txt absentInfo0.0

7. Remediation Guidance
Implement rate limiting:
python# Using Flask-Limiter as example
from flask_limiter import Limiter

@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    ...
Implement security.txt:
# /.well-known/security.txt
Contact: security@yourcompany.com
Expires: 2027-01-01T00:00:00.000Z
Preferred-Languages: en
Cache control on sensitive pages:
Cache-Control: no-store, no-cache, must-revalidate
Pragma: no-cache
Effort: Medium to High — rate limiting requires code changes, design review requires dedicated effort
Impact of fix: High — rate limiting alone prevents a large class of automated attacks

8. References

OWASP A06:2025 — https://owasp.org/Top10/2025/A06_2025-Insecure_Design/
OWASP Threat Modeling — https://owasp.org/www-community/Threat_Modeling
OWASP Proactive Controls — https://owasp.org/www-project-proactive-controls/
OWASP ASVS — https://owasp.org/www-project-application-security-verification-standard/
CWE-284: Improper Access Control
CWE-307: Improper Restriction of Excessive Authentication Attempts
