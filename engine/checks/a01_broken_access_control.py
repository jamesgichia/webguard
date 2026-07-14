"""
A01: Broken Access Control checks.
"""

from engine.base_check import BaseCheck
from engine.models import CheckResult, Dimension, Effort, ScanTarget, Severity


class A01BrokenAccessControlCheck(BaseCheck):
    """
    Checks for broken access control indicators, such as overly permissive CORS
    and directory listing enabled on the server.
    """

    owasp_id = "A01"
    owasp_name = "Broken Access Control"
    dimension = Dimension.HEADER_CONFIGURATION.value

    def run(self, target: ScanTarget) -> CheckResult:
        evidence = {}
        passed = True
        severity = Severity.INFO
        title = "Secure Access Control"
        description = "No obvious passive indicators of broken access control were found."
        business_impact = "Ensures data is only accessible to authorized users."
        recommendation = "Continue to enforce strict access controls and validate permissions."
        effort = Effort.LOW

        # 1. Check for Directory Listing
        body_lower = target.response_body_snippet.lower()
        if "<title>index of /" in body_lower or "<h1>index of /" in body_lower:
            passed = False
            severity = Severity.HIGH
            title = "Directory Listing Enabled"
            description = "The server appears to have directory listing enabled."
            business_impact = "Attackers can map the site structure and access sensitive files."
            recommendation = "Disable directory listing in the web server configuration."
            evidence["directory_listing"] = True

        # 2. Check for Overly Permissive CORS
        headers_lower = {k.lower(): v for k, v in target.response_headers.items()}
        cors_origin = headers_lower.get("access-control-allow-origin")

        if cors_origin == "*":
            if not passed:
                title = "Multiple Access Control Issues"
                description += " Additionally, overly permissive CORS is configured."
            else:
                passed = False
                severity = Severity.HIGH
                title = "Overly Permissive CORS"
                description = "The server returns an Access-Control-Allow-Origin header set to '*'."
                business_impact = (
                    "Any website can read data from this API/site, leading to data leaks."
                )
                recommendation = (
                    "Set Access-Control-Allow-Origin to specific trusted domains."
                )

            evidence["access-control-allow-origin"] = "*"

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
            references=["https://owasp.org/Top10/A01_2021-Broken_Access_Control/"],
        )
