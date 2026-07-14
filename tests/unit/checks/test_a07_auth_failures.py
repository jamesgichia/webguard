"""
Tests for A07 Authentication Failures check.
"""

from engine.checks.a07_auth_failures import A07AuthenticationFailuresCheck
from engine.models import ScanTarget, Severity


def test_a07_secure_cookies() -> None:
    check = A07AuthenticationFailuresCheck()
    target = ScanTarget(
        url="https://example.com",
        response_headers={},
        cookies=[
            {
                "name": "session_id",
                "value": "xyz",
                "secure": True,
                "httponly": True,
                "samesite": "Strict",
            }
        ],
        tls_info=None,
        dns_records={},
        response_body_snippet="",
        status_code=200,
    )
    result = check.run(target)
    assert result.passed is True
    assert result.severity == Severity.INFO


def test_a07_insecure_cookies() -> None:
    check = A07AuthenticationFailuresCheck()
    target = ScanTarget(
        url="https://example.com",
        response_headers={},
        cookies=[
            {
                "name": "session_id",
                "value": "xyz",
                "secure": False,
                "httponly": False,
                "samesite": "None",
            }
        ],
        tls_info=None,
        dns_records={},
        response_body_snippet="",
        status_code=200,
    )
    result = check.run(target)
    assert result.passed is False
    assert result.severity == Severity.HIGH
    assert len(result.evidence["insecure_cookies"]) == 1
    issues = result.evidence["insecure_cookies"][0]["issues"]
    assert "Missing 'Secure' flag" in issues
    assert "Missing 'HttpOnly' flag" in issues
    assert "Weak or missing 'SameSite' attribute" in issues


def test_a07_no_cookies() -> None:
    check = A07AuthenticationFailuresCheck()
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
