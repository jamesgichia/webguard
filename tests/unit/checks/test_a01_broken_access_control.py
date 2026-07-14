"""
Tests for A01 Broken Access Control check.
"""

from engine.checks.a01_broken_access_control import A01BrokenAccessControlCheck
from engine.models import ScanTarget, Severity


def test_a01_secure_configuration() -> None:
    check = A01BrokenAccessControlCheck()
    target = ScanTarget(
        url="https://example.com",
        response_headers={"content-type": "text/html"},
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


def test_a01_directory_listing() -> None:
    check = A01BrokenAccessControlCheck()
    target = ScanTarget(
        url="https://example.com",
        response_headers={},
        cookies=[],
        tls_info=None,
        dns_records={},
        response_body_snippet="<html><head><title>Index of /</title></head></html>",
        status_code=200,
    )
    result = check.run(target)
    assert result.passed is False
    assert result.severity == Severity.HIGH
    assert "directory_listing" in result.evidence


def test_a01_permissive_cors() -> None:
    check = A01BrokenAccessControlCheck()
    target = ScanTarget(
        url="https://example.com",
        response_headers={"Access-Control-Allow-Origin": "*"},
        cookies=[],
        tls_info=None,
        dns_records={},
        response_body_snippet="{}",
        status_code=200,
    )
    result = check.run(target)
    assert result.passed is False
    assert result.severity == Severity.HIGH
    assert result.evidence.get("access-control-allow-origin") == "*"


def test_a01_multiple_issues() -> None:
    check = A01BrokenAccessControlCheck()
    target = ScanTarget(
        url="https://example.com",
        response_headers={"Access-Control-Allow-Origin": "*"},
        cookies=[],
        tls_info=None,
        dns_records={},
        response_body_snippet="<h1>Index of /</h1>",
        status_code=200,
    )
    result = check.run(target)
    assert result.passed is False
    assert result.severity == Severity.HIGH
    assert "directory_listing" in result.evidence
    assert result.evidence.get("access-control-allow-origin") == "*"
    assert result.title == "Multiple Access Control Issues"
