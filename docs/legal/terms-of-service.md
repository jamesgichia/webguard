WebGuard — Terms of Service
Document: Terms of Service
Version: 1.0
Status: Draft
Created: May 2026
Author: James Gichia
Repository: docs/legal/terms-of-service.md

---

Please read these Terms of Service carefully before using WebGuard. By creating an account, submitting a scan, installing the CLI tool, or accessing the API, you agree to be bound by these terms. If you do not agree, do not use WebGuard.

---

1. About WebGuard

WebGuard ("the Service," "we," "us," or "our") is a passive web security scanning tool operated by James Gichia ("the Operator"). WebGuard analyzes publicly accessible HTTP and HTTPS endpoints by observing what those endpoints voluntarily expose — including HTTP response headers, TLS/SSL configuration, cookies, DNS records, component versions, and server metadata — and produces structured security reports based on those observations.

WebGuard is available through three interfaces:

- The web dashboard at the WebGuard website
- The CLI tool published on PyPI as the webguard package
- The REST API accessible at /api/v1/

These Terms of Service apply to all three interfaces and all use of the Service in any form.

---

2. Who May Use WebGuard

2.1 Eligibility
You may use WebGuard if:

- You are at least 18 years old, or the age of majority in your jurisdiction
- You have the legal capacity to enter into a binding agreement
- Your use complies with all applicable laws in your country of residence and the country in which you are using the Service

2.2 Account Registration
To access the web dashboard and API, you must create an account. When registering, you must:

- Provide a valid email address that you own or control
- Choose a password that meets the minimum security requirements
- Provide accurate information — you may not impersonate another person or organization

You are responsible for maintaining the confidentiality of your account credentials. You are responsible for all activity that occurs under your account. Notify us immediately at jamesgichia15@gmail.com if you believe your account has been compromised.

2.3 API Keys
You may generate API keys for use in CI/CD pipelines and automated workflows. API keys grant the same permissions as your account. You are responsible for securing your API keys. Do not commit API keys to version control systems. Revoke any key you believe may have been exposed.

---

3. Authorization to Scan — Your Most Important Obligation

3.1 The Authorization Requirement
WebGuard is a tool for analyzing web security. Using it on systems you do not own or have explicit permission to scan is illegal under computer access laws in most jurisdictions, including:

- The Computer Misuse and Cybercrimes Act 2018 (Kenya)
- The Computer Fraud and Abuse Act (United States)
- The Computer Misuse Act 1990 (United Kingdom)
- Directive 2013/40/EU on attacks against information systems (European Union)

By submitting any URL for scanning, you represent and warrant that:

