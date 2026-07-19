"""
Fetches the target URL and builds a ScanTarget for the engine.

This module performs three parallel data-collection tasks:
1. HTTP response fetch (headers, cookies, body, status code)
2. TLS certificate and connection inspection
3. DNS record resolution (A, AAAA, MX, TXT, NS, CAA, CNAME)

All data is packaged into a single ScanTarget so that no check
module ever needs to perform its own network requests.
"""

import asyncio
import logging
import ssl
import socket
from datetime import datetime, timezone
from typing import Any
from urllib.parse import urlparse

import dns.resolver
import httpx
from cryptography import x509
from cryptography.x509.oid import NameOID

from engine.models import ScanTarget, TLSInfo
from engine.url_validator import validate_and_normalize_url

logger = logging.getLogger(__name__)

# DNS record types we query for passive security analysis
_DNS_RECORD_TYPES = ("A", "AAAA", "MX", "TXT", "NS", "CAA", "CNAME")

# Timeout for individual DNS queries (seconds)
_DNS_QUERY_TIMEOUT = 5.0


async def fetch_target(url: str) -> ScanTarget:
    """
    Fetches the target URL and constructs a fully populated ScanTarget.

    Args:
        url: The raw URL to scan (will be validated and normalized).

    Returns:
        A ScanTarget populated with HTTP response data, TLS metadata,
        cookie attributes, and DNS records.

    Raises:
        InvalidTargetError: If the URL is invalid, unresolvable, or private.
        httpx.HTTPError: If the HTTP request fails.
    """
    url = validate_and_normalize_url(url)
    parsed = urlparse(url)
    hostname = parsed.hostname or ""

    # Run HTTP fetch, TLS inspection, and DNS resolution concurrently
    http_task = _fetch_http(url)
    tls_task = (
        _fetch_tls_info(hostname, parsed.port or 443)
        if parsed.scheme == "https"
        else _noop_tls()
    )
    dns_task = _resolve_dns_records(hostname)


    # Use gather for concurrency; TLS/DNS failures are non-fatal
    http_result, tls_info, dns_records = await asyncio.gather(
        http_task,
        tls_task,
        dns_task,
        return_exceptions=False,
    )

    response, headers, cookies, body, status_code = http_result

    return ScanTarget(
        url=str(response.url),
        response_headers=headers,
        cookies=cookies,
        tls_info=tls_info,
        dns_records=dns_records if isinstance(dns_records, dict) else {},
        response_body_snippet=body,
        status_code=status_code,
    )


async def _noop_tls() -> TLSInfo | None:
    """Returns None for non-HTTPS targets (no TLS to inspect)."""
    return None


async def _fetch_http(
    url: str,
) -> tuple[httpx.Response, dict[str, str], list[dict[str, Any]], str, int]:
    """
    Performs the HTTP GET request and extracts response data.

    Returns:
        A tuple of (response, headers_dict, cookies_list, body_snippet, status_code).
    """
    async with httpx.AsyncClient(verify=False, follow_redirects=True) as client:
        response = await client.get(url, timeout=30.0)

    headers = dict(response.headers)
    cookies = _extract_cookies(response)
    body = response.text[:4096]

    return response, headers, cookies, body, response.status_code


def _extract_cookies(response: httpx.Response) -> list[dict[str, Any]]:
    """
    Extracts cookies with their full security attributes from Set-Cookie headers.

    Parses the raw Set-Cookie header values to capture:
    - name, value
    - secure (bool)
    - httponly (bool)
    - samesite (str or None)
    - path, domain, expires, max-age

    This approach reads Set-Cookie headers directly rather than relying on
    httpx's cookie jar, which strips security attributes.
    """
    cookies: list[dict[str, Any]] = []
    set_cookie_headers = response.headers.get_list("set-cookie")

    for raw_header in set_cookie_headers:
        cookie = _parse_set_cookie_header(raw_header)
        if cookie:
            cookies.append(cookie)

    return cookies


def _parse_set_cookie_header(raw: str) -> dict[str, Any] | None:
    """
    Parses a single Set-Cookie header string into a structured dict.

    Example input:
        'session_id=abc123; Path=/; HttpOnly; Secure; SameSite=Strict'

    Returns:
        {'name': 'session_id', 'value': 'abc123', 'path': '/',
         'httponly': True, 'secure': True, 'samesite': 'Strict'}
    """
    if not raw or "=" not in raw.split(";")[0]:
        return None

    parts = [p.strip() for p in raw.split(";")]

    # First part is name=value
    name_value = parts[0]
    eq_idx = name_value.index("=")
    name = name_value[:eq_idx].strip()
    value = name_value[eq_idx + 1:].strip()

    cookie: dict[str, Any] = {
        "name": name,
        "value": value,
        "secure": False,
        "httponly": False,
        "samesite": None,
        "path": None,
        "domain": None,
        "expires": None,
        "max-age": None,
    }

    # Parse remaining attributes
    for attr in parts[1:]:
        attr_lower = attr.lower().strip()

        if attr_lower == "secure":
            cookie["secure"] = True
        elif attr_lower == "httponly":
            cookie["httponly"] = True
        elif attr_lower.startswith("samesite="):
            cookie["samesite"] = attr.split("=", 1)[1].strip()
        elif attr_lower.startswith("path="):
            cookie["path"] = attr.split("=", 1)[1].strip()
        elif attr_lower.startswith("domain="):
            cookie["domain"] = attr.split("=", 1)[1].strip()
        elif attr_lower.startswith("expires="):
            cookie["expires"] = attr.split("=", 1)[1].strip()
        elif attr_lower.startswith("max-age="):
            cookie["max-age"] = attr.split("=", 1)[1].strip()

    return cookie


