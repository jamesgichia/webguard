"""
A07: Authentication Failures checks.
"""

from engine.base_check import BaseCheck
from engine.models import CheckResult, Dimension, Effort, ScanTarget, Severity


class A07AuthenticationFailuresCheck(BaseCheck):
    """
    Checks for authentication failures, such as insecure cookie configurations
    (missing Secure, HttpOnly, or SameSite attributes).
    """

    owasp_id = "A07"
    owasp_name = "Authentication Failures"
    dimension = Dimension.COOKIE_SECURITY.value

    def run(self, target: ScanTarget) -> CheckResult:
        evidence = {}
        passed = True
        severity = Severity.INFO
        title = "Secure Authentication Indicators"
        description = "Cookies are securely configured."
        business_impact = (
            "Protects user sessions from hijacking and cross-site request forgery."
        )
        recommendation = "Maintain secure cookie attributes."
        effort = Effort.LOW

        insecure_cookies = []
        for cookie in target.cookies:
            issues = []
            if not cookie.get("secure", False):
                issues.append("Missing 'Secure' flag")
            if not cookie.get("httponly", False):
                issues.append("Missing 'HttpOnly' flag")
            
            samesite = cookie.get("samesite")
            if not samesite or samesite.lower() not in ("strict", "lax"):
                issues.append("Weak or missing 'SameSite' attribute")

            if issues:
                insecure_cookies.append(
                    {"name": cookie.get("name", "unknown"), "issues": issues}
                )

        if insecure_cookies:
            passed = False
            severity = Severity.HIGH
            title = "Insecure Cookie Configuration"
            description = (
                f"Found {len(insecure_cookies)} cookie(s) with insecure attributes."
            )
            business_impact = "Session tokens or sensitive cookies can be stolen via XSS or intercepted over cleartext."
            recommendation = "Ensure all cookies use 'Secure', 'HttpOnly', and 'SameSite=Strict' or 'Lax'."
            evidence["insecure_cookies"] = insecure_cookies

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
                "https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/"
            ],
        )
