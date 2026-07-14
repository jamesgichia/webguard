"""
Tests for A06 Insecure Design check.
"""

from engine.checks.a06_insecure_design import A06InsecureDesignCheck
from engine.models import ScanTarget, Severity


def test_a06_secure_cache_control() -> None:
    check = A06InsecureDesignCheck()
    target = ScanTarget(
        url="https://example.com",
        response_headers={"Cache-Control": "no-store, max-age=0"},
        cookies=[],
        tls_info=None,
        dns_records={},
        response_body_snippet="",
        status_code=200,
    )
    result = check.run(target)
    assert result.passed is True
    assert result.severity == Severity.INFO


def test_a06_insecure_cache_control() -> None:
    check = A06InsecureDesignCheck()
    target = ScanTarget(
        url="https://example.com",
        response_headers={"Cache-Control": "public, max-age=3600"},
        cookies=[],
        tls_info=None,
        dns_records={},
        response_body_snippet="",
        status_code=200,
    )
    result = check.run(target)
    assert result.passed is False
    assert result.severity == Severity.LOW
    assert result.evidence.get("cache-control") == "public, max-age=3600"


def test_a06_missing_cache_control() -> None:
    check = A06InsecureDesignCheck()
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
    assert result.severity == Severity.LOW
    assert "cache-control" in result.evidence
