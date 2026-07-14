"""
Tests for A03 Software Supply Chain Failures check.
"""

from engine.checks.a03_supply_chain_failures import A03SupplyChainFailuresCheck
from engine.models import ScanTarget, Severity


def test_a03_secure_configuration() -> None:
    check = A03SupplyChainFailuresCheck()
    body = '<script src="https://cdn.example.com/lib.js" integrity="sha384-..." crossorigin="anonymous"></script>'
    target = ScanTarget(
        url="https://example.com",
        response_headers={},
        cookies=[],
        tls_info=None,
        dns_records={},
        response_body_snippet=body,
        status_code=200,
    )
    result = check.run(target)
    assert result.passed is True
    assert result.severity == Severity.INFO
    assert not result.evidence


def test_a03_missing_sri() -> None:
    check = A03SupplyChainFailuresCheck()
    body = '<script src="https://cdn.example.com/lib.js"></script>'
    target = ScanTarget(
        url="https://example.com",
        response_headers={},
        cookies=[],
        tls_info=None,
        dns_records={},
        response_body_snippet=body,
        status_code=200,
    )
    result = check.run(target)
    assert result.passed is False
    assert result.severity == Severity.MEDIUM
    assert "scripts_missing_sri" in result.evidence
    assert result.evidence["scripts_missing_sri"][0] == "https://cdn.example.com/lib.js"


def test_a03_local_script() -> None:
    check = A03SupplyChainFailuresCheck()
    body = '<script src="/static/app.js"></script>'
    target = ScanTarget(
        url="https://example.com",
        response_headers={},
        cookies=[],
        tls_info=None,
        dns_records={},
        response_body_snippet=body,
        status_code=200,
    )
    result = check.run(target)
    assert result.passed is True
