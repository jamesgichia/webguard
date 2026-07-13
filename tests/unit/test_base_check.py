"""
Tests for the BaseCheck abstract class.
"""

import pytest

from engine.base_check import BaseCheck
from engine.models import CheckResult, Dimension, Effort, ScanTarget, Severity


def test_cannot_instantiate_base_check() -> None:
    """Ensure BaseCheck cannot be instantiated directly."""
    with pytest.raises(TypeError):
        BaseCheck()  # type: ignore


def test_valid_subclass_instantiation() -> None:
    """Ensure a valid subclass of BaseCheck can be instantiated."""

    class ValidCheck(BaseCheck):
        owasp_id = "A04"
        owasp_name = "Cryptographic Failures"
        dimension = Dimension.TRANSPORT_SECURITY.value

        def run(self, target: ScanTarget) -> CheckResult:
            return CheckResult(
                owasp_id=self.owasp_id,
                owasp_name=self.owasp_name,
                dimension=self.dimension,
                passed=True,
                severity=Severity.INFO,
                title="Test Title",
                description="Test description.",
                business_impact="Test business impact.",
                recommendation="Test recommendation.",
                effort=Effort.LOW,
            )

    check = ValidCheck()
    assert check.owasp_id == "A04"
    assert check.owasp_name == "Cryptographic Failures"
    assert check.dimension == "Transport Security"

    target = ScanTarget(
        url="https://example.com",
        response_headers={},
        cookies=[],
        tls_info=None,
        dns_records={},
        response_body_snippet="",
        status_code=200,
    )

    result = check.run(target)
    assert result.passed is True
