WebGuard — Privacy Policy
Document: Privacy Policy
Version: 1.0
Status: Draft
Created: May 2026
Author: James Gichia
Repository: docs/legal/privacy-policy.md

---

This Privacy Policy explains what personal data WebGuard collects, why we collect it, how we use it, how long we keep it, and what rights you have over it. We have written it in plain English because privacy decisions should be informed decisions.

WebGuard ("the Service," "we," "us," or "our") is operated by James Gichia ("the Operator"). This policy applies to the WebGuard web dashboard, the REST API, and any features of the CLI tool that involve data transmission to WebGuard servers.

Note: The WebGuard CLI tool, when used entirely offline or against local environments without connecting to the WebGuard API, does not transmit data to us. This policy applies to interactions with the hosted Service.

---

1. Legal Basis for This Policy

WebGuard operates under multiple data protection frameworks depending on the location of our users:

Kenya Data Protection Act, 2019 (DPA 2019)
The DPA 2019 governs the processing of personal data relating to individuals in Kenya. As a Kenyan-operated service, we comply with the DPA 2019 as our primary data protection framework. This includes obligations relating to lawful processing, data subject rights, security of processing, and data breach notification.

General Data Protection Regulation (GDPR)
If you are located in the European Economic Area (EEA), the UK, or Switzerland, the GDPR applies to our processing of your personal data. Where the GDPR applies, we process your data on the legal bases described in Section 3.

Other Jurisdictions
We respect applicable data protection laws in all jurisdictions where our users are located. If you have questions about data protection in your specific jurisdiction, contact us at jamesgichia15@gmail.com.

---

2. What Data We Collect

2.1 Account Data
When you register for a WebGuard account, we collect:

- Email address — used for authentication, account communication, and password reset
- Display name — used to personalize your dashboard experience
- Password — stored as a bcrypt hash. We never store your plaintext password and cannot retrieve it.
- Account creation date and timestamp
- Last login timestamp

2.2 Scan Data
When you submit a URL for scanning, we collect and store:

- The URL submitted for scanning
- The domain name extracted from that URL
- The scan profile selected (Quick, Standard, or Deep)
- The date and time the scan was submitted
- The scan status (pending, running, completed, failed)
- The complete scan result — all findings, scores, dimension scores, and metadata
- The duration of the scan
- The scan ID (a randomly generated identifier)

We also store the generated reports:
- JSON report
- HTML report
- PDF report

2.3 API Key Data
If you generate API keys, we store:

- A hashed version of the key (the plaintext key is shown only once and never stored)
- The label you assign to the key
- The creation date
- The date the key was last used

We never store the plaintext API key. If you lose an API key, it cannot be recovered — you must generate a new one.

2.4 Usage Data
We collect technical data about your use of the Service:

- IP address at time of login and scan submission
- Browser type and version (for web dashboard users)
- Operating system (for web dashboard users)
- Pages visited and timestamps (for web dashboard users)
- API endpoint requests and response codes
- Error logs (anonymized where possible)

2.5 CLI Tool Data
The WebGuard CLI tool operates locally on your machine. When you use it:

- Without an API key: No data is transmitted to WebGuard servers. All processing is local.
- With an API key (for submitting scans via the API): The URL, profile, and scan results are transmitted to and stored on WebGuard servers, subject to this policy.

2.6 What We Do Not Collect

- We do not collect payment card information. If billing is introduced in a future version, payments will be processed by a third-party payment provider and we will not store card numbers.
- We do not collect data from the websites you scan beyond what the scanning engine observes during the scan itself.
- We do not use cookies beyond those strictly necessary for authentication session management.
- We do not use tracking pixels, advertising cookies, or third-party analytics that track you across the web.

---

3. Why We Collect This Data and Our Legal Basis

3.1 Account Data
Purpose: To create and manage your account, authenticate you, and allow you to recover access to your account.
Legal basis (GDPR): Performance of contract — we need this data to provide the Service you signed up for.
Legal basis (Kenya DPA): Legitimate purpose — necessary for the provision of the Service.

3.2 Scan Data
Purpose: To perform the security scan you requested, generate reports, maintain your scan history, and power the dashboard statistics.
Legal basis (GDPR): Performance of contract — you submitted a scan and we need to store the results to show you.
Legal basis (Kenya DPA): Legitimate purpose — storage of results is necessary to fulfil the service.
Retention: Scan results are retained for 12 months from the date of the scan, or until you delete them, whichever comes first. On account deletion, all scan data is permanently removed.

3.3 Usage Data
Purpose: To maintain the security and performance of the Service, diagnose errors, detect abuse, and enforce rate limiting.
Legal basis (GDPR): Legitimate interests — we have a legitimate interest in keeping the Service secure and operational.
Legal basis (Kenya DPA): Legitimate purpose — security and operational integrity.
Retention: Usage logs are retained for 90 days.

3.4 API Key Data
Purpose: To authenticate API requests and allow you to manage and revoke your keys.
Legal basis (GDPR): Performance of contract.
Legal basis (Kenya DPA): Legitimate purpose.

---

4. Scan Data — A Special Note

The URLs you submit to WebGuard may reveal information about your projects, clients, or business. We treat scan data with particular care:

- We do not analyze your scan targets for our own business purposes
- We do not share your scan targets with any third party
- We do not use your scan data to train machine learning models
- Security consultants who scan client websites: the client URL and findings are stored in your account and are accessible only to you

The findings generated by a scan describe the publicly observable security posture of the URL you submitted at the time of the scan. This information was already publicly observable by anyone who looked — WebGuard makes it structured and visible to you.

---

5. How We Share Your Data

