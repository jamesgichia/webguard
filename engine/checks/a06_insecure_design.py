"""
A06: Insecure Design checks.
"""

from engine.base_check import BaseCheck
from engine.models import CheckResult, Dimension, Effort, ScanTarget, Severity


class A06InsecureDesignCheck(BaseCheck):
    """
    Checks for insecure design patterns, such as missing cache control
    for potentially sensitive information.
    """

    owasp_id = "A06"
    owasp_name = "Insecure Design"
    dimension = Dimension.HEADER_CONFIGURATION.value

    def run(self, target: ScanTarget) -> CheckResult:
        evidence = {}
        passed = True
        severity = Severity.INFO
        title = "Secure Design Patterns"
        description = "No obvious passive indicators of insecure design were found."
        business_impact = "Reduces the likelihood of architectural flaws being exploited."
        recommendation = "Continue using secure-by-default design patterns."
        effort = Effort.LOW

        headers_lower = {k.lower(): v for k, v in target.response_headers.items()}

        # Check Cache-Control headers
        cache_control = headers_lower.get("cache-control", "")
        if not cache_control or "no-store" not in cache_control:
            passed = False
            severity = Severity.LOW
            title = "Insecure Cache Control"
            description = "The server does not prevent caching of potentially sensitive information."
            business_impact = (
                "Sensitive data may be stored in browser caches or intermediate proxies."
            )
            recommendation = (
                "Implement 'Cache-Control: no-store, max-age=0' for sensitive routes."
            )
            evidence["cache-control"] = cache_control

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
            references=["https://owasp.org/Top10/A04_2021-Insecure_Design/"],
        )
