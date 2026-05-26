A02:2025 — Security MisconfigurationFile: docs/research/owasp/a02-security-misconfiguration.md1. DefinitionSecurity Misconfiguration occurs when a system, application, or cloud service is set up incorrectly from a security perspective, creating exploitable vulnerabilities. This category moved from fifth position in 2021 to second in 2025 — reflecting how the increasing complexity of modern software has made misconfiguration the dominant source of real-world vulnerabilities.OWASP data shows that 3.00% of applications tested had one or more of the 16 CWEs in this category. The rise is directly attributed to the growing reliance on configuration-driven behavior in modern frameworks, cloud platforms, and containerized deployments.2. How It ManifestsMissing Security Headers
The application returns HTTP responses without security-relevant headers that instruct browsers on safe behavior.Default Credentials Left Unchanged
Administrative interfaces, databases, or cloud services deployed with vendor default credentials that have never been changed.Unnecessary Features Enabled
Debug mode left active in production, verbose error pages exposing stack traces, unused services running, unnecessary HTTP methods enabled.Improper Cloud Storage Permissions
S3 buckets, Azure Blob Storage, or Google Cloud Storage configured for public access when they should be private.Missing Security Updates
Server software, frameworks, or infrastructure components running with known security patches not applied.Verbose Error Messages
Application error pages that reveal framework versions, database types, file system paths, or internal IP addresses to the end user.3. Real World ImpactCapital One (2019) — A misconfigured Web Application Firewall combined with an overly permissive IAM role allowed an attacker to access AWS metadata service via SSRF. Over 100 million customer records were exposed. Capital One paid $80 million in regulatory fines and $190 million in class action settlements.Microsoft Power Apps (2021) — Default configuration of Power Apps portals set table permissions to allow public access. This affected 38 organizations including American Airlines, Ford, and multiple US government agencies. 38 million records were exposed before Microsoft changed the default.GoDaddy (2021) — A misconfigured provisioning system exposed the credentials and SSH keys of 1.2 million managed WordPress customers. Attackers had access for two months before discovery.4. Passive Detection ApproachSecurity misconfiguration is one of the categories best suited to passive detection. Most misconfigurations are directly observable in HTTP responses without any payload injection.What passive scanning detects:ObservableWhat It IndicatesSeverityMissing CSP headerNo browser content source policyHighMissing HSTS headerConnections can be downgraded to HTTPHighMissing X-Content-Type-OptionsMIME type sniffing enabledMediumMissing Referrer-PolicySensitive URL data leaked in referrerLowServer version in headerVersion information aids attacker reconnaissanceHighX-Powered-By presentFramework disclosedMediumDebug headers presentDebug mode activeHighDirectory listing enabledFile structure exposedHighVerbose error pageStack trace or path exposedHighDefault error page with framework infoServer software exposedMedium5. WebGuard Implementation ScopeCheck modules:

engine/checks/security_headers.py
engine/checks/information_disclosure.py
Security headers checks:HDR-001: Content-Security-Policy absent
         → Severity: High

HDR-002: Content-Security-Policy contains unsafe-inline
         → Severity: Medium

HDR-003: Content-Security-Policy contains unsafe-eval
         → Severity: Medium

HDR-004: Strict-Transport-Security absent
         → Severity: High

HDR-005: HSTS max-age below 31536000
         → Severity: Medium

HDR-006: X-Content-Type-Options absent or not set to nosniff
         → Severity: Medium

HDR-007: Referrer-Policy absent
         → Severity: Low

HDR-008: Referrer-Policy set to unsafe-url
         → Severity: Medium

HDR-009: Permissions-Policy absent
         → Severity: Low

HDR-010: Cross-Origin-Opener-Policy absent
         → Severity: LowInformation disclosure checks:INF-001: Server header contains version number
         → Severity: High
         → Evidence: Exact header value

INF-002: X-Powered-By header present
         → Severity: Medium
         → Evidence: Exact header value

INF-003: X-AspNet-Version or X-AspNetMvc-Version present
         → Severity: High
         → Evidence: Exact header value

INF-004: Stack trace or framework error page detected
         → Severity: High
         → Evidence: Error page content indicators

INF-005: Internal IP address in response headers
         → Severity: High
         → Evidence: IP address found

INF-006: Debug mode indicators in headers
         → Severity: High
         → Evidence: Header name and value6. ScoringDimension: Header Configuration and Information ExposureFindingSeverityScore DeductionMissing CSPHigh−2.0Missing HSTSHigh−2.0Server version disclosedHigh−2.0Stack trace exposedHigh−2.0Missing X-Content-Type-OptionsMedium−1.0X-Powered-By presentMedium−1.0Short HSTS max-ageMedium−1.0Missing Referrer-PolicyLow−0.5Missing Permissions-PolicyLow−0.57. Remediation GuidanceContent Security Policy:
Content-Security-Policy: default-src 'self';
  script-src 'self';
  style-src 'self';
  img-src 'self' data:;
  font-src 'self';
  connect-src 'self';
  frame-ancestors 'none'HSTS:
Strict-Transport-Security: max-age=31536000; includeSubDomains; preloadRemove version disclosure:
# Apache — httpd.conf
ServerTokens Prod
ServerSignature Off

# Nginx — nginx.conf
server_tokens off;

# IIS — web.config
<httpRuntime enableVersionHeader="false" />Effort: Low — configuration file changes
Impact of fix: High — removes reconnaissance value for attackers8. References
OWASP A02:2025 — https://owasp.org/Top10/2025/A02_2025-Security_Misconfiguration/
OWASP HTTP Security Headers Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html
OWASP CSP Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html
Mozilla HTTP Observatory — https://observatory.mozilla.org
CWE-16: Configuration
CWE-209: Generation of Error Message Containing Sensitive Information
