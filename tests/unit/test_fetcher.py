"""
Unit tests for engine.fetcher — TLS, DNS, and cookie extraction.

All network calls are mocked. These tests verify:
1. Cookie attribute extraction from Set-Cookie headers
2. TLS info population for HTTPS targets
3. DNS record resolution
4. Graceful fallbacks when TLS/DNS fail
5. HTTP-only targets return tls_info=None
"""

import ssl
import socket
from datetime import datetime, timezone
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from engine.fetcher import (
    _extract_cookies,
    _parse_set_cookie_header,
    _sync_fetch_tls_info,
    _sync_resolve_dns,
    fetch_target,
)
from engine.models import ScanTarget, TLSInfo


# ---------------------------------------------------------------------------
# _parse_set_cookie_header tests
# ---------------------------------------------------------------------------


class TestParseSetCookieHeader:
    """Tests for individual Set-Cookie header parsing."""

    def test_full_cookie_with_all_attributes(self) -> None:
        raw = "session_id=abc123; Path=/; HttpOnly; Secure; SameSite=Strict; Domain=.example.com"
        result = _parse_set_cookie_header(raw)

        assert result is not None
        assert result["name"] == "session_id"
        assert result["value"] == "abc123"
        assert result["secure"] is True
        assert result["httponly"] is True
        assert result["samesite"] == "Strict"
        assert result["path"] == "/"
        assert result["domain"] == ".example.com"

    def test_cookie_without_security_flags(self) -> None:
        raw = "tracking=xyz789; Path=/"
        result = _parse_set_cookie_header(raw)

        assert result is not None
        assert result["name"] == "tracking"
        assert result["value"] == "xyz789"
        assert result["secure"] is False
        assert result["httponly"] is False
        assert result["samesite"] is None

    def test_cookie_with_max_age_and_expires(self) -> None:
        raw = "token=abc; Max-Age=3600; Expires=Thu, 01 Jan 2099 00:00:00 GMT"
        result = _parse_set_cookie_header(raw)

        assert result is not None
        assert result["max-age"] == "3600"
        assert result["expires"] == "Thu, 01 Jan 2099 00:00:00 GMT"

    def test_cookie_samesite_lax(self) -> None:
        raw = "pref=dark; SameSite=Lax; Secure"
        result = _parse_set_cookie_header(raw)

        assert result is not None
        assert result["samesite"] == "Lax"
        assert result["secure"] is True

    def test_empty_string_returns_none(self) -> None:
        assert _parse_set_cookie_header("") is None

    def test_invalid_cookie_no_equals(self) -> None:
        assert _parse_set_cookie_header("invalidcookie") is None

    def test_cookie_value_with_equals_sign(self) -> None:
        raw = "token=abc=def=ghi; Secure"
        result = _parse_set_cookie_header(raw)

        assert result is not None
        assert result["name"] == "token"
        assert result["value"] == "abc=def=ghi"
        assert result["secure"] is True

    def test_cookie_case_insensitive_attributes(self) -> None:
        raw = "id=1; SECURE; HTTPONLY; SAMESITE=Strict"
        result = _parse_set_cookie_header(raw)

        assert result is not None
        assert result["secure"] is True
        assert result["httponly"] is True
        assert result["samesite"] == "Strict"


# ---------------------------------------------------------------------------
# _extract_cookies tests
# ---------------------------------------------------------------------------


class TestExtractCookies:
    """Tests for extracting cookies from httpx responses."""

    def test_extracts_multiple_cookies(self) -> None:
        response = MagicMock(spec=httpx.Response)
        response.headers = httpx.Headers(
            [
                ("set-cookie", "a=1; Secure; HttpOnly"),
                ("set-cookie", "b=2; SameSite=Lax"),
            ]
        )

        cookies = _extract_cookies(response)

        assert len(cookies) == 2
        assert cookies[0]["name"] == "a"
        assert cookies[0]["secure"] is True
        assert cookies[0]["httponly"] is True
        assert cookies[1]["name"] == "b"
        assert cookies[1]["samesite"] == "Lax"

    def test_no_cookies_returns_empty_list(self) -> None:
        response = MagicMock(spec=httpx.Response)
        response.headers = httpx.Headers([])

        cookies = _extract_cookies(response)
        assert cookies == []


# ---------------------------------------------------------------------------
# _sync_resolve_dns tests
# ---------------------------------------------------------------------------


class TestSyncResolveDns:
    """Tests for DNS resolution logic."""

    @patch("engine.fetcher.dns.resolver.Resolver")
    def test_resolves_multiple_record_types(self, mock_resolver_cls: MagicMock) -> None:
        mock_resolver = MagicMock()
        mock_resolver_cls.return_value = mock_resolver

        # Simulate A records returning, TXT returning, others raising NoAnswer
        def side_effect(hostname: str, rtype: str) -> Any:
            if rtype == "A":
                record = MagicMock()
                record.__iter__ = lambda self: iter([MagicMock(__str__=lambda s: "93.184.216.34")])
                return record
            elif rtype == "TXT":
                record = MagicMock()
                record.__iter__ = lambda self: iter([MagicMock(__str__=lambda s: "v=spf1 include:example.com ~all")])
                return record
            else:
                import dns.resolver
                raise dns.resolver.NoAnswer()

        mock_resolver.resolve = MagicMock(side_effect=side_effect)

        records = _sync_resolve_dns("example.com")

        assert "A" in records
        assert records["A"] == ["93.184.216.34"]
        assert "TXT" in records
        assert "v=spf1" in records["TXT"][0]

    @patch("engine.fetcher.dns.resolver.Resolver")
    def test_handles_nxdomain(self, mock_resolver_cls: MagicMock) -> None:
        import dns.resolver
        mock_resolver = MagicMock()
        mock_resolver_cls.return_value = mock_resolver
        mock_resolver.resolve = MagicMock(side_effect=dns.resolver.NXDOMAIN())

        records = _sync_resolve_dns("nonexistent.invalid")
        assert records == {}

    @patch("engine.fetcher.dns.resolver.Resolver")
    def test_handles_timeout(self, mock_resolver_cls: MagicMock) -> None:
        import dns.resolver
        mock_resolver = MagicMock()
        mock_resolver_cls.return_value = mock_resolver
        mock_resolver.resolve = MagicMock(side_effect=dns.resolver.Timeout())

        records = _sync_resolve_dns("slow.example.com")
        assert records == {}


