A09:2025 — Security Logging and Alerting Failures
File: docs/research/owasp/a09-security-logging-alerting-failures.md

1. Definition
Security Logging and Alerting Failures occur when an application fails to generate, store, or act on security-relevant events. This category retains its position at ninth in 2025 with a name change from Security Logging and Monitoring Failures to emphasize that logging without alerting provides minimal security value.
This category is consistently underrepresented in automated testing data because failures are not directly observable in HTTP responses — yet it is repeatedly voted into the Top 10 by security practitioners who see its real-world impact during incident response. Breaches go undetected for months because there is nothing watching the logs.
The average time to detect a breach is 181 days. Effective logging and alerting is the primary mechanism for reducing that window.

2. How It Manifests
Insufficient Logging
Authentication failures, access control violations, and input validation failures are not logged — leaving no audit trail of attack attempts or successful breaches.
Log Injection
Applications log user-supplied data without sanitization — allowing attackers to inject fake log entries or corrupt log files.
No Alerting on Suspicious Activity
Logs are generated but no system monitors them for anomalies. A brute force attack producing thousands of failed login entries goes unnoticed.
Logs Not Protected
Log files accessible to the application layer — an attacker who compromises the application can delete or modify logs to cover their tracks.
No Centralized Logging
Logs scattered across individual servers with no central collection — incident response requires manually reviewing each system separately.

3. Real World Impact
Target (2013) — Target's security monitoring system generated alerts about the malware being used to steal payment card data. The alerts were reviewed and dismissed without escalation. 40 million credit and debit card numbers were stolen over several weeks before external parties notified Target.
Equifax (2017) — The breach went undetected for 78 days partly because of inadequate monitoring. A TLS inspection tool had been inactive for 19 months due to an expired certificate — meaning encrypted malicious traffic was not being inspected.
Colonial Pipeline (2021) — The breach was not detected internally but by the company's billing system — an indirect indicator. Effective security alerting would have detected the lateral movement significantly earlier.

4. Passive Detection Approach
Logging and alerting configurations are entirely internal to the application. There is virtually no way to detect logging failures through external passive scanning. However one observable indicator exists.
What passive scanning can detect:
ObservableWhat It IndicatesSeverityVerbose error pages with stack tracesErrors not being handled and logged internallyHighDefault error pages with server versionApplication not handling exceptionsMediumNo security.txtNo responsible disclosure or incident contactInfo
Critical limitation:
WebGuard cannot assess whether logging is implemented, whether alerts are configured, or whether incident response processes exist. This is the category where the passive-only approach has the greatest limitation.

5. WebGuard Implementation Scope
Check module: Handled within engine/checks/information_disclosure.py
LOG-001: Verbose error page with stack trace detected
         → Severity: High
         → Evidence: Error content patterns in response
         → Note: Indicates errors are surfaced to users rather
                 than being caught, logged, and handled internally

LOG-002: Default framework error page detected
         → Severity: Medium
         → Evidence: Recognized error page template

LOG-003: Security.txt absent
         → Severity: Info
         → Note: Positive indicator of security maturity when present
Critical documentation requirement:
The A09 section of every WebGuard report must include:

Security logging and alerting cannot be assessed through passive external scanning. WebGuard can only observe indirect indicators such as unhandled errors surfaced to users. A comprehensive logging and monitoring assessment requires internal access to application infrastructure. We recommend reviewing your logging implementation against the OWASP Logging Cheat Sheet.


6. Scoring
Dimension: Information Exposure
FindingSeverityScore DeductionStack trace in error responseHigh−2.0Default framework error pageMedium−1.0Security.txt absentInfo0.0

7. Remediation Guidance
Implement structured logging:
pythonimport logging
import json

class SecurityLogger:
    def __init__(self):
        self.logger = logging.getLogger('security')

    def log_auth_failure(self, username, ip_address, reason):
        self.logger.warning(json.dumps({
            'event': 'authentication_failure',
            'username': username,
            'ip': ip_address,
            'reason': reason,
            'timestamp': datetime.utcnow().isoformat()
        }))
Handle errors gracefully:
python# Never expose internal errors to users
@app.errorhandler(Exception)
def handle_exception(e):
    # Log the full error internally
    app.logger.error(f"Unhandled exception: {e}", exc_info=True)
    # Return a safe, generic message to the user
    return {"error": "An internal error occurred. Please try again."}, 500
Create security.txt:
Contact: mailto:security@yourcompany.com
Expires: 2027-12-31T23:59:00.000Z
Preferred-Languages: en
Policy: https://yourcompany.com/security-policy
Effort: Medium — requires code changes for error handling and logging implementation
Impact of fix: High — dramatically reduces breach detection time

8. References

OWASP A09:2025 — https://owasp.org/Top10/2025/A09_2025-Security_Logging_and_Alerting_Failures/
OWASP Logging Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
OWASP Error Handling Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/Error_Handling_Cheat_Sheet.html
CWE-778: Insufficient Logging
CWE-779: Logging of Excessive Data
CWE-209: Generation of Error Message Containing Sensitive Information
