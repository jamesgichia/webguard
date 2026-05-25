
WebGuard — User Personas
Document: User Personas
Version: 1.0
Status: Draft
Created: May 2026
Author: James Gichia
Repository: docs/project/user-personas.md

Purpose
User personas are fictional but research-grounded profiles of the real people WebGuard is designed to serve. They are built from market research, competitor analysis, and target segment data established in previous documents. Every feature decision, design choice, and communication strategy in this project should be evaluated against these personas.
When in doubt about any product decision, ask: Does this serve Daniel, Sarah, or Amara?

Persona 1 — Daniel Ochieng
The Developer

Name:         Daniel Ochieng
Age:          26
Role:         Backend Developer
Experience:   3 years professional development
Location:     Nairobi, Kenya
Education:    BSc Computer Science
Works at:     Mid-sized fintech startup (45 employees)
Team size:    6 developers, no dedicated security engineer

A Day in Daniel's Life
Daniel arrives at the office at 8:30am. By 9:00am he is in a standup where the team reviews what is shipping this week. Two features are going to production on Friday — a new customer onboarding flow and a payment confirmation endpoint. His team lead mentions compliance casually: "make sure it is secure before it goes out."
Daniel knows what that means in theory. In practice, he has a full sprint of work to complete, two pull requests to review, and a bug reported in production that needs diagnosing before end of day. Security is important but it lives at the end of the to-do list — again.
He has heard of OWASP. He has briefly used ZAP once during a university project but found it confusing and time-consuming to configure. He has never run a formal security check on any code he has shipped professionally. Not because he does not care — because there has never been a tool fast enough, simple enough, and clear enough to fit into his actual workflow.
On Friday the features ship. They are probably fine. Probably.

Goals

Ship secure code without becoming a security expert
Integrate security checks into his development workflow without slowing down delivery
Be able to show his team lead and CTO evidence that security was considered before deployment
Learn about security in context — understanding findings as they relate to real code he has written
Progress his career — security knowledge is increasingly valued and he knows it


Frustrations

Security tools feel built for penetration testers, not developers
ZAP and Nikto require configuration time he does not have
Reports from existing tools are full of jargon his manager cannot read
He does not know what he does not know — no visibility into what his application is exposing
Security always feels like something to do after the real work is done
No tool gives him a simple answer to the question: is this site reasonably secure right now?


How Daniel Uses WebGuard
Daniel adds WebGuard to his CI/CD pipeline. Every pull request targeting the main branch triggers a passive scan. Results arrive as JSON — a clean pass or a list of findings with severities. If a critical finding appears the build fails with a clear message explaining what was found and how to fix it.
Before major deployments he runs the standard profile from his terminal:
bashwebguard scan https://staging.fintechapp.co.ke --profile standard
He gets a scored result in under two minutes. He screenshots the terminal output or downloads the PDF and attaches it to the deployment ticket. His team lead can see it. His CTO can see it. The finding is documented.
When something is flagged he does not need to Google what it means. The remediation card tells him exactly what to add to the HTTP response headers, why it matters in plain language, and how long it will take to fix.

What Makes Daniel Trust WebGuard

Zero false positives in the first two weeks of use
Findings he can verify himself by inspecting the actual HTTP response
Remediation steps that work when he follows them
A tool that respects his time — fast, no configuration, clear output
An open source codebase he can inspect if something seems wrong


Quote

"I do not need a security degree. I need something that tells me what is broken, why it matters, and how to fix it — in the time it takes to make coffee."



Persona 2 — Sarah Wanjiku
The SMB Owner

Name:         Sarah Wanjiku
Age:          38
Role:         Founder and CEO
Experience:   12 years in retail, 4 years running an e-commerce business
Location:     Mombasa, Kenya
Education:    Diploma in Business Management
Works at:     Her own online retail business (12 employees)
Tech profile: Comfortable with business software, not technical

A Day in Sarah's Life
Sarah runs an e-commerce business selling Kenyan-made fashion and homeware. Her website processes customer orders, stores delivery addresses, and handles card payments through a third-party gateway. She has 3,400 registered customers.
She hired a freelance developer two years ago to build the site and has a part-time IT person who handles updates and occasional issues. Neither of them has mentioned security to her in any meaningful way. She assumes the site is secure because it has an SSL padlock and has never been obviously hacked.
Last month she attended a business networking event where another business owner told her their website had been breached — customer email addresses and phone numbers had been stolen and used in a phishing campaign targeting those customers. The business owner spent three months dealing with the aftermath, lost a significant portion of their customer base, and received a formal inquiry from the Office of the Data Protection Commissioner.
Sarah drove home that evening wondering if her website was actually safe. She searched online for ways to check. She found ZAP (too technical), Acunetix (too expensive at $5,000 per year), and Mozilla Observatory (gave her a grade but she did not know what to do with the findings). She closed her laptop without a clear answer.

Goals

Know whether her website is safe for her customers
Protect the personal data her customers have trusted her with
Avoid the regulatory consequences she heard about at that networking event
Have something she can show an auditor or regulatory body as evidence of security diligence
Not have to become technical to do any of this


Frustrations

Security tools assume she knows what a CSP header is
She cannot afford enterprise security consultants
Free tools give her grades and scores but no explanation of what they mean for her business
She does not know how to prioritize findings even when she finds them
Reports she has seen are written for developers, not business owners
There is no affordable option between free tools she cannot understand and expensive tools she cannot afford


