"""
Orchestrates the execution of all passive security checks against a ScanTarget.
"""

from engine.checks.a01_broken_access_control import A01BrokenAccessControlCheck
from engine.checks.a02_security_misconfiguration import A02SecurityMisconfigurationCheck
from engine.checks.a03_supply_chain_failures import A03SupplyChainFailuresCheck
from engine.checks.a04_cryptographic_failures import A04CryptographicFailuresCheck
from engine.checks.a05_injection import A05InjectionCheck
from engine.checks.a06_insecure_design import A06InsecureDesignCheck
from engine.checks.a07_auth_failures import A07AuthenticationFailuresCheck
from engine.checks.a08_data_integrity_failures import A08DataIntegrityFailuresCheck
from engine.checks.a09_logging_failures import A09LoggingFailuresCheck
from engine.checks.a10_exceptional_conditions import A10ExceptionalConditionsCheck
from engine.models import CheckResult, ScanTarget


def get_all_checks() -> list:
    """Returns a list of instantiated check modules."""
    return [
        A01BrokenAccessControlCheck(),
        A02SecurityMisconfigurationCheck(),
        A03SupplyChainFailuresCheck(),
        A04CryptographicFailuresCheck(),
        A05InjectionCheck(),
        A06InsecureDesignCheck(),
        A07AuthenticationFailuresCheck(),
        A08DataIntegrityFailuresCheck(),
        A09LoggingFailuresCheck(),
        A10ExceptionalConditionsCheck(),
    ]


class ScanOrchestrator:
    """
    Coordinates the execution of multiple checks on a given ScanTarget.
    """

    def __init__(self) -> None:
        self.checks = get_all_checks()

    def run_all(self, target: ScanTarget) -> list[CheckResult]:
        """
        Executes all registered checks against the target.

        Args:
            target (ScanTarget): The target HTTP data.

        Returns:
            list[CheckResult]: The results from all checks.
        """
        results = []
        for check in self.checks:
            result = check.run(target)
            results.append(result)
        return results
