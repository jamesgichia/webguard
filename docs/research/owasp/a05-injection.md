A05:2025 — Injection
File: docs/research/owasp/a05-injection.md

1. Definition
Injection flaws occur when an application sends untrusted data to an interpreter as part of a command or query. The attacker's hostile data can trick the interpreter into executing unintended commands or accessing data without proper authorization.
Injection fell from third position in 2021 to fifth in 2025. It maintains the greatest number of CVEs associated with its 38 CWEs — meaning it is the most documented category of vulnerabilities. It includes SQL Injection, Cross-Site Scripting (XSS), Command Injection, LDAP Injection, and related flaws.

2. How It Manifests
SQL Injection
User-supplied data is included in a database query without parameterization. An attacker can alter the query logic to extract, modify, or delete database content.
# Vulnerable query
SELECT * FROM users WHERE email = '$email' AND password = '$password'

# Attacker input — password field: ' OR '1'='1
# Resulting query authenticates without valid credentials
SELECT * FROM users WHERE email = 'admin@test.com' AND password = '' OR '1'='1'
Cross-Site Scripting (XSS)
User-supplied data is included in HTML output without encoding. An attacker injects script that executes in other users' browsers, stealing session tokens or performing actions on their behalf.
Command Injection
User input is passed to operating system commands. An attacker appends additional commands to the intended command.
LDAP Injection
User input is included in LDAP queries without sanitization, allowing authentication bypass or directory data extraction.

3. Real World Impact
Heartland Payment Systems (2008) — SQL injection against a web application gave attackers access to the payment processing network. 130 million credit and debit card numbers were stolen. Heartland paid over $140 million in settlements and fines.
British Airways (2018) — A Magecart attack injected malicious JavaScript into the British Airways website through a compromised third-party script. 500,000 customers had their payment card details skimmed. British Airways was fined £20 million under GDPR.
Equifax (2017) — An Apache Struts vulnerability (a form of injection through the OGNL expression language) was exploited to gain access to servers containing 147 million Americans' personal data including Social Security numbers and credit card details. Equifax paid over $700 million in settlements.

4. Passive Detection Approach
Critical limitation to document clearly:
Injection vulnerabilities fundamentally cannot be detected through passive scanning alone. Detecting SQL injection requires sending malicious SQL syntax. Detecting XSS requires injecting script payloads. These are active tests that WebGuard deliberately does not perform.
What passive scanning can detect (indirect indicators only):
ObservableWhat It IndicatesSeverityMissing Content-Security-PolicyXSS impact magnified without CSPHighCSP with unsafe-inlineXSS execution not blocked by CSPMediumVerbose SQL error messages in responsesSQL errors confirm injection vulnerabilityCriticalDatabase error strings in page contentBackend errors exposedHigh
Passive detection is meaningful for one specific case:
If an application returns database error strings in HTTP responses (ORA-xxxxx, MySQLSyntaxErrorException, etc.) this is both a misconfiguration finding and a strong indicator of injection vulnerability — because it confirms the database layer is reachable and errors are not handled.

5. WebGuard Implementation Scope
Check module: Handled within engine/checks/information_disclosure.py
INJ-001: Database error strings detected in HTTP response
         → Severity: Critical
         → Patterns: MySQL error, ORA-, PostgreSQL, SQLSTATE, 
                     Unclosed quotation mark, JDBC, SQLException
         → Evidence: Matched error string in response

INJ-002: Missing Content-Security-Policy
         → Severity: High
         → Note: Also captured in security_headers.py
         → Relationship: Absence of CSP means XSS has maximum impact

INJ-003: CSP present but contains unsafe-inline directive
         → Severity: Medium
         → Evidence: CSP header value
         → Note: unsafe-inline allows inline XSS execution
Critical documentation requirement:
The WebGuard report must clearly state in the A05 section:

WebGuard performs passive scanning only. SQL injection, XSS, command injection, and related active injection tests are outside the scope of this assessment. The findings above represent passive indicators only. A professional penetration test is required for comprehensive injection vulnerability assessment.


6. Scoring
Dimension: Information Exposure (database errors), Header Configuration (CSP relationship)
FindingSeverityScore DeductionDatabase error in responseCritical−3.0Missing CSP (XSS impact amplifier)High−2.0CSP with unsafe-inlineMedium−1.0

7. Remediation Guidance
Prevent SQL injection:
python# Never do this
query = "SELECT * FROM users WHERE email = '" + email + "'"

# Always use parameterized queries
cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
Prevent XSS with CSP:
Content-Security-Policy: default-src 'self';
  script-src 'self';
  style-src 'self'
Suppress database errors:
python# Never expose raw exceptions to users
try:
    result = db.query(...)
except DatabaseError:
    log.error("Database error", exc_info=True)
    return {"error": "An internal error occurred"}
Effort: Medium — requires code changes to parameterize queries
Impact of fix: Critical — SQL injection is among the most severe vulnerability classes

8. References

OWASP A05:2025 — https://owasp.org/Top10/2025/A05_2025-Injection/
OWASP SQL Injection Prevention Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html
OWASP XSS Prevention Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html
CWE-89: SQL Injection
CWE-79: Cross-site Scripting
CWE-77: Command Injection