How Sarah Uses WebGuard
Sarah signs up for the WebGuard web dashboard free tier. She enters her website URL and selects the standard profile. While the scan runs she makes tea.
The results appear on her dashboard. Her score is 5.8 out of 10. Grade D. The dashboard shows her a simple summary:
"Your website has several security issues that should be addressed. The most important ones relate to how your site communicates with browsers and how customer session data is protected."
She does not understand every finding but she understands the score, the grade, and the priority list. She downloads the PDF report and sends it to her part-time IT person with a message: "Can you fix the ones marked High and Critical please?"
Her IT person opens the report and follows the remediation steps. Two weeks later she runs the scan again. Her score is 8.1. Grade B. She feels genuinely better.
She upgrades to the paid tier and schedules a monthly scan to keep track of changes.

What Makes Sarah Trust WebGuard

She understood the results without needing help
The report looked professional enough to share with her IT person and file for compliance purposes
The price was reasonable — comparable to other business software subscriptions she pays monthly
The score improved after her IT person followed the remediation steps — proof it works
No sales calls, no contracts, no enterprise complexity


Quote

"I do not know what half of these technical things mean. But I know my score went from 5.8 to 8.1 after we fixed the issues. That is something I can understand and something I can show people."



Persona 3 — Amara Diallo
The Security Consultant

Name:         Amara Diallo
Age:          32
Role:         Independent Cybersecurity Consultant
Experience:   7 years in cybersecurity, 3 years freelancing
Location:     Lagos, Nigeria (works with clients across Africa and Europe)
Education:    BSc Information Security, CEH, CompTIA Security+
Works at:     Self-employed — 8 to 12 active clients at any time
Tech profile: Expert-level — comfortable with any tool in the security ecosystem

A Day in Amara's Life
Amara runs a one-person cybersecurity consultancy serving SMBs and mid-market businesses. Her typical engagement begins with a baseline security assessment — a review of what a business's web presence is exposing before she moves into deeper manual testing.
This baseline assessment is billable work but it is also the least exciting part of her job. It involves running a series of checks she has done hundreds of times — headers, TLS, cookies, component versions, DNS records — and compiling the results into a report her clients can understand. It takes her three to four hours per client and produces a document she then has to format manually to look professional.
She currently uses a combination of tools — Mozilla Observatory for headers, SSL Labs for TLS, manual inspection for cookies, and custom scripts she has written over the years for other checks. She stitches the results together in a Word document with her own branding. It works but it is inefficient and she cannot scale her practice without either hiring someone or finding a better tool.
She needs a tool that does the baseline in minutes, produces a professional report she can deliver to clients directly, and frees her time for the more valuable manual and active testing work.

Goals

Complete baseline passive assessments faster without sacrificing quality
Deliver professional reports to clients without manual formatting
Scale her practice to more clients without proportionally more hours
Maintain technical credibility — any tool she recommends must be accurate
Build a reputation for thorough, well-documented assessments


Frustrations

No single tool covers all the passive checks she needs in one place
Stitching results from multiple tools into one report wastes hours per engagement
Existing tools produce technical output not suitable for direct client delivery
False positives from tools like Nikto undermine her credibility with clients
The tools she trusts most (Burp Suite) are active scanners — different use case
No good CLI-first tool produces a PDF report she can hand to a client directly


How Amara Uses WebGuard
Amara uses WebGuard as her baseline assessment tool for every new client engagement. She runs the deep profile against each client's primary domain:
bashwebguard scan https://clientsite.com --profile deep --format pdf --output ./clients/clientname/
The PDF report is produced in under five minutes. She reviews it, adds her own observations and context as annotations, and delivers it to the client as part of the engagement kickoff. The structured findings, OWASP mapping, severity ratings, and remediation guidance mean the report is already 80% of what she would have produced manually.
She then spends her time on what only a human expert can do — manual testing, business logic analysis, and the deeper assessment her clients are paying for.
She has referred WebGuard to three other consultants in her network. She has mentioned it in two blog posts about security assessment workflows. For every consultant she refers who adopts WebGuard, the tool reaches that consultant's entire client base.

What Makes Amara Trust WebGuard

Zero false positives — she verified findings against manual inspection before trusting it
OWASP alignment gives her a credible framework to reference in client conversations
The PDF report looks professional enough to include in a formal deliverable
The CLI interface fits naturally into her existing workflow and scripts
Transparent about what it does and does not check — no overclaiming


Quote

"I have been waiting for a tool that does the boring part of my job well so I can spend more time on the interesting part. Baseline passive assessment should take five minutes and produce a report I can hand to a client. That is not a high bar. Somehow nobody has cleared it until now."



Persona Comparison Summary
AttributeDaniel (Developer)Sarah (SMB Owner)Amara (Consultant)Technical levelIntermediateNon-technicalExpertPrimary interfaceCLIWeb dashboardCLI + WebMost valued featurePipeline integrationPlain English reportsPDF report qualityDecision driverSpeed and accuracyPrice and simplicityAccuracy and time savingAdoption pathDiscovers on GitHub/PyPIReferred by developerDiscovers via security communityBecomes paying customerWhen team adopts itImmediately if it worksOn first client engagementAdvocacy behaviorShares with team, writes about itTells other business ownersRefers other consultants

How To Use These Personas
These personas are living references — not static documents. Refer to them when:

Prioritizing features: Does this feature serve Daniel, Sarah, or Amara? If none of them, it waits.
Writing copy: Does this landing page text make sense to Sarah? Would Daniel read this README?
Designing the report: Would Sarah understand this section without explanation? Would Amara trust this finding?
Making CLI decisions: Would Daniel run this command in a pipeline? Is this flag naming intuitive?
Evaluating scope creep: Which persona asked for this? If none, it goes in the backlog.


This document is version controlled. All changes must be committed with a descriptive message and reviewed before merging.
Last updated: May 2026