# ---------------------------------------------------------------------------
# fetch_target integration tests (with mocking)
# ---------------------------------------------------------------------------


class TestFetchTarget:
    """Tests for the main fetch_target function with mocked I/O."""

    @pytest.mark.asyncio
    @patch("engine.fetcher._resolve_dns_records")
    @patch("engine.fetcher._fetch_tls_info")
    @patch("engine.fetcher._fetch_http")
    @patch("engine.fetcher.validate_and_normalize_url")
    async def test_https_target_populates_all_fields(
        self,
        mock_validate: MagicMock,
        mock_http: AsyncMock,
        mock_tls: AsyncMock,
        mock_dns: AsyncMock,
    ) -> None:
        mock_validate.return_value = "https://example.com/"

        # Mock HTTP response
        mock_response = MagicMock(spec=httpx.Response)
        mock_response.url = "https://example.com/"
        mock_http.return_value = (
            mock_response,
            {"content-type": "text/html", "strict-transport-security": "max-age=31536000"},
            [{"name": "sid", "value": "x", "secure": True, "httponly": True, "samesite": "Strict"}],
            "<html></html>",
            200,
        )

        # Mock TLS info
        mock_tls.return_value = TLSInfo(
            version="TLSv1.3",
            cipher_suite="TLS_AES_256_GCM_SHA384",
            certificate_issuer="Let's Encrypt",
            certificate_subject="example.com",
            certificate_valid_from="2024-01-01T00:00:00+00:00",
            certificate_valid_to="2099-01-01T00:00:00+00:00",
            certificate_is_valid=True,
        )

        # Mock DNS
        mock_dns.return_value = {"A": ["93.184.216.34"], "TXT": ["v=spf1 include:example.com ~all"]}

        result = await fetch_target("https://example.com")

        assert isinstance(result, ScanTarget)
        assert result.url == "https://example.com/"
        assert result.status_code == 200
        assert result.tls_info is not None
        assert result.tls_info.version == "TLSv1.3"
        assert result.tls_info.certificate_is_valid is True
        assert result.dns_records["A"] == ["93.184.216.34"]
        assert len(result.cookies) == 1
        assert result.cookies[0]["secure"] is True

    @pytest.mark.asyncio
    @patch("engine.fetcher._resolve_dns_records")
    @patch("engine.fetcher._fetch_http")
    @patch("engine.fetcher.validate_and_normalize_url")
    async def test_http_target_has_no_tls(
        self,
        mock_validate: MagicMock,
        mock_http: AsyncMock,
        mock_dns: AsyncMock,
    ) -> None:
        mock_validate.return_value = "http://example.com/"

        mock_response = MagicMock(spec=httpx.Response)
        mock_response.url = "http://example.com/"
        mock_http.return_value = (
            mock_response,
            {"content-type": "text/html"},
            [],
            "<html></html>",
            200,
        )
        mock_dns.return_value = {"A": ["93.184.216.34"]}

        result = await fetch_target("http://example.com")

        assert result.tls_info is None
        assert result.dns_records == {"A": ["93.184.216.34"]}

    @pytest.mark.asyncio
    @patch("engine.fetcher._resolve_dns_records")
    @patch("engine.fetcher._fetch_tls_info")
    @patch("engine.fetcher._fetch_http")
    @patch("engine.fetcher.validate_and_normalize_url")
    async def test_tls_failure_returns_none_gracefully(
        self,
        mock_validate: MagicMock,
        mock_http: AsyncMock,
        mock_tls: AsyncMock,
        mock_dns: AsyncMock,
    ) -> None:
        mock_validate.return_value = "https://broken-tls.example.com/"

        mock_response = MagicMock(spec=httpx.Response)
        mock_response.url = "https://broken-tls.example.com/"
        mock_http.return_value = (
            mock_response,
            {},
            [],
            "",
            200,
        )
        mock_tls.return_value = None
        mock_dns.return_value = {}

        result = await fetch_target("https://broken-tls.example.com")

        assert result.tls_info is None
        assert result.dns_records == {}

    @pytest.mark.asyncio
    @patch("engine.fetcher._resolve_dns_records")
    @patch("engine.fetcher._fetch_tls_info")
    @patch("engine.fetcher._fetch_http")
    @patch("engine.fetcher.validate_and_normalize_url")
    async def test_dns_failure_returns_empty_dict(
        self,
        mock_validate: MagicMock,
        mock_http: AsyncMock,
        mock_tls: AsyncMock,
        mock_dns: AsyncMock,
    ) -> None:
        mock_validate.return_value = "https://example.com/"

        mock_response = MagicMock(spec=httpx.Response)
        mock_response.url = "https://example.com/"
        mock_http.return_value = (
            mock_response,
            {},
            [],
            "",
            200,
        )
        mock_tls.return_value = None
        mock_dns.return_value = {}

        result = await fetch_target("https://example.com")
        assert result.dns_records == {}
