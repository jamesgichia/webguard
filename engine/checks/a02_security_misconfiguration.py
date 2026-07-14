"""
A02: Security Misconfiguration checks.
"""

from engine.base_check import BaseCheck
from engine.models import CheckResult, Dimension, Effort, ScanTarget, Severity


class A02SecurityMisconfigurationCheck(BaseCheck):
    """
    Checks for security misconfigurations, such as missing security headers
    and verbose error pages revealing server details.
    """

    owasp_id = "A02"
    owasp_name = "Security Misconfiguration"
    dimension = Dimension.HEADER_CONFIGURATION.value

    def run(self, target: ScanTarget) -> CheckResult:
        evidence = {}
        passed = True
        severity = Severity.INFO
        title = "Secure Configuration"
        description = (
            "No obvious passive indicators of security misconfiguration were found."
        )
        business_impact = (
            "Reduces the attack surface and mitigates potential exploitation."
        )
        recommendation = "Continue to follow secure deployment and configuration practices."
        effort = Effort.LOW

        headers_lower = {k.lower(): v for k, v in target.response_headers.items()}

        # 1. Missing Security Headers
        missing_headers = []
        expected_headers = [
            "x-content-type-options",
            "x-frame-options",
            "content-security-policy",
        ]
        for h in expected_headers:
            if h not in headers_lower:
                missing_headers.append(h)

        if missing_headers:
            passed = False
            severity = Severity.MEDIUM
            title = "Missing Security Headers"
            description = f"The server is missing important security headers: {', '.join(missing_headers)}."
            business_impact = (
                "Leaves the application vulnerable to clickjacking, XSS, and MIME-sniffing."
            )
            recommendation = "Implement X-Content-Type-Options, X-Frame-Options, and Content-Security-Policy headers."
            evidence["missing_headers"] = missing_headers

        # 2. Verbose Server Headers
        server_header = headers_lower.get("server", "")
        x_powered_by = headers_lower.get("x-powered-by", "")

        verbose_headers_found = {}
        if server_header and any(c.isdigit() for c in server_header):
            verbose_headers_found["server"] = server_header
        if x_powered_by:
            verbose_headers_found["x-powered-by"] = x_powered_by

        if verbose_headers_found:
            passed = False
            if severity == Severity.INFO:
                severity = Severity.LOW
                title = "Verbose Server Headers"
                description = "The server exposes version information in headers."
                business_impact = "Attackers can identify the exact software versions to target known vulnerabilities."
                recommendation = "Remove or obscure the Server and X-Powered-By headers."
            else:
                title = "Multiple Security Misconfigurations"
                description += (
                    " Additionally, the server exposes version information in headers."
                )
            evidence["verbose_headers"] = verbose_headers_found

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
            references=[],
        )
