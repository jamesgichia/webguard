A07:2025 — Authentication Failures
File: docs/research/owasp/a07-authentication-failures.md

1. Definition
Authentication Failures occur when functions related to user identity, authentication, and session management are implemented incorrectly — allowing attackers to compromise passwords, keys, session tokens, or to assume other users' identities. This category maintains its position at seventh in 2025 with a slight name change from Identification and Authentication Failures to more accurately reflect its 36 CWEs.
The increased use of standardized authentication frameworks appears to be having a beneficial effect on occurrence rates — but custom authentication implementations remain highly vulnerable.

2. How It Manifests
Weak Session Management
Session tokens that are predictable, not invalidated on logout, transmitted over HTTP, or have excessively long expiry times.
Credential Stuffing Vulnerability
No rate limiting or lockout on authentication endpoints enabling automated use of breached credential lists.
Weak Password Policy
Applications accepting short, simple, or commonly used passwords. No enforcement of minimum complexity requirements.
Insecure Password Storage
Passwords stored in plaintext or using weak hashing algorithms (MD5, SHA1 without salting) that are trivially reversible.
Missing Multi-Factor Authentication
High-value applications without MFA as an option or requirement — single factor authentication is easily bypassed through phishing or credential theft.
Exposed Session Tokens
Session identifiers transmitted in URL parameters rather than cookies, appearing in server logs and browser history.

3. Real World Impact
RockYou (2009) — 32 million passwords stored in plaintext were stolen and leaked. The RockYou list remains the most commonly used password cracking wordlist today — directly enabling credential stuffing attacks against other sites.
Dropbox (2012) — Hashed passwords stolen from Dropbox were cracked because they were hashed with MD5 without unique salts. 68 million credentials were eventually published. The breach was not fully disclosed until 2016.
Twitter (2020) — Authentication failures in Twitter's internal admin tools allowed attackers who had obtained employee credentials through social engineering to access and take over high-profile accounts including Barack Obama, Elon Musk, and Bill Gates. The attack netted over $100,000 in Bitcoin within hours.

4. Passive Detection Approach
Many authentication failures are in backend logic not observable from external HTTP responses. However several indicators are passively detectable.
What passive scanning detects:
ObservableWhat It IndicatesSeveritySession cookie without HttpOnly flagSession token accessible to JavaScriptHighSession cookie without Secure flagSession token transmitted over HTTPHighSession cookie without SameSite attributeCSRF and session theft riskMediumLogin page served over HTTPCredentials transmitted in plaintextCriticalSession token in URL parametersToken exposed in logs and historyHighAutocomplete not disabled on password fieldsPassword cached by browserLowNo evidence of CSRF token in formsCross-site request forgery possibleMedium

5. WebGuard Implementation Scope
Check module: engine/checks/cookie_security.py
AUTH-001: Session cookie missing HttpOnly flag
          → Severity: High
          → Evidence: Cookie name and observed flags

AUTH-002: Session cookie missing Secure flag on HTTPS site
          → Severity: High
          → Evidence: Cookie name and observed flags

AUTH-003: Session cookie missing SameSite attribute
          → Severity: Medium
          → Evidence: Cookie name

AUTH-004: SameSite=None without Secure flag
          → Severity: High
          → Evidence: Cookie attributes

AUTH-005: Cookie with very long or no expiry on apparent session cookie
          → Severity: Low
          → Evidence: Cookie Max-Age or Expires value

AUTH-006: Broad cookie Domain attribute
          → Severity: Low
          → Evidence: Cookie Domain value

6. Scoring
Dimension: Cookie Security (weight: 20%)
FindingSeverityScore DeductionMissing HttpOnly on session cookieHigh−2.0Missing Secure on session cookieHigh−2.0SameSite=None without SecureHigh−2.0Missing SameSite attributeMedium−1.0Excessive cookie expiryLow−0.5Broad Domain attributeLow−0.5

7. Remediation Guidance
Secure cookie configuration:
Set-Cookie: sessionid=abc123;
  HttpOnly;
  Secure;
  SameSite=Strict;
  Path=/;
  Max-Age=3600
Framework-specific examples:
Django:
pythonSESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Strict'
SESSION_COOKIE_AGE = 3600
Express.js:
javascriptapp.use(session({
  cookie: {
    secure: true,
    httpOnly: true,
    sameSite: 'strict',
    maxAge: 3600000
  }
}))
Effort: Low — configuration changes in most frameworks
Impact of fix: High — protects session tokens from theft

8. References

OWASP A07:2025 — https://owasp.org/Top10/2025/A07_2025-Authentication_Failures/
OWASP Authentication Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
OWASP Session Management Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html
CWE-287: Improper Authentication
CWE-384: Session Fixation
CWE-613: Insufficient Session Expiration
