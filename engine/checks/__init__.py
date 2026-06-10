"""
Passive check modules — one per OWASP Top 10 2025 category.

Each module is a concrete subclass of BaseCheck. All checks are async
and receive a shared ScanTarget. They never re-fetch the target URL.

Check modules (mapped to functional checks and scan profiles):

  Quick profile:
    transport_security  — TLS, HSTS, HTTP→HTTPS redirect
    ssl_certificate     — certificate validity, expiry, chain
    security_headers    — CSP, X-Frame-Options, and others

  Standard profile (all Quick +):
    cookie_security         — HttpOnly, Secure, SameSite
    information_disclosure  — Server header, X-Powered-By, debug indicators
    cors_config             — CORS header misconfigurations
    dns_security            — SPF, DMARC, CAA records
    sensitive_files         — robots.txt, .git, .env exposure indicators
    content_protocol        — mixed content, HTTP/2, SRI

  Deep profile (all Standard +):
    component_safety    — JS library versions, CVE lookup via NVD/OSV
"""
