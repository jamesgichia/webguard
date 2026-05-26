A08:2025 — Software or Data Integrity Failures
File: docs/research/owasp/a08-software-data-integrity-failures.md

1. Definition
Software or Data Integrity Failures occur when code and infrastructure do not protect against integrity violations. This category is focused on the failure to maintain trust boundaries and verify the integrity of software, code, and data artifacts at a lower level than Software Supply Chain Failures (A03).
Where A03 addresses the supply chain ecosystem, A08 addresses the runtime trust boundaries — ensuring that code loaded and executed at runtime has not been tampered with and that data processed by the application has not been modified in unauthorized ways.

2. How It Manifests
Missing Subresource Integrity on CDN Resources
JavaScript or CSS loaded from external CDNs without cryptographic integrity verification. If the CDN serves modified content the application executes it without knowing.
Insecure Deserialization
An application accepts serialized objects from untrusted sources and deserializes them without verification — allowing attackers to manipulate object properties or execute arbitrary code.
Auto-Update Without Integrity Verification
Applications that automatically download and execute updates without verifying cryptographic signatures — allowing a man-in-the-middle to substitute malicious updates.
Unsigned Cookies or JWT Without Validation
Application uses unsigned cookies for security decisions, or accepts JWT tokens without verifying the signature — allowing token forgery.

3. Real World Impact
Polyfill.io (2024) — After domain ownership changed, the new owner modified the JavaScript served by the polyfill.io CDN to inject malicious code into over 100,000 websites. Sites that included the polyfill without SRI verification executed the malicious code in all their users' browsers.
CCleaner (2017) — Attackers compromised the CCleaner build infrastructure and signed a malicious version with the legitimate certificate. The integrity-verified, signed installer was downloaded by 2.27 million users before discovery.
npm event-stream (2018) — As described in A03 — malicious code injected into a widely used package specifically targeted cryptocurrency wallets. The integrity of the dependency tree was violated.

4. Passive Detection Approach
What passive scanning detects:
ObservableWhat It IndicatesSeverityExternal script without SRI integrity attributeCDN compromise executes in users' browsersMediumExternal CSS without SRI integrity attributeCDN compromise modifies page renderingLowScript with integrity but missing crossoriginSRI check may not function correctlyLowMixed HTTP/HTTPS resourcesHTTP resources can be modified in transitMedium

5. WebGuard Implementation Scope
Check module: engine/checks/component_safety.py (SRI checks) and engine/checks/content_protocol.py (mixed content)
INT-001: External script tag missing integrity attribute
         → Severity: Medium
         → Evidence: Script src URL

INT-002: External script has integrity but missing crossorigin attribute
         → Severity: Low
         → Evidence: Script src URL and attributes

INT-003: External CSS link missing integrity attribute
         → Severity: Low
         → Evidence: Link href URL

INT-004: Mixed content — HTTP resource on HTTPS page
         → Severity: Medium
         → Evidence: HTTP resource URLs found on HTTPS page

INT-005: HTTP resource loaded for JavaScript or CSS (active mixed content)
         → Severity: High
         → Evidence: HTTP script or stylesheet URL on HTTPS page

6. Scoring
Dimension: Component Safety (SRI) and Transport Security (mixed content)
FindingSeverityScore DeductionActive mixed content (HTTP JS/CSS on HTTPS)High−2.0External script without SRIMedium−1.0Passive mixed content (HTTP image/media)Medium−1.0External CSS without SRILow−0.5SRI without crossorigin attributeLow−0.5

7. Remediation Guidance
Add SRI to external scripts:
html<!-- Generate hash at https://www.srihash.org/ -->
<script
  src="https://cdn.example.com/library.min.js"
  integrity="sha384-[generated-hash]"
  crossorigin="anonymous">
</script>
Fix mixed content:
html<!-- Replace HTTP with HTTPS for all external resources -->
<!-- Or use protocol-relative URLs -->
<img src="//cdn.example.com/image.jpg" />

<!-- Or set upgrade-insecure-requests in CSP -->
Content-Security-Policy: upgrade-insecure-requests
Effort: Low — adding attributes to existing tags and updating resource URLs
Impact of fix: Medium to High — prevents CDN compromise from affecting users

8. References

OWASP A08:2025 — https://owasp.org/Top10/2025/A08_2025-Software_or_Data_Integrity_Failures/
MDN SRI Documentation — https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity
SRI Hash Generator — https://www.srihash.org/
CWE-353: Missing Support for Integrity Check
CWE-345: Insufficient Verification of Data Authenticity
CWE-494: Download of Code Without Integrity Check
