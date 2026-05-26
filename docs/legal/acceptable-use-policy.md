WebGuard — Acceptable Use Policy
Document: Acceptable Use Policy
Version: 1.0
Status: Draft
Created: May 2026
Author: James Gichia
Repository: docs/legal/acceptable-use-policy.md

---

This Acceptable Use Policy ("AUP") defines what you may and may not do with WebGuard. It applies to every interface through which you use the Service — the web dashboard, the CLI tool, and the REST API — and is incorporated by reference into the Terms of Service. Using WebGuard means you have read and accepted this policy.

The purpose of this policy is straightforward: WebGuard is a tool built to help people improve security. It must not be used to harm it.

---

1. The Core Principle

WebGuard exists to help developers, teams, and organizations understand their own security posture. Every permitted use of WebGuard serves this purpose. Every prohibited use undermines it.

The line is not technical — it is one of authorization and intent:

Permitted: Analyzing the security posture of systems you own or have explicit permission to analyze.
Prohibited: Using WebGuard on any system without the owner's explicit authorization, regardless of your intent.

---

2. Permitted Uses

You may use WebGuard to:

2.1 Scan Your Own Systems
Analyze the security posture of any web application, domain, or endpoint that you own or operate. This includes:

- Your personal projects and side projects
- Websites and web applications you have built
- Staging, development, and production environments you manage
- Domains registered to you or your organization

2.2 Scan with Explicit Authorization
Conduct security analysis on behalf of another organization, provided you have received explicit written authorization to do so. Common authorized contexts include:

- Security consultants conducting baseline assessments for clients who have engaged them to do so
- Penetration testers performing authorized security engagements
- Developers scanning their employer's systems as part of their job responsibilities
- Students or researchers scanning systems provided for that purpose (CTF environments, intentionally vulnerable applications such as OWASP Juice Shop, DVWA, or HackTheBox labs)

2.3 Integration into Development Workflows
Integrate WebGuard into CI/CD pipelines, pre-deployment checks, and automated security workflows for systems you have authorization to scan.

2.4 Educational and Research Purposes
Use WebGuard to learn about web security concepts, test understanding of security misconfigurations, and conduct research — provided all scanning targets are systems you own or are explicitly authorized to scan.

---

3. Prohibited Uses

The following uses are prohibited and may result in immediate account termination and referral to law enforcement.

3.1 Unauthorized Scanning
You may not submit any URL for scanning unless you own the domain or have received explicit written authorization from the owner. This applies without exception, regardless of:

- The nature of the scan (passive-only does not change your legal obligations)
- Your stated purpose (curiosity, research, bug bounty — you must have authorization)
- Whether you believe the target is publicly accessible
- Whether you believe the target is already insecure

3.2 Prohibited Target Categories
Even with claimed authorization, you may not use WebGuard to scan the following categories of systems:

- Government systems and official government websites, at any level (local, national, or international)
- Critical national infrastructure — power grids, water systems, transportation networks, telecommunications infrastructure
- Financial system infrastructure — banking systems, payment processing networks, stock exchange systems
- Healthcare and emergency services — hospital systems, emergency response systems, healthcare provider systems
- Educational institutions — university or school administrative systems without explicit institutional authorization
- Any system whose compromise could pose risk to public safety or national security

This restriction exists because the consequences of unauthorized access — even passive observation — to these systems can be severe and our tool must not contribute to that risk.

3.3 Scanning as Reconnaissance
You may not use WebGuard as part of a workflow that includes, or is intended to lead to, unauthorized access, exploitation, or attack of any system. Specifically prohibited:

- Using WebGuard to identify weaknesses before an attack
- Conducting unauthorized bug bounty hunting (you must be enrolled in the program and comply with its scope)
- Using WebGuard findings to support, enable, or inform an attack on any system

3.4 Circumventing Service Controls
You may not:

- Attempt to bypass, disable, or circumvent rate limiting controls
- Create multiple accounts to exceed per-account rate limits
- Share accounts between multiple users to exceed individual limits
- Automate scan submissions in ways that violate the rate limits defined in the Terms of Service

