"""
URL validation and normalization for WebGuard targets.
"""

import ipaddress
import socket
from urllib.parse import urlparse


class InvalidTargetError(Exception):
    """Raised when a target URL is invalid, malformed, or points to a private IP."""
    pass


def validate_and_normalize_url(url: str) -> str:
    """
    Validates the target URL and normalizes it.

    Checks:
    - URL scheme must be http or https.
    - Hostname must be resolvable.
    - Resolved IP must not be a private or loopback address.

    Args:
        url (str): The target URL to validate.

    Returns:
        str: The normalized URL.

    Raises:
        InvalidTargetError: If the URL is invalid or points to an internal IP.
    """
    if not url.startswith(("http://", "https://", "ftp://")):
        url = "https://" + url

    parsed = urlparse(url)

    if not parsed.hostname:
        raise InvalidTargetError(f"Invalid URL provided: {url}")

    if parsed.scheme not in ("http", "https"):
        raise InvalidTargetError("URL scheme must be http or https.")

    try:
        ip_addr = socket.gethostbyname(parsed.hostname)
    except socket.gaierror:
        raise InvalidTargetError(f"Could not resolve hostname: {parsed.hostname}")

    ip_obj = ipaddress.ip_address(ip_addr)

    if ip_obj.is_private or ip_obj.is_loopback:
        raise InvalidTargetError(
            "Scanning private or loopback IP addresses is strictly forbidden."
        )

    # Return normalized URL
    return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
