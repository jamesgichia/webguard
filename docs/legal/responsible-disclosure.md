WebGuard — Responsible Disclosure Policy
Document: Responsible Disclosure Policy
Version: 1.0
Status: Draft
Created: May 2026
Author: James Gichia
Repository: docs/legal/responsible-disclosure.md

---

WebGuard is a security tool. We are committed to keeping it secure. If you have discovered a vulnerability in WebGuard — in the web dashboard, the API, the CLI tool, or any other component — we want to hear from you.

This policy explains how to report vulnerabilities to us, what to expect when you do, and what protections apply to researchers who act in good faith.

---

1. Our Commitment to Security Researchers

Security research is valuable. Finding and reporting vulnerabilities in security tools — especially a tool whose purpose is to find them in other software — is important and we take it seriously.

If you discover a genuine vulnerability in WebGuard and report it to us responsibly, we commit to:

- Acknowledge your report within 48 hours of receipt
- Confirm whether the reported vulnerability is valid within 7 days
- Work to resolve confirmed vulnerabilities as quickly as practicable, with priority given to severity
- Keep you informed of progress toward resolution
- Credit you publicly for your discovery, if you wish to be credited
- Not pursue legal action against you for responsible disclosure conducted in accordance with this policy

---

2. Safe Harbor

We will not initiate legal action against you for security research conducted in good faith and in accordance with this policy. Specifically, to the extent that your research activities are consistent with this policy, we regard them as authorized under the Computer Misuse and Cybercrimes Act 2018 and we will not refer you to law enforcement.

Good faith means:

- You report the vulnerability to us before disclosing it publicly
- You do not access, modify, or delete data beyond what is necessary to demonstrate the vulnerability
- You do not exploit the vulnerability beyond what is necessary to confirm its existence
- You do not perform social engineering, phishing, or physical attacks against WebGuard staff or infrastructure
- You give us reasonable time to address the vulnerability before any public disclosure

If you conduct research outside the bounds of this policy, we cannot extend the safe harbor protections described here.

---

3. Scope

The following are in scope for responsible disclosure:

3.1 In Scope

- The WebGuard web dashboard and all its features
- The WebGuard REST API (api.webguard.dev or equivalent)
- The WebGuard CLI tool (the webguard Python package on PyPI)
- Authentication and session management
- Authorization controls — can one user access another user's scan data?
- API key management
- Rate limiting bypass
- Injection vulnerabilities in any WebGuard interface
- Server-side request forgery (SSRF) — particularly important given that WebGuard makes HTTP requests to URLs submitted by users
- The scan engine's private IP blocking — can it be bypassed to force scans of internal systems?
- Report generation — can malicious content in a scan result be injected into a PDF or HTML report?
- The WebGuard domain and subdomains

3.2 Out of Scope

The following are explicitly out of scope. Reports on these topics will not be eligible for credit and may not receive a response:

- Vulnerabilities in third-party tools or libraries that are not within our control to fix (please report these upstream)
- Denial of service attacks — please do not attempt to take down the Service
- Social engineering of WebGuard staff or users
- Physical security
- Clickjacking on pages with no sensitive actions
- Missing security headers on static landing pages (ironic as this would be, given the nature of the product — but headers-only findings on static pages are informational)
- Self-XSS that requires the attacker to inject content into their own account
- Rate limiting findings that do not represent a meaningful security risk beyond inconvenience
- SSL/TLS configuration issues on third-party services we do not control
- Theoretical vulnerabilities with no demonstrated impact

---

4. Vulnerability Severity Categories

We use the following severity framework for triage and prioritization:

Critical — Immediate Priority (target: 24 hours to initial mitigation)
Examples:
- Authentication bypass — accessing accounts without credentials
- SSRF allowing scan engine to reach internal network addresses or cloud metadata endpoints
- SQL injection with data exfiltration capability
- Accessing another user's scan data without authorization
- Remote code execution on any WebGuard component

High — Priority (target: 7 days to resolution)
Examples:
- Cross-site scripting (XSS) with meaningful impact
- Broken access control on API endpoints
- JWT token validation bypass
- API key exposure in server responses
- Significant rate limiting bypass enabling abuse at scale