3.5 Misrepresentation and Fraud
You may not:

- Provide false information about your authorization to scan a target
- Impersonate another person or organization in your account or communications
- Misrepresent WebGuard findings — for example, falsely claiming a site is vulnerable or secure based on manipulated output

3.6 Competitive Intelligence
You may not use WebGuard to systematically gather intelligence about competitors' technical security configurations for competitive purposes. A security consultant scanning a client's site is permitted; systematically mapping a competitor's infrastructure is not.

3.7 Violation of Law
You may not use WebGuard in any way that violates applicable law, including computer access laws, data protection laws, privacy laws, or intellectual property laws in any jurisdiction.

---

4. Understanding Passive Scanning

WebGuard performs passive scanning only. It does not inject payloads, probe for active vulnerabilities, or attempt to exploit anything it finds. We want to be clear about what this means:

Passive scanning observes what a system voluntarily exposes to any visitor making a standard HTTP request. This includes HTTP response headers, TLS configuration, cookies set in response to requests, DNS records, and publicly accessible files.

The passive nature of WebGuard does not change your legal obligations. In most jurisdictions, making HTTP requests to a system you do not have authorization to access — even read-only requests — may constitute unauthorized computer access. The law does not distinguish between active and passive unauthorized access in the way that security professionals often do.

If you are uncertain whether you have authorization to scan a target, do not scan it.

---

5. Bug Bounty Programs

If you wish to use WebGuard as part of a bug bounty submission:

- You must be a registered participant in the bug bounty program
- The target URL must be explicitly within scope as defined by the program
- Your use of WebGuard must comply with the program's testing guidelines
- You may not scan out-of-scope targets even if you believe they are vulnerable

WebGuard findings may provide useful context for a bug bounty report but are not a substitute for the evidence standards required by bug bounty platforms.

---

6. Security Consultants and Professional Use

Security consultants and penetration testers are a valued part of the WebGuard community. Professional use is explicitly permitted within the following framework:

- You have a signed engagement agreement or written authorization from the client before scanning
- The scope of your scanning matches the scope defined in your engagement
- You use WebGuard findings responsibly — providing clients with accurate, contextualized reports
- You make clear to clients that WebGuard is a passive tool and does not replace active penetration testing

WebGuard's PDF reports are designed to be delivered directly to clients as part of a professional engagement. We trust security consultants to use them honestly and in context.

---

7. Reporting Violations

If you believe someone is using WebGuard in violation of this policy — or if you are the owner of a system being scanned without your authorization — please contact us immediately at jamesgichia15@gmail.com.

Please include:

- The URL being scanned (if known)
- Any evidence you have of unauthorized scanning
- Your contact information

We take all reports of policy violations seriously and will investigate promptly. Where evidence of unauthorized scanning is confirmed, we will terminate the responsible account and cooperate with law enforcement where appropriate.

If you believe WebGuard has been used to scan your systems without authorization and you have suffered harm as a result, we encourage you to contact law enforcement in your jurisdiction.

---

8. Consequences of Violations

Violations of this policy may result in:

- Immediate suspension or permanent termination of your account
- Forfeiture of any reports or data generated during the violation
- Reporting of your activity to the relevant law enforcement agencies
- Civil or criminal liability under applicable computer access laws

The severity of the consequence will be proportionate to the nature and impact of the violation. Unauthorized scanning of critical infrastructure will be treated with the highest severity.

---

9. Changes to This Policy

We may update this policy as the Service evolves or as new risks are identified. Material changes will be communicated in accordance with the Terms of Service. The current version is always available in the WebGuard repository.

---

10. Contact

Questions about this policy or reports of violations:

Operator: James Gichia
Email: jamesgichia15@gmail.com
GitHub: https://github.com/jamesgichia

---

This document is version controlled. All changes require a new version entry, a descriptive commit message, and review before merging to the docs branch.
Last updated: May 2026
