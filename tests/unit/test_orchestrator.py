"""
Tests for the ScanOrchestrator.
"""

from engine.models import ScanTarget
from engine.orchestrator import ScanOrchestrator


def test_orchestrator_initialization() -> None:
    orchestrator = ScanOrchestrator()
    assert len(orchestrator.checks) == 10


def test_orchestrator_run_all() -> None:
    orchestrator = ScanOrchestrator()
    target = ScanTarget(
        url="https://example.com",
        response_headers={},
        cookies=[],
        tls_info=None,
        dns_records={},
        response_body_snippet="<html><body>OK</body></html>",
        status_code=200,
    )
    results = orchestrator.run_all(target)
    assert len(results) == 10
    owasp_ids = [r.owasp_id for r in results]
    assert "A01" in owasp_ids
    assert "A10" in owasp_ids
