"""
Tests for the report generator.
"""

import json
import os
import tempfile
from datetime import datetime

from engine.models import (
    CheckResult,
    Dimension,
    DimensionScore,
    ScanReport,
    ScanScore,
    Severity,
)
from engine.reporter import Reporter


def test_reporter_json() -> None:
    reporter = Reporter(templates_dir="reports/templates")
    score = ScanScore(
        overall_score=8.5,
        overall_grade="B",
        overall_label="Good",
        dimensions=[
            DimensionScore(
                dimension=Dimension.TRANSPORT_SECURITY.value,
                score=8.5,
                weight=0.25,
                grade="B",
                label="Good",
            )
        ],
    )
    report = ScanReport(
        target_url="https://example.com",
        scan_time_utc="2026-07-14T10:00:00Z",
        score=score,
        results=[],
    )

    json_str = reporter.generate_json(report)
    data = json.loads(json_str)
    assert data["target_url"] == "https://example.com"
    assert data["score"]["overall_score"] == 8.5


def test_reporter_html() -> None:
    reporter = Reporter(templates_dir="reports/templates")
    score = ScanScore(
        overall_score=8.5,
        overall_grade="B",
        overall_label="Good",
        dimensions=[],
    )
    report = ScanReport(
        target_url="https://example.com",
        scan_time_utc="2026-07-14T10:00:00Z",
        score=score,
        results=[],
    )

    html_str = reporter.generate_html(report)
    assert "https://example.com" in html_str
    assert "8.5 / 10.0" in html_str


def test_reporter_pdf() -> None:
    reporter = Reporter(templates_dir="reports/templates")
    score = ScanScore(
        overall_score=8.5,
        overall_grade="B",
        overall_label="Good",
        dimensions=[],
    )
    report = ScanReport(
        target_url="https://example.com",
        scan_time_utc="2026-07-14T10:00:00Z",
        score=score,
        results=[],
    )

    with tempfile.TemporaryDirectory() as temp_dir:
        pdf_path = os.path.join(temp_dir, "report.pdf")
        reporter.generate_pdf(report, pdf_path)
        assert os.path.exists(pdf_path)
        assert os.path.getsize(pdf_path) > 0
