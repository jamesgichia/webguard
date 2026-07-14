"""
Fetches the target URL and builds a ScanTarget for the engine.
"""

import httpx

from engine.models import ScanTarget
from engine.url_validator import validate_and_normalize_url


async def fetch_target(url: str) -> ScanTarget:
    """
    Fetches the target URL and constructs a ScanTarget.
    """
    url = validate_and_normalize_url(url)

    async with httpx.AsyncClient(verify=False, follow_redirects=True) as client:
        response = await client.get(url, timeout=30.0)

    headers = dict(response.headers)
    cookies = []
    
    # Simple cookie extraction for basic passive checks
    for name, value in response.cookies.items():
        cookies.append({"name": name, "value": value})

    body = response.text[:4096]

    return ScanTarget(
        url=str(response.url),
        response_headers=headers,
        cookies=cookies,
        tls_info=None,
        dns_records={},
        response_body_snippet=body,
        status_code=response.status_code,
    )
