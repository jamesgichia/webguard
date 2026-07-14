"""
Tests for A10 Mishandling of Exceptional Conditions check.
"""

from engine.checks.a10_exceptional_conditions import A10ExceptionalConditionsCheck
from engine.models import ScanTarget, Severity


def test_a10_secure_error() -> None:
    check = A10ExceptionalConditionsCheck()
    target = ScanTarget(
        url="https://example.com",
        response_headers={},
        cookies=[],
        tls_info=None,
        dns_records={},
        response_body_snippet="<html><body>Internal Server Error</body></html>",
        status_code=500,
    )
    result = check.run(target)
    assert result.passed is True
    assert result.severity == Severity.INFO


def test_a10_verbose_error() -> None:
    check = A10ExceptionalConditionsCheck()
    target = ScanTarget(
        url="https://example.com",
        response_headers={},
        cookies=[],
        tls_info=None,
        dns_records={},
        response_body_snippet="<html><body>Traceback (most recent call last):<br>File...</body></html>",
        status_code=500,
    )
    result = check.run(target)
    assert result.passed is False
    assert result.severity == Severity.HIGH
    assert "stack_trace_detected" in result.evidence


def test_a10_ok_response() -> None:
    check = A10ExceptionalConditionsCheck()
    target = ScanTarget(
        url="https://example.com",
        response_headers={},
        cookies=[],
        tls_info=None,
        dns_records={},
        response_body_snippet="<html><body>OK</body></html>",
        status_code=200,
    )
    result = check.run(target)
    assert result.passed is True
