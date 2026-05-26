A10:2025 — Mishandling of Exceptional Conditions
File: docs/research/owasp/a10-mishandling-exceptional-conditions.md

1. Definition
Mishandling of Exceptional Conditions is a new category in the OWASP Top 10 2025, replacing SSRF (which has been absorbed into A01). It contains 24 CWEs focusing on improper error handling, logical errors, failing open, and other scenarios stemming from abnormal conditions that systems encounter.
This category describes what happens when software fails to prevent, detect, or respond appropriately to unusual and unpredictable situations — leading to crashes, unexpected behavior, security control bypasses, and sometimes complete system compromise.
The three core failure modes are:

The application does not prevent the unusual situation from occurring
The application does not identify the situation as it is happening
The application responds poorly or not at all when it occurs


2. How It Manifests
Failing Open
Security controls that default to permitting access when an error occurs rather than denying it. A failure in the authentication check causes the application to allow the request through.
python# Dangerous — failing open
try:
    if not is_authorized(user):
        return 403
except Exception:
    pass  # Exception silently swallowed — request proceeds
return serve_resource()
Null Pointer Dereferences
Accessing properties of null or undefined objects causing application crashes that expose stack traces, create denial of service conditions, or trigger undefined behavior exploitable for security bypass.
Integer Overflow and Underflow
Arithmetic operations that wrap around integer boundaries producing unexpected values — classic in systems programming but also relevant in web applications handling quantities, prices, or sizes.
Unhandled Promise Rejections and Async Errors
In JavaScript applications, unhandled promise rejections that silently fail — leaving security-critical operations (like permission checks or audit log writes) completed partially or not at all.
Exception-Based Logic Bypass
An attacker deliberately triggers an exception in the application to cause it to skip security validation logic and proceed to the protected resource.

3. Real World Impact
Apache Struts CVE-2017-5638 (Equifax breach) — An exception in the Jakarta multipart parser was not handled securely. The OGNL expression in the Content-Type header was evaluated during exception handling. Exceptional condition handling led directly to remote code execution and the exposure of 147 million records.
Cloudflare (2023) — A logic error in exception handling during a code change led to a significant outage affecting a large portion of Cloudflare's network. While not a security breach in this instance the same failure pattern in security controls would have had severe consequences.
Heartbleed (2014) — The underlying cause was a failure to validate the length parameter in the TLS heartbeat extension — an exceptional condition (invalid length value) that was not handled — causing the server to return memory contents beyond the intended buffer.

4. Passive Detection Approach
Exceptional condition handling failures are primarily internal application behaviors not directly observable through passive HTTP scanning. However the external symptoms of poor exception handling are sometimes visible.
What passive scanning detects:
ObservableWhat It IndicatesSeverityStack trace in HTTP responseUnhandled exception surfaced to userHighApplication crash page (500 error) with detailsException not caught and handledMediumFramework error page with internal pathsException handler revealing internal infoMediumInconsistent behavior on malformed requestsPossible exception handling gapsLow

5. WebGuard Implementation Scope
Check module: engine/checks/information_disclosure.py
EXC-001: Stack trace visible in HTTP response body
         → Severity: High
         → Evidence: Stack trace content pattern
         → Detection patterns:
           - "at [ClassName].[method]([file].java"
           - "Traceback (most recent call last)"
           - "File \"/path/to/file.py\""
           - "System.NullReferenceException"
           - "Fatal error:" (PHP)
           - "undefined is not a function" in response (JavaScript)

EXC-002: Detailed 500 error page with framework or path information
         → Severity: Medium
         → Evidence: Recognized framework error template

EXC-003: Application returning inconsistent status codes
         → Severity: Info
         → Evidence: Unexpected response codes

EXC-004: Error response revealing internal file system paths
         → Severity: High
         → Evidence: Path strings in error response
Critical documentation requirement:
The A10 section of every WebGuard report must include:

Mishandling of exceptional conditions encompasses a wide range of internal application behaviors that cannot be assessed through passive external scanning. WebGuard detects only the observable symptoms of poor exception handling — unhandled errors surfaced in HTTP responses. A comprehensive assessment requires code review and active testing. This is a new OWASP 2025 category reflecting the growing recognition of error handling as a security concern.


6. Scoring
Dimension: Information Exposure
FindingSeverityScore DeductionStack trace in responseHigh−2.0Internal paths in error responseHigh−2.0Detailed 500 error pageMedium−1.0

7. Remediation Guidance
Global exception handler — never fail open:
python# Python/Flask example
@app.errorhandler(Exception)
def handle_all_exceptions(e):
    # Log the full exception internally with context
    app.logger.error(
        f"Unhandled exception on {request.path}",
        exc_info=True,
        extra={'user': getattr(g, 'user_id', 'anonymous')}
    )
    # Return safe generic response — never expose internals
    return jsonify({"error": "An internal error occurred"}), 500
Explicit exception handling — fail closed:
python# Always fail closed on security decisions
def check_permission(user_id, resource_id):
    try:
        return permission_service.is_authorized(user_id, resource_id)
    except Exception as e:
        # Log the failure
        security_logger.error(f"Permission check failed: {e}")
        # Fail closed — deny access on error
        return False
Custom error pages (Nginx):
nginxerror_page 500 502 503 504 /50x.html;
location = /50x.html {
    root /var/www/error-pages;
    internal;
}
Effort: Medium — requires systematic review of exception handling throughout codebase
Impact of fix: High — prevents information disclosure and potential security bypass through error conditions

8. References

OWASP A10:2025 — https://owasp.org/Top10/2025/A10_2025-Mishandling_of_Exceptional_Conditions/
OWASP Error Handling Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/Error_Handling_Cheat_Sheet.html
CWE-391: Unchecked Error Condition
CWE-755: Improper Handling of Exceptional Conditions
CWE-754: Improper Check for Unusual or Exceptional Conditions
CWE-248: Uncaught Exception
