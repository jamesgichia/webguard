"""
A03: Software Supply Chain Failures checks.
"""

import re

from engine.base_check import BaseCheck
from engine.models import CheckResult, Dimension, Effort, ScanTarget, Severity


class A03SupplyChainFailuresCheck(BaseCheck):
    """
    Checks for indicators of supply chain vulnerabilities, such as the
    absence of Subresource Integrity (SRI) on external scripts.
    """

    owasp_id = "A03"
    owasp_name = "Software Supply Chain Failures"
    dimension = Dimension.COMPONENT_SAFETY.value

    def run(self, target: ScanTarget) -> CheckResult:
        evidence = {}
        passed = True
        severity = Severity.INFO
        title = "Secure Supply Chain Indicators"
        description = (
            "No obvious passive indicators of supply chain failures were found."
        )
        business_impact = (
            "Protects the application from vulnerabilities in third-party components."
        )
        recommendation = "Continue to vet and monitor third-party scripts and libraries."
        effort = Effort.LOW

        body_lower = target.response_body_snippet.lower()

        # Check for missing SRI on external scripts
        script_tags = re.findall(r"<script\s+([^>]+)>", body_lower)
        scripts_missing_sri = []
        for attrs in script_tags:
            if "src=" in attrs and ("http://" in attrs or "https://" in attrs):
                if "integrity=" not in attrs:
                    src_match = re.search(r'src=["\']([^"\']+)["\']', attrs)
                    if src_match:
                        scripts_missing_sri.append(src_match.group(1))

        if scripts_missing_sri:
            passed = False
            severity = Severity.MEDIUM
            title = "Missing Subresource Integrity (SRI)"
            description = "External scripts are loaded without Subresource Integrity (SRI) attributes."
            business_impact = "If the external host is compromised, malicious code can be injected into the application."
            recommendation = (
                "Add integrity and crossorigin attributes to all external script tags."
            )
            evidence["scripts_missing_sri"] = scripts_missing_sri

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
                "https://owasp.org/Top10/A06_2021-Vulnerable_and_Outdated_Components/"
            ],
        )
