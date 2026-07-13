"""
Tests for URL validation and normalization.
"""

import socket
from unittest.mock import patch

import pytest

from engine.url_validator import InvalidTargetError, validate_and_normalize_url


@patch("engine.url_validator.socket.gethostbyname")
def test_valid_https_url(mock_gethostbyname) -> None:
    """Test valid HTTP and HTTPS URLs."""
    mock_gethostbyname.return_value = "8.8.8.8"
    assert validate_and_normalize_url("https://example.com") == "https://example.com"
    assert validate_and_normalize_url("example.com") == "https://example.com"


@patch("engine.url_validator.socket.gethostbyname")
def test_private_ip(mock_gethostbyname) -> None:
    """Test that private IPs raise InvalidTargetError."""
    mock_gethostbyname.return_value = "192.168.1.1"
    with pytest.raises(InvalidTargetError, match="strictly forbidden"):
        validate_and_normalize_url("https://example.local")


@patch("engine.url_validator.socket.gethostbyname")
def test_loopback_ip(mock_gethostbyname) -> None:
    """Test that loopback IPs raise InvalidTargetError."""
    mock_gethostbyname.return_value = "127.0.0.1"
    with pytest.raises(InvalidTargetError, match="strictly forbidden"):
        validate_and_normalize_url("http://localhost")


@patch("engine.url_validator.socket.gethostbyname")
def test_unresolvable_host(mock_gethostbyname) -> None:
    """Test that unresolvable hostnames raise InvalidTargetError."""
    mock_gethostbyname.side_effect = socket.gaierror("Name or service not known")
    with pytest.raises(InvalidTargetError, match="Could not resolve hostname"):
        validate_and_normalize_url("https://this-does-not-exist.example.com")


def test_invalid_scheme() -> None:
    """Test that non-HTTP(S) schemes raise InvalidTargetError."""
    with pytest.raises(InvalidTargetError, match="URL scheme must be http or https"):
        validate_and_normalize_url("ftp://example.com")


def test_invalid_url_format() -> None:
    """Test that completely invalid URL structures are caught."""
    with pytest.raises(InvalidTargetError, match="Invalid URL provided"):
        validate_and_normalize_url("http://")
