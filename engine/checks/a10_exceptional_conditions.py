"""
A10: Mishandling of Exceptional Conditions checks.
"""

from engine.base_check import BaseCheck
from engine.models import CheckResult, Dimension, Effort, ScanTarget, Severity


class A10ExceptionalConditionsCheck(BaseCheck):
    """
    Checks for mishandled exceptions, such as verbose error pages that
    leak internal stack traces to the user.
    """

    owasp_id = "A10"
    owasp_name = "Mishandling of Exceptional Conditions"
    dimension = Dimension.INFORMATION_EXPOSURE.value

    def run(self, target: ScanTarget) -> CheckResult:
        evidence = {}
        passed = True
        severity = Severity.INFO
        title = "Secure Error Handling"
        description = (
            "No obvious passive indicators of mishandled exceptions were found."
        )
        business_impact = (
            "Prevents exposure of sensitive internal system details during errors."
        )
        recommendation = "Maintain generic error messages for end users."
        effort = Effort.LOW

        # Check if status code indicates a server error
        if target.status_code >= 500:
            body_lower = target.response_body_snippet.lower()
            # Look for common stack trace indicators
            if (
                "traceback (most recent call last):" in body_lower
                or "at java." in body_lower
                or "stack trace:" in body_lower
            ):
                passed = False
                severity = Severity.HIGH
                title = "Verbose Error Message"
                description = "The server returned a verbose error message containing a stack trace."
                business_impact = "Stack traces expose internal application logic and pathways to attackers."
                recommendation = "Configure the application to return generic error messages in production."
                evidence["status_code"] = target.status_code
                evidence["stack_trace_detected"] = True

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
                "https://owasp.org/Top10/A10_2021-Server-Side_Request_Forgery_%28SSRF%29/"
            ],
        )
