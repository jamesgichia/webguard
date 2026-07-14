"""
A05: Injection checks.
"""

from engine.base_check import BaseCheck
from engine.models import CheckResult, Dimension, Effort, ScanTarget, Severity


class A05InjectionCheck(BaseCheck):
    """
    Checks for passive indicators that could allow injection attacks,
    such as missing or weak Content-Security-Policy (CSP) headers.
    """

    owasp_id = "A05"
    owasp_name = "Injection"
    dimension = Dimension.HEADER_CONFIGURATION.value

    def run(self, target: ScanTarget) -> CheckResult:
        evidence = {}
        passed = True
        severity = Severity.INFO
        title = "Secure Injection Mitigations"
        description = (
            "No obvious passive indicators of injection vulnerabilities were found."
        )
        business_impact = (
            "Mitigates the risk of Cross-Site Scripting (XSS) and data injection attacks."
        )
        recommendation = (
            "Continue to validate input, encode output, and use strict CSPs."
        )
        effort = Effort.LOW

        headers_lower = {k.lower(): v for k, v in target.response_headers.items()}
        csp = headers_lower.get("content-security-policy", "")

        if not csp:
            passed = False
            severity = Severity.MEDIUM
            title = "Missing Content-Security-Policy (CSP)"
            description = "The server does not enforce a Content-Security-Policy."
            business_impact = (
                "Leaves the application highly vulnerable to XSS and data injection."
            )
            recommendation = "Implement a strict Content-Security-Policy."
            evidence["missing_csp"] = True
        else:
            # Check for weak CSP directives
            weak_directives = ["unsafe-inline", "unsafe-eval"]
            found_weak = [wd for wd in weak_directives if wd in csp]
            if found_weak:
                passed = False
                severity = Severity.MEDIUM
                title = "Weak Content-Security-Policy (CSP)"
                description = (
                    f"The CSP contains weak directives: {', '.join(found_weak)}."
                )
                business_impact = "Weak CSP directives reduce the effectiveness of XSS mitigation."
                recommendation = (
                    "Remove 'unsafe-inline' and 'unsafe-eval' from the CSP."
                )
                evidence["weak_csp_directives"] = found_weak
                evidence["csp"] = csp

        return CheckResult(
            owasp_id=self.owasp_id,
            owasp_name=self.owasp_name,
            dimension=self.dimension,
            passed=passed,
            severity=severity,
            title=title,
            description=description,
            business_impact=business_impact,
            recommendation=recommendation,
            effort=effort,
            evidence=evidence,
            references=["https://owasp.org/Top10/A03_2021-Injection/"],
        )
