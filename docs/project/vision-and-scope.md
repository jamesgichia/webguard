WebGuard — Vision and Scope
Document: Vision and Scope
Version: 1.0
Status: Draft
Created: May 2026
Author: James Gichia
Repository: docs/project/vision-and-scope.md

1. Vision
WebGuard will become the universal security layer that every web application is built with — as standard and expected as a linter, a test suite, or a version control system. A future where no developer ships code without first knowing exactly what their application exposes to the world. Where no business operates a website in ignorance of its security posture. Where data privacy is not an afterthought but a foundation verified before deployment and monitored continuously.
The silent threats that destroy businesses, compromise customer data, and erode institutional trust are detectable. WebGuard makes them visible — before they are exploited.

2. Problem Statement
Most organizations do not know their websites are vulnerable until something goes wrong. Not because the vulnerabilities are hidden or sophisticated — but because nobody looked. The tools that could find these flaws are either too complex for non-specialists, too expensive for small organizations, or produce reports that decision makers cannot understand or act on.
The consequence is a world where:

Developers ship code without security visibility
Businesses operate websites with unknown critical flaws
Customers trust organizations that have not earned that trust technically
Institutions face regulatory fines for vulnerabilities that were entirely preventable
Security remains the domain of specialists rather than every developer

WebGuard exists to change this — starting with the developer, at the moment before deployment, when fixing a flaw costs nothing compared to what it costs after a breach.

3. Product Vision Statement

For developers, security teams, and businesses who need to understand their web security posture, WebGuard is a passive web security scanner that surfaces openly detectable vulnerabilities and delivers clear, actionable reports. Unlike existing tools that are either too complex for non-experts or too expensive for smaller organizations, WebGuard speaks the language of both engineers and decision makers — making professional security analysis accessible to every team regardless of budget or technical expertise.


4. Target Users
Primary User — The Developer
The developer is the heart of WebGuard. They integrate it into their workflow, run it before deployment, and use it in CI/CD pipelines. They care about accuracy, speed, JSON output, and CLI usability. They are the first line of defense — and when they catch a flaw before deployment, every downstream consequence is prevented.
Secondary User — The DevOps Engineer
Works alongside developers. Integrates WebGuard into automated pipelines. Cares about reliability, API access, and machine-readable output. Values tools that run silently and report clearly.
Tertiary User — The Security Consultant
Uses WebGuard for baseline assessments on client engagements. Values professional PDF reports they can deliver directly to clients. Cares about accuracy, credibility, and time efficiency.
Future Users — Version 2 and Beyond

IT managers and CTOs needing executive security visibility
Small and medium businesses with no dedicated security team
Compliance officers needing documented security assessments
Students and educators in cybersecurity programs


5. Product Scope
5.1 What WebGuard Is
WebGuard is a passive web security scanner. It analyzes everything a website voluntarily exposes to the public — HTTP headers, TLS configuration, cookies, DNS records, component versions, and server information — and maps its findings against the OWASP Top 10 framework.
It delivers results through:

A CLI tool for developers and pipelines
A web dashboard for teams and organizations
A REST API for custom integrations

Every finding includes a severity rating, an OWASP category mapping, a plain English explanation, a business impact statement, and a specific remediation guide.
5.2 What WebGuard Is Not
These boundaries are deliberate and non-negotiable for Version 1:
Not an active scanner
WebGuard does not inject payloads, probe for injection vulnerabilities, or attempt to exploit anything. It observes only what is publicly and passively available. This is an architectural and ethical decision — not a technical limitation.
Not a penetration testing replacement
WebGuard complements professional penetration testing. It does not replace it. A security consultant using WebGuard for a baseline assessment should clearly communicate this distinction to their clients.
Not a compliance auditing tool
Version 1 does not make definitive compliance claims against GDPR, PCI-DSS, or ISO 27001. Findings may be relevant to these frameworks but WebGuard does not certify compliance.
Not an enterprise platform
Version 1 does not include team workspaces, multi-user organizations, billing, or enterprise support contracts. These are planned for future versions.

6. Version Roadmap
Version 1.0 — Foundation
The core product. Passive scanning. Dual interface. Professional reporting.
✅ 10 passive check modules
✅ Multi-dimensional scoring (0.0 – 10.0)
✅ Three scan profiles (Quick, Standard, Deep)
✅ CLI tool published on PyPI
✅ Web dashboard with scan history
✅ REST API with authentication
✅ JSON, HTML, and PDF reports
✅ First-class remediation guidance
Version 2.0 — Depth
Adding continuity and compliance awareness.
⬜ Scheduled and recurring scans
⬜ Slack and email alerting on new findings
⬜ Compliance mapping (GDPR, PCI-DSS, ISO 27001)
⬜ Score trending and historical charts
⬜ GitHub Actions and GitLab CI plugins
⬜ Billing and subscription tiers
⬜ Team workspaces
Version 3.0 — Scale
Enterprise readiness and ecosystem expansion.
⬜ Optional active scanning module (with authorization verification)
⬜ White-label reporting for security consultants
⬜ Verified security badge system
⬜ CVE feed integration and real-time alerts
⬜ Multi-user enterprise workspaces
⬜ API access tiers
⬜ Browser extension
Long Term Vision
The universal web security standard.
⬜ Domain ownership verification for authorized active scanning
⬜ Industry benchmark comparisons by sector
⬜ Security posture certification
⬜ Integration with major development platforms
⬜ Open standard for passive security reporting

7. Assumptions
The following assumptions underpin the scope and design of WebGuard Version 1.0:

Target websites are publicly accessible over HTTP or HTTPS
Users have legal authorization to scan any URL they submit
The NVD and OSV APIs remain publicly available for CVE lookups
Developers are the primary adopters and will introduce the tool to their organizations
Passive scanning provides sufficient value to justify Version 1 without active checks
Python 3.11+ is available in all target development environments


8. Constraints
ConstraintDescriptionPassive onlyNo active scanning, payload injection, or exploitation of any kindLegal complianceTool must operate within computer access laws across all jurisdictionsNo false positivesAccuracy is prioritized over detection breadth at all timesScope disciplineVersion 1 features are fixed — new ideas go to the backlogSingle developerArchitecture must be manageable by one developer without cutting quality

9. Success Metrics
Version 1.0 Launch Success
MetricTargetTimeframePyPI downloads50060 days post launchGitHub stars10060 days post launchUser feedback responses10 genuine responses60 days post launchFalse positive reportsZero confirmedFirst 30 daysAverage scan timeUnder 3 minutesStandard profileCommunity mentions3 independent posts90 days post launch
Long Term Success Indicators

WebGuard becomes a recommended tool in developer security communities
Organizations reference WebGuard scans in security documentation
The tool is cited in cybersecurity educational resources
Active contributors join the open source project


10. Risks and Boundaries
RiskBoundary SetLegal misuseStrict ToS and acceptable use policy on all interfacesScope creepAll out-of-scope ideas documented in future-ideas.md backlogOverclaimingMarketing never claims active scanning or compliance certificationFalse positivesOnly report findings with high confidence — when in doubt, omitDependency failureCVE API failures degrade gracefully — scan completes without CVE data

11. Relationship to Other Documents
DocumentRelationshipProject CharterParent document — defines the project this scope servesRequirements DocumentChild document — details functional requirements within this scopeSystem ArchitectureTechnical document — implements this scope in codeLegal DocumentsEnforces the ethical boundaries defined in this scopeRisk RegisterExpands on the risks identified in Section 10

This document is version controlled. All changes must be committed with a descriptive message and reviewed before merging.
Last updated: May 2026
