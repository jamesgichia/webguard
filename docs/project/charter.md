WebGuard — Project Charter
Document: Project Charter
Version: 1.0
Status: Draft
Created: May 2026
Author: James Gichia
Repository: docs/project/charter.md

1. Project Overview
Project Name: WebGuard
Project Type: Open Source Security Tool with Commercial SaaS Layer
Version Scope: Version 1.0

2. The Problem
Human beings are generally ignorant of persisting silent threats. A business owner does not wake up thinking about missing security headers or weak TLS configurations on their website. A development team ships code focused on features, deadlines, and functionality — not the invisible gaps quietly waiting to be found by the wrong person.
Yet it is precisely these silent, openly detectable flaws that are most dangerous. They require no sophisticated attack. They ask no permission. They sit exposed on the public surface of a website, visible to anyone who knows where to look, until the day someone with malicious intent decides to look.
When that day comes, the consequences are not technical. They are deeply human:

A business loses the reputation it spent years building
Sensitive customer data is exposed to people it was never meant for
Regulatory bodies impose fines that threaten financial survival
Customers withdraw their trust — and trust, once lost, rarely returns
An institution that existed to serve people becomes the reason those people were harmed

The tragedy is not that these flaws are undetectable. They are entirely detectable — passively, safely, and without any specialist knowledge — if the right tool exists to surface them. The tragedy is that most organizations never look until it is too late.

3. The Solution
WebGuard is a passive web security scanner that analyzes everything a website voluntarily exposes to the public — headers, certificates, cookies, configurations, components, and DNS records — and translates what it finds into clear, actionable intelligence.
It does not probe. It does not inject. It does not guess. It observes, analyzes, and reports — the way a careful and knowledgeable professional would if asked to review a website's security posture before it faced the world.
WebGuard delivers its findings through two interfaces built for different people with the same goal:

A CLI tool for developers who want security insights in their terminal and their pipelines
A web dashboard for teams and organizations who want visibility, history, and professional reports

Every finding comes with a plain English explanation, a business impact statement, and a specific remediation guide. Not a list of problems — a roadmap to solutions.

4. Vision Statement
A world where businesses and institutions operate without fear of compromise. Where customers trust the organizations they engage with because that trust has been earned and maintained. Where data privacy is not a promise but a guarantee — built in from the beginning, verified before deployment, and monitored continuously.
WebGuard exists to make that world more achievable — one scan at a time, starting with the developer before a single line of code reaches the public.

5. Mission Statement
To give every developer, team, and organization — regardless of budget or technical expertise — the visibility they need to understand and improve their web security posture, through a tool that is honest about what it finds, clear about what it means, and specific about how to fix it.

6. The Person This Tool Exists For
WebGuard is built first and foremost for the developer.
Not because businesses and institutions matter less — but because the developer is where the chain of consequences either begins or is broken. A developer who catches an exposed server version, a missing Content Security Policy, or a weak TLS configuration before deployment has already prevented the breach, the fine, the headline, and the loss of customer trust that would have followed.
Every feature in WebGuard is evaluated against one question:

Does this help a developer find and fix a security flaw before it reaches the public?

If the answer is yes, it belongs in the product. If the answer is no, it waits.

7. Target Audience
Primary — Version 1.0
Developers and DevOps engineers who want to integrate security analysis into their development workflow and CI/CD pipelines.
Secondary — Version 1.0
Security consultants who need a fast, reliable baseline assessment tool with professional reporting for client engagements.
Future Versions

Small and medium businesses with no dedicated security team
IT managers and CTOs who need executive-level security visibility
Compliance officers who need documented security assessments
Educational institutions and students learning web security


8. Project Scope
In Scope — Version 1.0
Core Engine

10 passive check modules covering all publicly observable security indicators
Asynchronous orchestration for fast concurrent scanning
Multi-dimensional scoring system (0.0 to 10.0, one decimal place)
Three scan profiles: Quick, Standard, and Deep
JSON, HTML, and PDF report generation
First-class remediation guidance for every finding

Passive Checks Include

Transport security and TLS/SSL configuration
HTTP security headers analysis
Cookie security flags
Information and version disclosure
Component safety and CVE matching
CORS configuration
DNS security records
Sensitive file exposure indicators
SSL certificate details
Content and protocol security

CLI Tool

Published on PyPI as webguard
Scan profiles, output formats, and verbose mode
Professional terminal output with Rich
CI/CD pipeline friendly

API Backend