Medium — Standard Priority (target: 30 days to resolution)
Examples:
- Information disclosure of non-critical internal details
- CSRF on non-critical actions
- Stored XSS with limited impact
- Insecure direct object reference with limited data exposure

Low — Next Release (target: 90 days to resolution)
Examples:
- Minor information disclosure
- Missing security headers on WebGuard's own interfaces
- Non-exploitable misconfigurations

---

5. How to Report

Send your report to:

Email: jamesgichia15@gmail.com
Subject line: [SECURITY] Brief description of the vulnerability

Please include in your report:

5.1 Required Information
- A description of the vulnerability — what it is, where it exists, and why it is a security concern
- Steps to reproduce — clear, step-by-step instructions that allow us to reproduce the issue
- The impact — what an attacker could achieve by exploiting this vulnerability
- Your assessment of severity — Critical, High, Medium, or Low, with your reasoning

5.2 Helpful Additions (not required but appreciated)
- Proof of concept — code, screenshots, or a video demonstrating the vulnerability
- Your suggested fix, if you have one
- Whether you wish to be credited publicly when we resolve the issue
- Your preferred contact method for follow-up

5.3 Encryption
If your report contains particularly sensitive details — for example, working exploit code or credentials — please indicate this in your email and we will arrange a secure channel for the full disclosure.

---

6. What Happens After You Report

Day 1–2: Acknowledgement
We will acknowledge receipt of your report within 48 hours. If you have not received an acknowledgement within 48 hours, please follow up to ensure your report reached us.

Day 1–7: Triage
We will investigate the report and determine whether it is a valid vulnerability. We will notify you of our determination. If we need additional information to reproduce the issue, we will ask.

After Confirmation: Remediation
For confirmed vulnerabilities, we will work to resolve the issue. We will keep you informed of progress. Timelines depend on severity as described in Section 4.

After Resolution: Disclosure
We prefer coordinated disclosure. We will notify you when the fix has been deployed and ask that you delay any public disclosure until that point. We will credit you in the fix notes and any public disclosure, if you wish.

We aim to be transparent. If we believe a vulnerability is not valid, we will explain our reasoning. If we disagree on severity, we will discuss it. We treat security researchers as partners.

---

7. What We Ask You Not to Do

Please do not:

- Access, copy, modify, or delete data belonging to other users — if you need to demonstrate a data access vulnerability, use two accounts you control
- Disrupt the Service for other users
- Submit automated scanning tools against WebGuard's infrastructure at a rate that causes degradation
- Publicly disclose a vulnerability before we have had reasonable time to address it
- Extort or demand payment for disclosure
- Use the vulnerability for any purpose beyond demonstrating the security issue to us

---

8. A Note on Scanning WebGuard with WebGuard

Using the WebGuard CLI tool or web dashboard to scan WebGuard's own domain (if and when deployed) is explicitly permitted and encouraged. In fact, we run WebGuard against our own domain as part of our pre-launch verification process.

This is a form of passive security assessment of a publicly accessible endpoint, and the scan data belongs to your account. It does not constitute security research requiring disclosure unless you discover a vulnerability through means other than the scan results.

---

9. Public Acknowledgements

We maintain a record of researchers who have responsibly disclosed vulnerabilities and given permission to be credited. We will publish this list on the WebGuard repository as the Service matures.

If you would like to be credited publicly for a valid report, please indicate this in your initial report along with the name or handle you would like us to use.

---

10. Contact

Security reports: jamesgichia15@gmail.com
GitHub: https://github.com/jamesgichia
Operator: James Gichia

This policy is inspired by best practices from the security community, including the disclose.io framework and HackerOne's responsible disclosure guidelines.

---

> [!NOTE]
> Implementation Note: When the WebGuard web dashboard goes live, a link to this document should appear in the footer on every page and in the README. A security.txt file at /.well-known/security.txt should be deployed on the WebGuard domain pointing to this policy, the contact email, and a PGP key if one is established. Interestingly, WebGuard's own Sensitive File Exposure check (FR-010) checks for the presence of security.txt — we should obviously pass our own check.

---

This document is version controlled. All changes require a new version entry, a descriptive commit message, and review before merging to the docs branch.
Last updated: May 2026
