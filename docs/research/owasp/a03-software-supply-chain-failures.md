A03:2025 — Software Supply Chain Failures
File: docs/research/owasp/a03-software-supply-chain-failures.md

1. Definition
Software Supply Chain Failures are breakdowns or compromises in the process of building, distributing, or updating software. They are caused by vulnerabilities or malicious changes in third-party code, tools, or dependencies that a system relies on.
This category is an expansion of the 2021 category Vulnerable and Outdated Components and now includes the broader scope of compromises occurring across the entire ecosystem of software dependencies, build systems, and distribution infrastructure. It was voted the top concern in the OWASP 2025 community survey.
This category has the fewest occurrences in collected data but the highest average exploit and impact scores — meaning when these vulnerabilities are exploited the consequences are severe.

2. How It Manifests
Outdated Frontend Libraries with Known CVEs
JavaScript libraries included directly in web pages — jQuery, Bootstrap, React, Angular, Lodash — at versions with documented vulnerabilities.
Malicious Package Injection
A package in the software supply chain is compromised — either through typosquatting, maintainer account compromise, or a malicious pull request — and the compromised version is distributed to downstream applications.
Missing Subresource Integrity
JavaScript and CSS loaded from external CDNs without SRI hash verification. If the CDN is compromised the malicious script runs in every user's browser.
End of Life Dependencies
Libraries, frameworks, or runtimes that are no longer receiving security patches — meaning newly discovered vulnerabilities will never be fixed.
Compromised Build Pipeline
The build and deployment process itself is tampered with — malicious code injected into CI/CD pipelines, build servers, or artifact repositories.

3. Real World Impact
SolarWinds (2020) — Attackers compromised the SolarWinds build system and injected malicious code into the Orion software update package. The compromised update was signed by SolarWinds and distributed to approximately 18,000 customers including US government agencies and Fortune 500 companies. This is considered one of the most significant supply chain attacks in history.
event-stream (2018) — A malicious actor was given ownership of a popular npm package with 2 million weekly downloads. They added a dependency that specifically targeted the Copay Bitcoin wallet and attempted to steal cryptocurrency. Demonstrated how dependency trees can be weaponized.
Polyfill.io (2024) — A Chinese company purchased the polyfill.io domain and CDN service used by over 100,000 websites. They modified the JavaScript served to inject malicious code into websites that included the polyfill without SRI verification.

4. Passive Detection Approach
Supply chain failures are partially detectable through passive scanning of publicly served web content.
What passive scanning detects:
ObservableWhat It IndicatesSeverityJavaScript library version in script tag or responseKnown vulnerable version in useHigh/CriticalExternal script without SRI hashCDN compromise would affect all usersMediumExternal CSS without SRI hashCDN compromise would affect all usersLowEnd-of-life library version detectedNo security patches forthcomingHighKnown malicious CDN domainsActive supply chain compromise indicatorCritical
What passive scanning cannot detect:

Server-side dependency vulnerabilities (not exposed in HTTP responses)
Build pipeline compromises
Package registry compromises not yet reflected in deployed versions


5. WebGuard Implementation Scope
Check module: engine/checks/component_safety.py
Checks implemented:
COMP-001: Detect JavaScript library name and version from script tags
          → Libraries checked: jQuery, Bootstrap, React, Angular, Vue,
            Lodash, Underscore, Moment.js, Handlebars, Backbone.js,
            Ember.js, Prototype.js, MooTools, Dojo, YUI
          → Method: Parse HTML for script src attributes and inline
            library version patterns
          → On version detection: query NVD API and OSV API for CVEs

COMP-002: CVE match found for detected library version
          → Severity: Critical (CVSS 9.0+), High (CVSS 7.0-8.9),
            Medium (CVSS 4.0-6.9), Low (CVSS <4.0)
          → Evidence: Library name, version, CVE ID, CVSS score

COMP-003: External script tag without integrity attribute
          → Severity: Medium
          → Evidence: Script src URL

COMP-004: External script with integrity but without crossorigin attribute
          → Severity: Low
          → Evidence: Script src URL

COMP-005: Library version matches end-of-life release
          → Severity: High
          → Evidence: Library name, version, EOL date

COMP-006: Known malicious or compromised CDN domain detected
          → Severity: Critical
          → Evidence: Domain name and script URL
CVE API integration:

Primary source: NVD API (https://nvd.nist.gov/developers/vulnerabilities)
Fallback source: OSV API (https://osv.dev/docs/)
Cache responses for 24 hours to avoid rate limiting
Graceful degradation: if both APIs unavailable, mark check inconclusive and note in report


6. Scoring
Dimension: Component Safety (weight: 15%)
FindingSeverityScore DeductionCritical CVE in detected libraryCritical−3.0High CVE in detected libraryHigh−2.0End-of-life libraryHigh−2.0Medium CVE in detected libraryMedium−1.0External script without SRIMedium−1.0Low CVE in detected libraryLow−0.5External CSS without SRILow−0.5

7. Remediation Guidance
Update vulnerable libraries:
html<!-- Before — vulnerable jQuery -->
<script src="https://code.jquery.com/jquery-1.12.4.min.js"></script>

<!-- After — current version with SRI -->
<script
  src="https://code.jquery.com/jquery-3.7.1.min.js"
  integrity="sha384-1H217gwSVyLSIfaLxHbE7dRb3v4mYCKbpQvzx0cegeju1MVsGrX5xXxaYymDFwe"
  crossorigin="anonymous">
</script>
Generate SRI hashes:
Use https://www.srihash.org/ to generate integrity hashes for external resources.
Automate dependency checking:
Integrate tools like npm audit, pip-audit, or Snyk into your CI/CD pipeline so vulnerabilities are caught before deployment.
Effort: Low to Medium — library updates and SRI attribute additions
Impact of fix: High — eliminates known exploitable vulnerabilities in frontend code

8. References

OWASP A03:2025 — https://owasp.org/Top10/2025/A03_2025-Software_Supply_Chain_Failures/
OWASP Component Analysis — https://owasp.org/www-community/Component_Analysis
NVD API Documentation — https://nvd.nist.gov/developers/vulnerabilities
OSV Database — https://osv.dev/
SRI Hash Generator — https://www.srihash.org/
CWE-1104: Use of Unmaintained Third Party Components
CWE-829: Inclusion of Functionality from Untrusted Control Sphere
