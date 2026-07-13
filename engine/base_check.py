"""
Abstract base class for all WebGuard checks.
"""

from abc import ABC, abstractmethod

from engine.models import CheckResult, ScanTarget


class BaseCheck(ABC):
    """
    Abstract base class that all scanning checks must implement.

    Each check represents a specific security control or vulnerability
    type and maps to an OWASP Top 10 category and a scoring dimension.
    """

    owasp_id: str
    owasp_name: str
    dimension: str

    @abstractmethod
    def run(self, target: ScanTarget) -> CheckResult:
        """
        Execute the security check against the provided target.

        Args:
            target (ScanTarget): The immutable HTTP response data and metadata.

        Returns:
            CheckResult: The outcome of the check, including severity,
                         recommendations, and evidence.
        """
        pass