async def _fetch_tls_info(hostname: str, port: int = 443) -> TLSInfo | None:
    """
    Connects to the target via raw SSL to extract TLS certificate metadata.

    Uses the low-level ssl module (not httpx) so we can inspect the
    actual certificate chain, protocol version, and cipher suite.

    Args:
        hostname: The target hostname.
        port: The TLS port (default 443).

    Returns:
        A TLSInfo dataclass, or None if TLS inspection fails.
    """
    try:
        return await asyncio.to_thread(_sync_fetch_tls_info, hostname, port)
    except Exception as exc:
        logger.warning("TLS inspection failed for %s:%d — %s", hostname, port, exc)
        return None


def _sync_fetch_tls_info(hostname: str, port: int = 443) -> TLSInfo:
    """
    Synchronous TLS inspection (run in a thread via asyncio.to_thread).

    Creates two connections:
    1. A validating connection to check certificate trust.
    2. A non-validating connection to always get cert details (even if expired/self-signed).
    """
    # --- Connection 1: Validate certificate ---
    certificate_is_valid = True
    try:
        ctx_verify = ssl.create_default_context()
        with socket.create_connection((hostname, port), timeout=10) as sock:
            with ctx_verify.wrap_socket(sock, server_hostname=hostname) as ssock:
                pass  # If we get here, cert is valid
    except (ssl.SSLCertVerificationError, ssl.SSLError):
        certificate_is_valid = False
    except (OSError, socket.timeout):
        # Connection-level error; we'll still try the non-validating path
        certificate_is_valid = False

    # --- Connection 2: Extract cert metadata (no validation) ---
    ctx_no_verify = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx_no_verify.check_hostname = False
    ctx_no_verify.verify_mode = ssl.CERT_NONE

    with socket.create_connection((hostname, port), timeout=10) as sock:
        with ctx_no_verify.wrap_socket(sock, server_hostname=hostname) as ssock:
            tls_version = ssock.version() or "Unknown"
            cipher_info = ssock.cipher()
            cipher_suite = cipher_info[0] if cipher_info else "Unknown"

            # Get the DER-encoded certificate
            der_cert = ssock.getpeercert(binary_form=True)

    if not der_cert:
        raise ValueError("No certificate returned by the server")

    # Parse the certificate with the cryptography library
    cert = x509.load_der_x509_certificate(der_cert)

    issuer = _extract_cn_or_org(cert.issuer)
    subject = _extract_cn_or_org(cert.subject)
    valid_from = cert.not_valid_before_utc.isoformat()
    valid_to = cert.not_valid_after_utc.isoformat()

    # Check expiry against current time
    now = datetime.now(timezone.utc)
    if now > cert.not_valid_after_utc or now < cert.not_valid_before_utc:
        certificate_is_valid = False

    return TLSInfo(
        version=tls_version,
        cipher_suite=cipher_suite,
        certificate_issuer=issuer,
        certificate_subject=subject,
        certificate_valid_from=valid_from,
        certificate_valid_to=valid_to,
        certificate_is_valid=certificate_is_valid,
    )


def _extract_cn_or_org(name: x509.Name) -> str:
    """
    Extracts the Common Name (CN) or Organization (O) from an X.509 name.

    Falls back to the full RFC 4514 string if neither is found.
    """
    try:
        cn = name.get_attributes_for_oid(NameOID.COMMON_NAME)
        if cn:
            return str(cn[0].value)
    except Exception:
        pass

    try:
        org = name.get_attributes_for_oid(NameOID.ORGANIZATION_NAME)
        if org:
            return str(org[0].value)
    except Exception:
        pass

    return name.rfc4514_string()


async def _resolve_dns_records(hostname: str) -> dict[str, list[str]]:
    """
    Resolves DNS records for the target hostname.

    Queries A, AAAA, MX, TXT, NS, CAA, and CNAME records.
    Individual query failures are silently skipped (the record type
    simply won't appear in the result dict).

    This runs the blocking dnspython resolver in a thread pool
    so it doesn't block the async event loop.

    Args:
        hostname: The target hostname to resolve.

    Returns:
        A dict mapping record type strings to lists of record value strings.
        Example: {"A": ["93.184.216.34"], "TXT": ["v=spf1 ..."]}
    """
    return await asyncio.to_thread(_sync_resolve_dns, hostname)


def _sync_resolve_dns(hostname: str) -> dict[str, list[str]]:
    """
    Synchronous DNS resolution (run in a thread via asyncio.to_thread).
    """
    resolver = dns.resolver.Resolver()
    resolver.timeout = _DNS_QUERY_TIMEOUT
    resolver.lifetime = _DNS_QUERY_TIMEOUT
    records: dict[str, list[str]] = {}

    for rtype in _DNS_RECORD_TYPES:
        try:
            answers = resolver.resolve(hostname, rtype)
            records[rtype] = [str(rdata) for rdata in answers]
        except (
            dns.resolver.NoAnswer,
            dns.resolver.NXDOMAIN,
            dns.resolver.NoNameservers,
            dns.resolver.Timeout,
            dns.name.EmptyLabel,
            Exception,
        ):
            # Record type not available — this is normal (e.g., no AAAA or CAA)
            continue

    return records
