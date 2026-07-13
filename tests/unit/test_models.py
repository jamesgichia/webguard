"""
Tests for the core data models.
"""

from engine.models import (
    CheckResult,
    Dimension,
    Effort,
    ScanTarget,
    Severity,
    TLSInfo,
)


def test_severity_enum() -> None:
    """Test that Severity enum members have the correct string values."""
    assert Severity.INFO.value == "INFO"
    assert Severity.LOW.value == "LOW"
    assert Severity.MEDIUM.value == "MEDIUM"
    assert Severity.HIGH.value == "HIGH"
    assert Severity.CRITICAL.value == "CRITICAL"


def test_dimension_enum() -> None:
    """Test that Dimension enum members have the correct string values."""
    assert Dimension.TRANSPORT_SECURITY.value == "Transport Security"
    assert Dimension.HEADER_CONFIGURATION.value == "Header Configuration"
    assert Dimension.COOKIE_SECURITY.value == "Cookie Security"
    assert Dimension.COMPONENT_SAFETY.value == "Component Safety"
    assert Dimension.INFORMATION_EXPOSURE.value == "Information Exposure"
    assert Dimension.DNS_SECURITY.value == "DNS Security"


def test_effort_enum() -> None:
    """Test that Effort enum members have the correct string values."""
    assert Effort.LOW.value == "Low"
    assert Effort.MEDIUM.value == "Medium"
    assert Effort.HIGH.value == "High"


def test_tls_info_creation() -> None:
    """Test instantiation of TLSInfo dataclass."""
    tls = TLSInfo(
        version="TLSv1.3",
        cipher_suite="TLS_AES_256_GCM_SHA384",
        certificate_issuer="Let's Encrypt",
        certificate_subject="example.com",
        certificate_valid_from="2024-01-01",
        certificate_valid_to="2024-04-01",
        certificate_is_valid=True,
    )
    assert tls.version == "TLSv1.3"
    assert tls.certificate_is_valid is True


def test_scan_target_creation() -> None:
    """Test instantiation of ScanTarget dataclass."""
    target = ScanTarget(
        url="https://example.com",
        response_headers={"Server": "nginx"},
        cookies=[{"name": "session", "value": "123", "secure": True}],
        tls_info=None,
        dns_records={"A": ["192.0.2.1"]},
        response_body_snippet="<html>Hello</html>",
        status_code=200,
    )
    assert target.url == "https://example.com"
    assert target.status_code == 200
    assert target.tls_info is None


def test_check_result_creation() -> None:
    """Test instantiation of CheckResult dataclass."""
    result = CheckResult(
        owasp_id="A04",
        owasp_name="Cryptographic Failures",
        dimension=Dimension.TRANSPORT_SECURITY,
        passed=True,
        severity=Severity.INFO,
        title="TLS 1.3 Supported",
        description="The server supports TLS 1.3.",
        business_impact="Ensures data privacy.",
        recommendation="Maintain current configuration.",
        effort=Effort.LOW,
        evidence={"version": "TLSv1.3"},
        references=["https://owasp.org/A04"],
    )
    assert result.passed is True
    assert result.severity == Severity.INFO
    assert result.effort == Effort.LOW
    assert len(result.evidence) == 1
    assert len(result.references) == 1