FastAPI with JWT authentication
Asynchronous scan job processing via Celery and Redis
Full scan result and report retrieval
API key management for pipeline integration
Rate limiting and input validation

Web Dashboard

React frontend with Tailwind CSS
Landing page, authentication, dashboard, scan submission
Real-time scan progress
Findings display with remediation cards
PDF and HTML report download
Scan history
Mobile responsive

Out of Scope — Version 1.0
The following are deliberately excluded from Version 1.0 and documented for future versions:

Active scanning and payload injection of any kind
Scheduled and recurring scans
Detailed compliance mapping (GDPR, PCI-DSS, ISO 27001)
White-label reporting
Team workspaces and multi-user organizations
Billing and subscription management
Browser extension
Mobile application
Slack and email alerting
Verified security badge system


9. Scoring Model
WebGuard uses a multi-dimensional scoring system across six security dimensions:
DimensionWeightTransport Security25%Header Configuration20%Cookie Security20%Component Safety15%Information Exposure10%DNS Security10%
Each dimension scores from 0.0 to 10.0. The overall score is a weighted average rounded to one decimal place.
ScoreGradeLabel9.0 – 10.0AExcellent7.5 – 8.9BGood6.0 – 7.4CFair4.0 – 5.9DPoor0.0 – 3.9FCritical

10. Technology Stack
LayerTechnologyScanning EnginePython 3.11+HTTP Clienthttpx (async)CLI FrameworkTyper + RichAPI BackendFastAPITask QueueCelery + RedisDatabasePostgreSQLORMSQLAlchemy + AlembicReport GenerationWeasyPrint + Jinja2FrontendReact + Tailwind CSSAuthenticationJWT + OAuth2ContainerizationDocker + Docker ComposeCI/CDGitHub ActionsError MonitoringSentry

11. Success Criteria
Version 1.0 is considered successfully delivered when:
Technical

All 10 passive check modules operational and tested
Scan accuracy verified against OWASP Juice Shop and DVWA
80% or above test coverage on the core engine
Zero critical security vulnerabilities in WebGuard itself
Full deployment operational on cloud infrastructure

Adoption

500 PyPI downloads within 60 days of launch
100 GitHub stars within 60 days of launch
10 genuine user feedback responses collected
At least 3 independent blog posts or mentions in security communities

Quality

No confirmed false positive reports from users in first 30 days
Average scan completion under 3 minutes for standard profile
PDF report readable and useful to a non-technical stakeholder


12. Project Risks
RiskLikelihoodImpactMitigationFalse positives damaging credibilityMediumHighExtensive testing, confidence scoring, user feedback mechanismScope creep delaying launchHighHighStrict Version 1 scope document, future-ideas backlogCVE API dependency or rate limitingMediumMediumCache responses, use multiple CVE sources (NVD + OSV)Passive scanning perceived as insufficient by professionalsMediumLowClear positioning as monitoring tool not pentest replacementLegal misuse by users scanning without authorizationLowHighClear ToS, acceptable use policy, and disclaimer on all interfaces

13. Project Timeline
PhaseFocusDuration0Research and DiscoveryWeeks 1–21Foundation and SetupWeek 32Core Scanning EngineWeeks 4–73CLI ToolWeek 84API BackendWeeks 9–115Web DashboardWeeks 12–156Testing and QAWeeks 16–177DeploymentWeek 188LaunchWeek 19

14. Guiding Principles
These principles govern every decision made during the development of WebGuard:
Accuracy before features
A finding reported with certainty is worth more than ten findings reported with doubt. WebGuard will never report what it cannot confirm.
Clarity over complexity
Every finding must be understandable to the person reading it. Technical accuracy and plain English are not opposites — WebGuard requires both.
The developer first
Every feature is evaluated against its value to the developer catching flaws before deployment. Features that do not serve this purpose wait for future versions.
Passive by design
WebGuard observes what is publicly available. It does not probe, inject, or exploit. This is not a limitation — it is a deliberate architectural and ethical decision.
Silent threats deserve a loud warning
The most dangerous vulnerabilities are the ones nobody is looking for. WebGuard exists to make the invisible visible before it becomes a crisis.


15. Authorization
This charter formally authorizes the WebGuard Version 1.0 project to proceed through all phases as documented.
Project Lead: James Gichia
Education: BSc Computer Science — Mama Ngina University (Studies completed April 2026, Graduation December 2026)
Specialization: Cybersecurity
Contact: jamesgichia15@gmail.com
GitHub: https://github.com/jamesgichia
LinkedIn: www.linkedin.com/in/jamesgichia
