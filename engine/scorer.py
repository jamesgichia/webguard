"""
Scoring engine for evaluating WebGuard check results.
"""

from engine.models import CheckResult, Dimension, DimensionScore, ScanScore, Severity

# Weights from CLAUDE.md
DIMENSION_WEIGHTS = {
    Dimension.TRANSPORT_SECURITY.value: 0.25,
    Dimension.HEADER_CONFIGURATION.value: 0.20,
    Dimension.COOKIE_SECURITY.value: 0.20,
    Dimension.COMPONENT_SAFETY.value: 0.15,
    Dimension.INFORMATION_EXPOSURE.value: 0.10,
    Dimension.DNS_SECURITY.value: 0.10,
}

SEVERITY_DEDUCTIONS = {
    Severity.CRITICAL: 3.0,
    Severity.HIGH: 2.0,
    Severity.MEDIUM: 1.0,
    Severity.LOW: 0.5,
    Severity.INFO: 0.0,
}


def get_grade_and_label(score: float) -> tuple[str, str]:
    """Returns the grade (A-F) and label based on the score."""
    if score >= 9.0:
        return "A", "Excellent"
    elif score >= 7.5:
        return "B", "Good"
    elif score >= 6.0:
        return "C", "Fair"
    elif score >= 4.0:
        return "D", "Poor"
    else:
        return "F", "Critical"


class Scorer:
    """
    Calculates dimension scores and the overall scan score based on check results.
    """

    def calculate(self, results: list[CheckResult]) -> ScanScore:
        """
        Calculates the score from 0.0 to 10.0 for each dimension, and an overall weighted score.
        """
        # Initialize dimension scores to 10.0
        dimension_scores_raw = {dim.value: 10.0 for dim in Dimension}

        # Apply deductions based on failures
        for result in results:
            if not result.passed:
                deduction = SEVERITY_DEDUCTIONS.get(result.severity, 0.0)
                dimension_scores_raw[result.dimension] -= deduction

        # Ensure floor of 0.0 and construct DimensionScore objects
        dimension_scores = []
        overall_score = 0.0

        for dim_value, raw_score in dimension_scores_raw.items():
            # Floor at 0.0
            final_score = max(0.0, raw_score)

            grade, label = get_grade_and_label(final_score)
            weight = DIMENSION_WEIGHTS.get(dim_value, 0.0)

            dimension_scores.append(
                DimensionScore(
                    dimension=dim_value,
                    score=round(final_score, 1),
                    weight=weight,
                    grade=grade,
                    label=label,
                )
            )

            # Add to overall score
            overall_score += final_score * weight

        overall_score = round(overall_score, 1)
        overall_grade, overall_label = get_grade_and_label(overall_score)

        return ScanScore(
            overall_score=overall_score,
            overall_grade=overall_grade,
            overall_label=overall_label,
            dimensions=dimension_scores,
        )
