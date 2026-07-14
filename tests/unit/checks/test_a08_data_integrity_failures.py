"""
Tests for A08 Software and Data Integrity Failures check.
"""

from engine.checks.a08_data_integrity_failures import A08DataIntegrityFailuresCheck
from engine.models import ScanTarget, Severity


def test_a08_secure_csp() -> None:
    check = A08DataIntegrityFailuresCheck()
    target = ScanTarget(
        url="https://example.com",
        response_headers={
            "Content-Security-Policy": "default-src 'self'; strict-dynamic"
        },
        cookies=[],
        tls_info=None,
        dns_records={},
        response_body_snippet="",
        status_code=200,
    )
    result = check.run(target)
    assert result.passed is True
    assert result.severity == Severity.INFO


def test_a08_weak_csp() -> None:
    check = A08DataIntegrityFailuresCheck()
    target = ScanTarget(
        url="https://example.com",
        response_headers={"Content-Security-Policy": "default-src 'self'"},
        cookies=[],
        tls_info=None,
        dns_records={},
        response_body_snippet="",
        status_code=200,
    )
    result = check.run(target)
    assert result.passed is False
    assert result.severity == Severity.LOW
    assert "csp" in result.evidence
