"""
Tests for A02 Security Misconfiguration check.
"""

from engine.checks.a02_security_misconfiguration import (
    A02SecurityMisconfigurationCheck,
)
from engine.models import ScanTarget, Severity


def test_a02_secure_configuration() -> None:
    check = A02SecurityMisconfigurationCheck()
    target = ScanTarget(
        url="https://example.com",
        response_headers={
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "Content-Security-Policy": "default-src 'self'",
            "Server": "nginx",
        },
        cookies=[],
        tls_info=None,
        dns_records={},
        response_body_snippet="<html><body>Hello</body></html>",
        status_code=200,
    )
    result = check.run(target)
    assert result.passed is True
    assert result.severity == Severity.INFO
    assert not result.evidence


def test_a02_missing_headers() -> None:
    check = A02SecurityMisconfigurationCheck()
    target = ScanTarget(
        url="https://example.com",
        response_headers={"Server": "nginx"},
        cookies=[],
        tls_info=None,
        dns_records={},
        response_body_snippet="<html><body>Hello</body></html>",
        status_code=200,
    )
    result = check.run(target)
    assert result.passed is False
    assert result.severity == Severity.MEDIUM
    assert "missing_headers" in result.evidence
    assert len(result.evidence["missing_headers"]) == 3


def test_a02_verbose_headers() -> None:
    check = A02SecurityMisconfigurationCheck()
    target = ScanTarget(
        url="https://example.com",
        response_headers={
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "Content-Security-Policy": "default-src 'self'",
            "Server": "nginx/1.24.0",
            "X-Powered-By": "Express",
        },
        cookies=[],
        tls_info=None,
        dns_records={},
        response_body_snippet="<html><body>Hello</body></html>",
        status_code=200,
    )
    result = check.run(target)
    assert result.passed is False
    assert result.severity == Severity.LOW
    assert "verbose_headers" in result.evidence
    assert result.evidence["verbose_headers"]["server"] == "nginx/1.24.0"
    assert result.evidence["verbose_headers"]["x-powered-by"] == "Express"


def test_a02_multiple_issues() -> None:
    check = A02SecurityMisconfigurationCheck()
    target = ScanTarget(
        url="https://example.com",
        response_headers={
            "Server": "nginx/1.24.0",
        },
        cookies=[],
        tls_info=None,
        dns_records={},
        response_body_snippet="<html><body>Hello</body></html>",
        status_code=200,
    )
    result = check.run(target)
    assert result.passed is False
    assert result.severity == Severity.MEDIUM
    assert "missing_headers" in result.evidence
    assert "verbose_headers" in result.evidence
    assert result.title == "Multiple Security Misconfigurations"
