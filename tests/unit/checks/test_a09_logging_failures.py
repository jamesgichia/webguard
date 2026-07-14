"""
Tests for A09 Security Logging and Alerting Failures check.
"""

from engine.checks.a09_logging_failures import A09LoggingFailuresCheck
from engine.models import ScanTarget, Severity


def test_a09_unverifiable() -> None:
    check = A09LoggingFailuresCheck()
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
    assert result.severity == Severity.INFO
    assert result.title == "Unverifiable Passively"
