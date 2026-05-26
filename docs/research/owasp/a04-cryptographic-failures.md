A04:2025 — Cryptographic Failures
File: docs/research/owasp/a04-cryptographic-failures.md

1. Definition
Cryptographic Failures occur when an application fails to adequately protect data in transit or at rest through proper encryption. This category fell from second position in 2021 to fourth in 2025. The data indicates that on average 3.80% of applications have one or more of the 32 CWEs in this category.
This category focuses on root causes — weak or absent encryption — rather than the symptom (sensitive data exposure). Failures here lead directly to the exposure of passwords, credit card numbers, health records, personal identification data, and session tokens.

2. How It Manifests
Weak TLS Configuration
Servers supporting deprecated protocol versions (TLS 1.0, TLS 1.1, SSLv3) that have known vulnerabilities and are no longer considered secure.
Expired or Invalid Certificates
SSL certificates that have expired, are self-signed, or have broken certificate chains — causing browsers to warn users or fail silently depending on configuration.
Missing HTTPS Enforcement
Websites serving content over HTTP or failing to redirect HTTP requests to HTTPS — allowing credentials and session tokens to be transmitted in plaintext.
Missing HSTS
Sites using HTTPS but without HTTP Strict Transport Security — allowing downgrade attacks that force connections back to HTTP.
Weak Cipher Suites
Server configured to accept deprecated cipher suites with known cryptographic weaknesses (RC4, DES, 3DES, EXPORT ciphers).
Insecure Cookie Transmission
Cookies without the Secure flag transmitted over HTTP, exposing session tokens to network interception.

3. Real World Impact
Yahoo (2013–2014) — Weak encryption on stored passwords combined with poor key management contributed to the largest breach in history — 3 billion accounts compromised. Yahoo's eventual sale to Verizon was reduced by $350 million as a direct consequence.
Heartbleed (CVE-2014-0160) — A vulnerability in OpenSSL's TLS implementation allowed attackers to read memory from affected servers including private keys, session tokens, and plaintext passwords. Affected an estimated 17% of all HTTPS servers on the internet.
POODLE (2014) — An attack against SSLv3 forced connections to downgrade from TLS to SSLv3 where attackers could decrypt session cookies. SSL 3.0 is now universally disabled but systems still supporting TLS 1.0 remain vulnerable to similar downgrade attacks.

4. Passive Detection Approach
Cryptographic failures are among the most reliably detectable categories through passive scanning. TLS configuration, certificate validity, and HSTS headers are all externally observable.
What passive scanning detects:
ObservableWhat It IndicatesSeverityTLS 1.0 supportedDeprecated protocol — vulnerable to attacksCriticalTLS 1.1 supportedDeprecated protocol — PCI-DSS non-compliantCriticalCertificate expiredConnection not trustworthyCriticalCertificate expiring within 30 daysImminent expiry riskHighCertificate expiring within 90 daysPlanned renewal neededMediumSelf-signed certificateNo trusted CA verificationHighMissing HSTS headerDowngrade attack possibleHighHSTS max-age below one yearInsufficient protection durationMediumHTTP serving content without redirectData transmitted in plaintextCriticalMissing Secure flag on cookiesSession token transmitted over HTTPHigh

5. WebGuard Implementation Scope
Check modules:

engine/checks/transport_security.py
engine/checks/ssl_certificate.py
engine/checks/cookie_security.py (Secure flag component)

TLS checks:
TLS-001: TLS 1.0 supported
         → Severity: Critical
         → Method: TLS handshake negotiation attempt
         → Evidence: Protocol version negotiated

TLS-002: TLS 1.1 supported
         → Severity: Critical
         → Evidence: Protocol version negotiated

TLS-003: Only TLS 1.2 supported (TLS 1.3 not available)
         → Severity: Low (informational — TLS 1.2 is acceptable)
         → Evidence: Highest protocol version negotiated

TLS-004: HTTP content served without HTTPS redirect
         → Severity: Critical
         → Evidence: HTTP response code and content

TLS-005: HTTPS redirect present but HTTP page loads before redirect
         → Severity: Medium
         → Evidence: HTTP response observation
Certificate checks:
CERT-001: Certificate expired
          → Severity: Critical
          → Evidence: Expiry date

CERT-002: Certificate expiring within 30 days
          → Severity: High
          → Evidence: Expiry date and days remaining

CERT-003: Certificate expiring within 90 days
          → Severity: Medium
          → Evidence: Expiry date and days remaining

CERT-004: Self-signed certificate detected
          → Severity: High
          → Evidence: Issuer equals subject

CERT-005: Incomplete certificate chain
          → Severity: High
          → Evidence: Missing intermediate certificates

CERT-006: Certificate does not cover www subdomain
          → Severity: Low
          → Evidence: Subject alternative names list
HSTS checks:
HSTS-001: Strict-Transport-Security header absent
          → Severity: High

HSTS-002: HSTS max-age below 31536000 (one year)
          → Severity: Medium
          → Evidence: Actual max-age value

HSTS-003: HSTS missing includeSubDomains directive
          → Severity: Low

HSTS-004: HSTS missing preload directive
          → Severity: Info (informational only)

6. Scoring
Dimension: Transport Security (weight: 25%)
FindingSeverityScore DeductionTLS 1.0 supportedCritical−3.0TLS 1.1 supportedCritical−3.0HTTP without redirectCritical−3.0Certificate expiredCritical−3.0Missing HSTSHigh−2.0Certificate expiring within 30 daysHigh−2.0Self-signed certificateHigh−2.0Certificate expiring within 90 daysMedium−1.0HSTS max-age too shortMedium−1.0Missing includeSubDomainsLow−0.5

7. Remediation Guidance
Disable deprecated TLS versions (Nginx):
nginxssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:
            ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
ssl_prefer_server_ciphers off;
HSTS header:
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
Force HTTPS redirect (Nginx):
nginxserver {
    listen 80;
    server_name example.com;
    return 301 https://$server_name$request_uri;
}
Certificate renewal:
Use Let's Encrypt with Certbot for automatic certificate renewal:
bashcertbot renew --pre-hook "service nginx stop" --post-hook "service nginx start"
Effort: Low to Medium — configuration changes and certificate management
Impact of fix: Critical — protects all data in transit

8. References

OWASP A04:2025 — https://owasp.org/Top10/2025/A04_2025-Cryptographic_Failures/
OWASP Transport Layer Security Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet.html
Mozilla SSL Configuration Generator — https://ssl-config.mozilla.org/
Qualys SSL Labs Test — https://www.ssllabs.com/ssltest/
CWE-261: Weak Encoding for Password
CWE-326: Inadequate Encryption Strength
CWE-295: Improper Certificate Validation
