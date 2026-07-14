"""
Tests for A04 Cryptographic Failures check.
"""

from engine.checks.a04_cryptographic_failures import A04CryptographicFailuresCheck
from engine.models import ScanTarget, Severity, TLSInfo


def test_a04_secure_https() -> None:
    check = A04CryptographicFailuresCheck()
    tls = TLSInfo(
        version="TLSv1.3",
        cipher_suite="TLS_AES_256_GCM_SHA384",
        certificate_issuer="Let's Encrypt",
        certificate_subject="example.com",
        certificate_valid_from="2024-01-01",
        certificate_valid_to="2024-04-01",
        certificate_is_valid=True,
    )
    target = ScanTarget(
        url="https://example.com",
        response_headers={"Strict-Transport-Security": "max-age=31536000"},
        cookies=[],
        tls_info=tls,
        dns_records={},
        response_body_snippet="<html><body>Secure</body></html>",
        status_code=200,
    )
    result = check.run(target)
    assert result.passed is True
    assert result.severity == Severity.INFO


def test_a04_cleartext_http() -> None:
    check = A04CryptographicFailuresCheck()
    target = ScanTarget(
        url="http://example.com",
        response_headers={},
        cookies=[],
        tls_info=None,
        dns_records={},
        response_body_snippet="<html><body>Insecure</body></html>",
        status_code=200,
    )
    result = check.run(target)
    assert result.passed is False
    assert result.severity == Severity.HIGH
    assert "cleartext_http" in result.evidence


def test_a04_weak_tls() -> None:
    check = A04CryptographicFailuresCheck()
    tls = TLSInfo(
        version="TLSv1.0",
        cipher_suite="TLS_RSA_WITH_AES_128_CBC_SHA",
        certificate_issuer="Let's Encrypt",
        certificate_subject="example.com",
        certificate_valid_from="2024-01-01",
        certificate_valid_to="2024-04-01",
        certificate_is_valid=True,
    )
    target = ScanTarget(
        url="https://example.com",
        response_headers={"Strict-Transport-Security": "max-age=31536000"},
        cookies=[],
        tls_info=tls,
        dns_records={},
        response_body_snippet="<html><body>Weak</body></html>",
        status_code=200,
    )
    result = check.run(target)
    assert result.passed is False
    assert result.severity == Severity.HIGH
    assert result.evidence.get("tls_version") == "TLSv1.0"


def test_a04_invalid_certificate() -> None:
    check = A04CryptographicFailuresCheck()
    tls = TLSInfo(
        version="TLSv1.3",
        cipher_suite="TLS_AES_256_GCM_SHA384",
        certificate_issuer="Unknown CA",
        certificate_subject="example.com",
        certificate_valid_from="2024-01-01",
        certificate_valid_to="2024-04-01",
        certificate_is_valid=False,
    )
    target = ScanTarget(
        url="https://example.com",
        response_headers={"Strict-Transport-Security": "max-age=31536000"},
        cookies=[],
        tls_info=tls,
        dns_records={},
        response_body_snippet="<html><body>Invalid Cert</body></html>",
        status_code=200,
    )
    result = check.run(target)
    assert result.passed is False
    assert result.severity == Severity.HIGH
    assert result.evidence.get("certificate_valid") is False


def test_a04_missing_hsts() -> None:
    check = A04CryptographicFailuresCheck()
    tls = TLSInfo(
        version="TLSv1.2",
        cipher_suite="TLS_AES_256_GCM_SHA384",
        certificate_issuer="Let's Encrypt",
        certificate_subject="example.com",
        certificate_valid_from="2024-01-01",
        certificate_valid_to="2024-04-01",
        certificate_is_valid=True,
    )
    target = ScanTarget(
        url="https://example.com",
        response_headers={},
        cookies=[],
        tls_info=tls,
        dns_records={},
        response_body_snippet="<html><body>No HSTS</body></html>",
        status_code=200,
    )
    result = check.run(target)
    assert result.passed is False
    assert result.severity == Severity.MEDIUM
    assert "missing_hsts" in result.evidence


def test_a04_mixed_content() -> None:
    check = A04CryptographicFailuresCheck()
    tls = TLSInfo(
        version="TLSv1.2",
        cipher_suite="TLS_AES_256_GCM_SHA384",
        certificate_issuer="Let's Encrypt",
        certificate_subject="example.com",
        certificate_valid_from="2024-01-01",
        certificate_valid_to="2024-04-01",
        certificate_is_valid=True,
    )
    target = ScanTarget(
        url="https://example.com",
        response_headers={"Strict-Transport-Security": "max-age=31536000"},
        cookies=[],
        tls_info=tls,
        dns_records={},
        response_body_snippet='<html><body><img src="http://example.com/img.jpg"></body></html>',
        status_code=200,
    )
    result = check.run(target)
    assert result.passed is False
    assert result.severity == Severity.HIGH
    assert "mixed_content" in result.evidence
