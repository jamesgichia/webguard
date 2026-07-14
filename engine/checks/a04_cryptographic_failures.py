"""
A04: Cryptographic Failures checks.
"""

import re

from engine.base_check import BaseCheck
from engine.models import CheckResult, Dimension, Effort, ScanTarget, Severity


class A04CryptographicFailuresCheck(BaseCheck):
    """
    Checks for cryptographic failures such as weak TLS versions, missing HSTS,
    invalid certificates, and mixed content.
    """

    owasp_id = "A04"
    owasp_name = "Cryptographic Failures"
    dimension = Dimension.TRANSPORT_SECURITY.value

    def run(self, target: ScanTarget) -> CheckResult:
        evidence = {}
        passed = True
        severity = Severity.INFO
        title = "Secure Transport Configuration"
        description = "No passive indicators of cryptographic failures were found."
        business_impact = (
            "Protects sensitive data in transit from interception and tampering."
        )
        recommendation = "Continue to enforce strong encryption and HSTS."
        effort = Effort.LOW

        headers_lower = {k.lower(): v for k, v in target.response_headers.items()}

        issues = []

        # 1. Check TLS info if provided
        if target.url.startswith("https://"):
            if target.tls_info:
                if not target.tls_info.certificate_is_valid:
                    issues.append("Invalid SSL/TLS Certificate.")
                    evidence["certificate_valid"] = False
                    passed = False

                # Check for weak TLS versions
                weak_versions = ["TLSv1.0", "TLSv1.1", "SSLv2", "SSLv3"]
                if target.tls_info.version in weak_versions:
                    issues.append(
                        f"Weak protocol version used: {target.tls_info.version}."
                    )
                    evidence["tls_version"] = target.tls_info.version
                    passed = False

            # 2. Check HSTS
            hsts = headers_lower.get("strict-transport-security")
            if not hsts:
                issues.append("Missing Strict-Transport-Security (HSTS) header.")
                evidence["missing_hsts"] = True
                passed = False
        else:
            # target is http://
            issues.append("Data is transmitted in cleartext over HTTP.")
            evidence["cleartext_http"] = True
            passed = False

        # 3. Check for mixed content
        if target.url.startswith("https://"):
            body_lower = target.response_body_snippet.lower()
            # Simple heuristic: looking for resources loaded over http://
            mixed_content_tags = re.findall(
                r'<(?:img|script|link|iframe|audio|video|source)[^>]+src=["\']http://',
                body_lower,
            )
            if mixed_content_tags:
                issues.append(
                    "Mixed Content: HTTP resources are loaded on an HTTPS page."
                )
                evidence["mixed_content"] = True
                passed = False

        # Evaluate overall severity
        if issues:
            if "Data is transmitted in cleartext over HTTP." in issues:
                severity = Severity.HIGH
                title = "Cleartext HTTP Usage"
                effort = Effort.LOW
            elif (
                "Invalid SSL/TLS Certificate." in issues
                or "Weak protocol version used:" in " ".join(issues)
            ):
                severity = Severity.HIGH
                title = "Weak TLS Configuration"
                effort = Effort.MEDIUM
            elif (
                "Missing Strict-Transport-Security (HSTS) header." in issues
                and len(issues) == 1
            ):
                severity = Severity.MEDIUM
                title = "Missing HSTS Header"
                effort = Effort.LOW
            else:
                severity = (
                    Severity.HIGH
                    if "Mixed Content" in " ".join(issues)
                    else Severity.MEDIUM
                )
                title = "Multiple Cryptographic Failures"
                effort = Effort.LOW

            description = (
                "The following cryptographic issues were identified: "
                + " ".join(issues)
            )
            business_impact = (
                "Sensitive data could be intercepted or modified in transit."
            )
            recommendation = (
                "Enforce HTTPS, use strong TLS versions (1.2+), and configure HSTS."
            )

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
            references=["https://owasp.org/Top10/A02_2021-Cryptographic_Failures/"],
        )
