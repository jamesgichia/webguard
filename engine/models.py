"""
Core data models for the WebGuard passive scanning engine.

This module defines the essential data structures used throughout the engine,
including the definition of a scan target, the structure of findings, and
the various severity and scoring enumerations.
"""

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class Severity(StrEnum):
    """Vulnerability severity levels, mapping to scoring deductions."""

    INFO = "INFO"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class Effort(StrEnum):
    """Estimated effort required to remediate a finding."""

    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class Dimension(StrEnum):
    """The six core scoring dimensions for the WebGuard report."""

    TRANSPORT_SECURITY = "Transport Security"
    HEADER_CONFIGURATION = "Header Configuration"
    COOKIE_SECURITY = "Cookie Security"
    COMPONENT_SAFETY = "Component Safety"
    INFORMATION_EXPOSURE = "Information Exposure"
    DNS_SECURITY = "DNS Security"


@dataclass
class TLSInfo:
    """TLS metadata extracted during the connection phase."""

    version: str
    cipher_suite: str
    certificate_issuer: str
    certificate_subject: str
    certificate_valid_from: str
    certificate_valid_to: str
    certificate_is_valid: bool


@dataclass
class ScanTarget:
    """
    The immutable target payload provided to every check module.

    Contains the full HTTP response data so no check ever needs
    to fetch data independently.
    """

    url: str
    response_headers: dict[str, str]
    cookies: list[dict[str, Any]]
    tls_info: TLSInfo | None
    dns_records: dict[str, list[str]]
    response_body_snippet: str  # first 4KB only
    status_code: int


@dataclass
class CheckResult:
    """
    The standardized result structure returned by every check.

    A check returns one result; if the check 'passed', the finding
    represents a confirmation of secure configuration. If it failed,
    it represents a vulnerability.
    """

    owasp_id: str
    owasp_name: str
    dimension: str
    passed: bool
    severity: Severity
    title: str
    description: str
    business_impact: str
    recommendation: str
    effort: str
    evidence: dict[str, Any] = field(default_factory=dict)
    references: list[str] = field(default_factory=list)
