"""
Tests for A05 Injection check.
"""

from engine.checks.a05_injection import A05InjectionCheck
from engine.models import ScanTarget, Severity


def test_a05_secure_csp() -> None:
    check = A05InjectionCheck()
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
    assert result.passed is True
    assert result.severity == Severity.INFO


def test_a05_missing_csp() -> None:
    check = A05InjectionCheck()
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
    assert result.passed is False
    assert result.severity == Severity.MEDIUM
    assert "missing_csp" in result.evidence


def test_a05_weak_csp() -> None:
    check = A05InjectionCheck()
    target = ScanTarget(
        url="https://example.com",
        response_headers={
            "Content-Security-Policy": "default-src 'self' 'unsafe-inline'"
        },
        cookies=[],
        tls_info=None,
        dns_records={},
        response_body_snippet="",
        status_code=200,
    )
    result = check.run(target)
    assert result.passed is False
    assert result.severity == Severity.MEDIUM
    assert "unsafe-inline" in result.evidence["weak_csp_directives"]