We do not sell, rent, or trade your personal data. We do not share your data with advertising networks. We share data only in the following limited circumstances:

5.1 Service Providers
We may share data with third-party providers who help us operate the Service, including:

- Cloud infrastructure providers (hosting and database)
- Error monitoring services (Sentry — for capturing application errors)

These providers act as data processors on our behalf. They process data only according to our instructions and are bound by data processing agreements. They do not use your data for their own purposes.

5.2 Legal Requirements
We may disclose your data if required to do so by:

- A court order or other legal process with jurisdiction over us
- A lawful request from a law enforcement agency
- A regulatory requirement under Kenyan law or applicable international law

We will notify you of any such request unless we are legally prohibited from doing so.

5.3 Protection of Rights
We may disclose data where necessary to detect, investigate, or prevent illegal activity, fraud, or violations of our Terms of Service — including unauthorized scanning.

5.4 Business Transfers
If WebGuard is acquired, merged, or its assets are transferred, your data may be transferred to the acquiring entity. We will notify registered users before any such transfer and the acquiring entity will be bound by this Privacy Policy or a materially equivalent one.

---

6. Data Security

We take the security of your data seriously, including because we understand the sensitivity of security-related data.

Measures we implement:

- Passwords stored using bcrypt with a minimum of 12 rounds — plaintext passwords never stored
- All data transmitted over HTTPS — no plaintext HTTP in production
- JWT access tokens with 15-minute expiry
- Refresh tokens with 7-day expiry, invalidated on logout
- API rate limiting to limit exposure in the event of credential compromise
- Database access restricted to application services — no public database exposure
- Sentry error monitoring to detect unusual application behavior
- Dependencies pinned to exact versions and monitored for vulnerabilities via GitHub Dependabot
- Docker containers run as non-root users

We conduct security testing on WebGuard itself. We run WebGuard's own scanning engine against the WebGuard domain as part of pre-launch verification.

No security measure is perfect. In the event of a data breach that affects your personal data, we will notify you in accordance with our obligations under the Kenya DPA 2019 and, where applicable, the GDPR.

---

7. Your Rights

7.1 Under the Kenya Data Protection Act 2019
As a data subject under the Kenya DPA, you have the right to:

- Be informed about the processing of your personal data (this policy fulfils that obligation)
- Access your personal data — you may request a copy of all data we hold about you
- Correct inaccurate personal data
- Delete your personal data — you may delete your account and all associated data from the Settings page
- Object to processing of your personal data
- Restrict processing of your personal data in certain circumstances
- Data portability — you may export your scan history as JSON at any time

7.2 Under the GDPR (EEA Users)
If you are located in the EEA, UK, or Switzerland, you have the same rights listed above, plus:

- The right not to be subject to solely automated decision-making with legal or similarly significant effects (WebGuard does not make such decisions)
- The right to lodge a complaint with your national data protection supervisory authority

7.3 How to Exercise Your Rights
To exercise any of your rights, contact us at jamesgichia15@gmail.com. We will respond within 30 days. We will not charge a fee for reasonable requests.

For account deletion and data export, these functions are available directly in the Settings page of the web dashboard without needing to contact us.

---

8. Cookies

WebGuard uses cookies only for the following purposes:

- Authentication session management — to keep you logged in between page loads
- CSRF protection — to prevent cross-site request forgery attacks

We do not use cookies for advertising, tracking, or analytics. We do not use third-party cookies.

If you block all cookies, the web dashboard will not function correctly because it requires session cookies to authenticate you.

---

9. International Data Transfers

WebGuard is operated from Kenya. If you access the Service from outside Kenya, your data will be transferred to and processed in Kenya (or the location of our cloud infrastructure provider).

For EEA users: transfers of your data outside the EEA will be made in accordance with GDPR requirements, including through appropriate safeguards such as Standard Contractual Clauses where required.

---

10. Children's Privacy

WebGuard is not intended for use by anyone under the age of 18. We do not knowingly collect personal data from children. If you believe a child has created an account, contact us at jamesgichia15@gmail.com and we will delete the account promptly.

---

11. Data Retention Summary

| Data Type | Retention Period |
|---|---|
| Account data | Until account deletion |
| Scan results and reports | 12 months, or until deleted |
| Usage and access logs | 90 days |
| API key records (hashed) | Until key is revoked or account deleted |
| Error logs (Sentry) | 90 days |

---

12. Changes to This Policy

When we make material changes to this Privacy Policy, we will:

- Update the version number and effective date
- Notify registered users by email at least 14 days before the changes take effect
- Maintain the previous version in the repository commit history

Continued use of the Service after the effective date constitutes acceptance of the updated policy.

---

13. Contact and Complaints

For privacy questions, data access requests, or complaints:

Operator: James Gichia
Email: jamesgichia15@gmail.com
GitHub: https://github.com/jamesgichia

If you are located in Kenya and wish to lodge a formal complaint, you may contact the Office of the Data Protection Commissioner:
Website: www.odpc.go.ke

If you are located in the EU/EEA and wish to lodge a formal complaint, contact your national data protection supervisory authority.

---

> [!NOTE]
> Legal Review Flag: The data retention periods (Section 11), the international transfer safeguards for EEA users (Section 9), and the data breach notification procedures should be reviewed by a qualified Kenyan lawyer before the Service goes live. The Kenya DPA 2019 has specific breach notification timelines (72 hours to the ODPC) that should be reflected in internal procedures even if not explicitly detailed in this public-facing document.

---

This document is version controlled. All changes require a new version entry, a descriptive commit message, and review before merging to the docs branch.
Last updated: May 2026
