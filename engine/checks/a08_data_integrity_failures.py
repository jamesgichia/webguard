"""
A08: Software and Data Integrity Failures checks.
"""

from engine.base_check import BaseCheck
from engine.models import CheckResult, Dimension, Effort, ScanTarget, Severity


class A08DataIntegrityFailuresCheck(BaseCheck):
    """
    Checks for indicators of data integrity failures, such as CSP lacking
    strict integrity directives.
    """

    owasp_id = "A08"
    owasp_name = "Software and Data Integrity Failures"
    dimension = Dimension.HEADER_CONFIGURATION.value

    def run(self, target: ScanTarget) -> CheckResult:
        evidence = {}
        passed = True
        severity = Severity.INFO
        title = "Data Integrity Controls"
        description = (
            "No obvious passive indicators of data integrity failures were found."
        )
        business_impact = "Ensures code and data are not tampered with."
        recommendation = "Use Subresource Integrity (SRI) and secure update mechanisms."
        effort = Effort.LOW

        headers_lower = {k.lower(): v for k, v in target.response_headers.items()}
        csp = headers_lower.get("content-security-policy", "")

        if csp:
            if "require-sri-for" not in csp and "strict-dynamic" not in csp:
                passed = False
                severity = Severity.LOW
                title = "CSP Lacks Integrity Directives"
                description = "The Content-Security-Policy does not enforce strict integrity checks."
                business_impact = "Without strict CSP, malicious scripts can more easily be executed if injected."
                recommendation = (
                    "Consider utilizing strict CSP directives for scripts and styles."
                )
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
            references=[
                "https://owasp.org/Top10/A08_2021-Software_and_Data_Integrity_Failures/"
            ],
        )