- You are the owner of the domain or web application at that URL, OR
- You have received explicit written authorization from the owner to conduct security scanning, OR
- The URL belongs to a system you are legally authorized to test (such as your employer's system, or a test environment you operate)

3.2 No Exceptions
This requirement has no exceptions. The fact that WebGuard performs only passive scanning does not change your legal obligations as the person initiating the scan. Unauthorized scanning — even passive, read-only observation — may constitute unauthorized computer access in your jurisdiction.

3.3 Your Indemnity
You agree to indemnify and hold harmless WebGuard, the Operator, and any associated parties from any claims, losses, liabilities, damages, or expenses (including legal fees) arising from your use of the Service on systems you did not have authorization to scan.

---

4. Acceptable Use

Your use of WebGuard is governed by the Acceptable Use Policy, which is incorporated into these Terms by reference. The Acceptable Use Policy defines permitted uses, prohibited targets, and the consequences of violations. Please read it in full.

In summary, you may not use WebGuard to:

- Scan any system you do not own or have explicit authorization to scan
- Scan government systems, critical national infrastructure, financial systems, healthcare systems, or emergency services
- Conduct reconnaissance in preparation for an attack
- Attempt to circumvent rate limiting, authentication, or other security controls
- Use the Service in any way that violates applicable law

---

5. What WebGuard Does and Does Not Do

5.1 Passive Scanning Only
WebGuard performs passive observation only. It does not:

- Inject SQL, JavaScript, HTML, or any other payloads into target systems
- Attempt to exploit vulnerabilities it discovers
- Authenticate to target systems using credentials
- Crawl beyond the primary endpoint submitted
- Perform brute-force path enumeration (it checks a maximum of 10 specific passive indicator paths)
- Scan internal network addresses, private IP ranges, localhost, or cloud metadata endpoints (these are blocked by design)

5.2 No Guarantee of Completeness
WebGuard's findings represent what is observable passively. A clean scan result does not mean the target system is fully secure. WebGuard does not replace professional penetration testing, manual code review, or comprehensive security audits. We make no representation that WebGuard will detect all vulnerabilities in any system.

5.3 Accuracy
We design WebGuard to minimize false positives. However, we do not warrant that every finding is accurate in every case. Security configurations change, network conditions vary, and edge cases exist. You are responsible for verifying findings before acting on them.

---

6. The Service

6.1 Availability
We aim to make WebGuard available continuously but do not guarantee uninterrupted access. The Service may be unavailable for maintenance, updates, or reasons outside our control. We target 99.5% monthly availability for the web dashboard and API.

6.2 Rate Limiting
The Service enforces rate limits to ensure fair access and prevent abuse:

- Scan submissions: 10 per hour per user account
- Authentication attempts: 10 per 15-minute window per IP address

These limits may change. We will provide notice of material changes to registered users.

6.3 Scan Queue
Scans are processed asynchronously via a background task queue. Submission of a scan does not guarantee an immediate start time. During periods of high demand, scans may be queued before processing begins.

6.4 Data Retention
We retain scan results and reports for a period defined in the Privacy Policy. You may delete your scan history from the dashboard at any time. On account deletion, all associated scan data is permanently removed.

---

7. Intellectual Property

7.1 The WebGuard Codebase
The WebGuard CLI tool is open source software published under the MIT License. The terms of that license govern your use of the codebase. The MIT License permits you to use, copy, modify, merge, publish, distribute, sublicense, and sell copies of the software, subject to inclusion of the original copyright notice and permission notice.

7.2 The Web Service
The WebGuard web dashboard and API service — including the user interface, branding, and the hosted infrastructure — are not covered by the MIT License. All rights to the service, branding, and non-open-source components are reserved by the Operator.

7.3 Your Data
You retain ownership of all data you submit to WebGuard, including URLs you scan, reports you generate, and any content associated with your account. By using the Service, you grant WebGuard a limited, non-exclusive license to store, process, and display that data for the purpose of delivering the Service to you.

We do not claim ownership of your scan results. We do not sell your scan data to third parties.

---

8. Disclaimers and Limitation of Liability

8.1 No Security Warranty
WebGuard is provided "as is" and "as available." We do not warrant that the Service will meet your specific security requirements, that all vulnerabilities in your system will be detected, or that findings are free from error. Security is complex and no automated tool provides complete coverage.

8.2 No Compliance Certification
WebGuard findings may be relevant to regulatory frameworks including GDPR, PCI-DSS 4.0, and the Kenya Data Protection Act. However, WebGuard does not certify compliance with any regulatory framework. A positive scan result is not a certification that your system complies with any law or standard.

8.3 Limitation of Liability
To the maximum extent permitted by applicable law, WebGuard and the Operator shall not be liable for:

- Any indirect, incidental, special, or consequential damages
- Loss of data, revenue, profits, or business
- Damages arising from your reliance on scan results
- Damages arising from unauthorized use of the Service by you or any third party accessing your account

Our total liability to you for any claim arising from your use of the Service shall not exceed the amount you have paid to us in the three months preceding the claim, or USD 100, whichever is greater.

Nothing in these Terms limits our liability for death or personal injury caused by negligence, fraud, or any liability that cannot be excluded by law.

---

9. Termination

9.1 By You
You may terminate your account at any time by using the account deletion function in the Settings page. On termination, your account and all associated scan data will be permanently deleted within 30 days.

9.2 By WebGuard
We may suspend or terminate your account immediately, without prior notice, if:

- You violate the authorization requirement in Section 3
- You violate the Acceptable Use Policy
- Your use of the Service poses a legal, security, or reputational risk to WebGuard or third parties
- You provide false information during registration
- Required by law or court order

We will provide notice of termination where legally required and practically feasible.

9.3 Effect of Termination
On termination, your right to use the Service ends immediately. Sections 3 (Authorization), 7 (Intellectual Property), 8 (Disclaimers), and 10 (Governing Law) survive termination.

---

10. Governing Law and Dispute Resolution

10.1 Governing Law
These Terms are governed by the laws of the Republic of Kenya, without regard to conflict of law principles.

10.2 Jurisdiction
You agree that any dispute arising from these Terms or your use of the Service shall be subject to the exclusive jurisdiction of the courts of Kenya.

10.3 Good Faith Resolution
Before initiating any formal legal proceeding, both parties agree to attempt to resolve any dispute in good faith by direct communication. Contact us at jamesgichia15@gmail.com with a description of the dispute. We will respond within 14 days.

---

11. Changes to These Terms

We may update these Terms from time to time. When we make material changes, we will:

- Update the version number and effective date at the top of this document
- Notify registered users by email at least 14 days before the changes take effect
- Maintain the previous version in the repository commit history

Continued use of the Service after the effective date of changes constitutes acceptance of the updated Terms.

---

12. Contact

For questions about these Terms, to report a violation, or to notify us of a security concern:

Operator: James Gichia
Email: jamesgichia15@gmail.com
GitHub: https://github.com/jamesgichia
Security issues: See the Responsible Disclosure Policy

---

> [!NOTE]
> Legal Review Flag: The jurisdiction clause (Section 10), the limitation of liability amounts (Section 8.3), and the indemnification clause (Section 3.3) should be reviewed by a qualified Kenyan lawyer before the Service goes live. The substantive positions are sound but the specific legal language may need refinement for enforceability under Kenyan law.

---

This document is version controlled. All changes require a new version entry, a descriptive commit message, and review before merging to the docs branch.
Last updated: May 2026
