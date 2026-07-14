"""
Tests for the scoring engine.
"""

from engine.models import CheckResult, Dimension, Severity
from engine.scorer import Scorer, get_grade_and_label


def test_get_grade_and_label() -> None:
    assert get_grade_and_label(10.0) == ("A", "Excellent")
    assert get_grade_and_label(9.0) == ("A", "Excellent")
    assert get_grade_and_label(8.9) == ("B", "Good")
    assert get_grade_and_label(7.5) == ("B", "Good")
    assert get_grade_and_label(7.4) == ("C", "Fair")
    assert get_grade_and_label(6.0) == ("C", "Fair")
    assert get_grade_and_label(5.9) == ("D", "Poor")
    assert get_grade_and_label(4.0) == ("D", "Poor")
    assert get_grade_and_label(3.9) == ("F", "Critical")
    assert get_grade_and_label(0.0) == ("F", "Critical")


def test_scorer_all_pass() -> None:
    scorer = Scorer()
    # Empty results should mean no deductions
    scan_score = scorer.calculate([])

    assert scan_score.overall_score == 10.0
    assert scan_score.overall_grade == "A"
    assert scan_score.overall_label == "Excellent"

    for dim in scan_score.dimensions:
        assert dim.score == 10.0
        assert dim.grade == "A"


def test_scorer_with_deductions() -> None:
    scorer = Scorer()

    results = [
        # Transport Security: 1 HIGH (-2.0), 1 LOW (-0.5) -> score 7.5
        CheckResult(
            owasp_id="A04",
            owasp_name="",
            dimension=Dimension.TRANSPORT_SECURITY.value,
            passed=False,
            severity=Severity.HIGH,
            title="",
            description="",
            business_impact="",
            recommendation="",
            effort="",
            evidence={},
            references=[],
        ),
        CheckResult(
            owasp_id="A04",
            owasp_name="",
            dimension=Dimension.TRANSPORT_SECURITY.value,
            passed=False,
            severity=Severity.LOW,
            title="",
            description="",
            business_impact="",
            recommendation="",
            effort="",
            evidence={},
            references=[],
        ),
        # Header Configuration: 1 CRITICAL (-3.0), 1 MEDIUM (-1.0) -> score 6.0
        CheckResult(
            owasp_id="A06",
            owasp_name="",
            dimension=Dimension.HEADER_CONFIGURATION.value,
            passed=False,
            severity=Severity.CRITICAL,
            title="",
            description="",
            business_impact="",
            recommendation="",
            effort="",
            evidence={},
            references=[],
        ),
        CheckResult(
            owasp_id="A06",
            owasp_name="",
            dimension=Dimension.HEADER_CONFIGURATION.value,
            passed=False,
            severity=Severity.MEDIUM,
            title="",
            description="",
            business_impact="",
            recommendation="",
            effort="",
            evidence={},
            references=[],
        ),
        # Cookie Security: goes below 0.0 -> floor to 0.0
        CheckResult(
            owasp_id="A07",
            owasp_name="",
            dimension=Dimension.COOKIE_SECURITY.value,
            passed=False,
            severity=Severity.CRITICAL,
            title="",
            description="",
            business_impact="",
            recommendation="",
            effort="",
            evidence={},
            references=[],
        ),
        CheckResult(
            owasp_id="A07",
            owasp_name="",
            dimension=Dimension.COOKIE_SECURITY.value,
            passed=False,
            severity=Severity.CRITICAL,
            title="",
            description="",
            business_impact="",
            recommendation="",
            effort="",
            evidence={},
            references=[],
        ),
        CheckResult(
            owasp_id="A07",
            owasp_name="",
            dimension=Dimension.COOKIE_SECURITY.value,
            passed=False,
            severity=Severity.CRITICAL,
            title="",
            description="",
            business_impact="",
            recommendation="",
            effort="",
            evidence={},
            references=[],
        ),
        CheckResult(
            owasp_id="A07",
            owasp_name="",
            dimension=Dimension.COOKIE_SECURITY.value,
            passed=False,
            severity=Severity.CRITICAL,
            title="",
            description="",
            business_impact="",
            recommendation="",
            effort="",
            evidence={},
            references=[],
        ),
    ]

    scan_score = scorer.calculate(results)

    # Check individual dimensions
    ts_dim = next(
        d
        for d in scan_score.dimensions
        if d.dimension == Dimension.TRANSPORT_SECURITY.value
    )
    assert ts_dim.score == 7.5
    assert ts_dim.grade == "B"

    hc_dim = next(
        d
        for d in scan_score.dimensions
        if d.dimension == Dimension.HEADER_CONFIGURATION.value
    )
    assert hc_dim.score == 6.0
    assert hc_dim.grade == "C"

    cs_dim = next(
        d
        for d in scan_score.dimensions
        if d.dimension == Dimension.COOKIE_SECURITY.value
    )
    assert cs_dim.score == 0.0
    assert cs_dim.grade == "F"

    # Other dimensions should be 10.0
    csf_dim = next(
        d
        for d in scan_score.dimensions
        if d.dimension == Dimension.COMPONENT_SAFETY.value
    )
    assert csf_dim.score == 10.0

    # Calculate expected overall score
    # TS: 7.5 * 0.25 = 1.875
    # HC: 6.0 * 0.20 = 1.2
    # CS: 0.0 * 0.20 = 0.0
    # CompSaf: 10.0 * 0.15 = 1.5
    # InfoExp: 10.0 * 0.10 = 1.0
    # DNS: 10.0 * 0.10 = 1.0
    # Total = 6.575 -> rounded to 1 decimal place: 6.6

    assert scan_score.overall_score == 6.6
    assert scan_score.overall_grade == "C"
