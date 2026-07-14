"""
Generates JSON, HTML, and PDF reports from scan results.
"""

import dataclasses
import json
import os
from datetime import datetime

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

from engine.models import ScanReport


class Reporter:
    """
    Handles report generation in multiple formats (JSON, HTML, PDF).
    """

    def __init__(self, templates_dir: str = "reports/templates") -> None:
        # Ensure templates directory exists and setup Jinja environment
        os.makedirs(templates_dir, exist_ok=True)
        self.env = Environment(loader=FileSystemLoader(templates_dir))

    def generate_json(self, report: ScanReport) -> str:
        """Generates a JSON string representing the scan report."""
        return json.dumps(dataclasses.asdict(report), indent=2)

    def generate_html(self, report: ScanReport) -> str:
        """Generates an HTML string representing the scan report."""
        template = self.env.get_template("report_html.html.j2")
        return template.render(report=report)

    def generate_pdf(self, report: ScanReport, output_path: str) -> None:
        """Generates a PDF report and writes it to the specified path."""
        template = self.env.get_template("report_pdf.html.j2")
        html_content = template.render(report=report)
        HTML(string=html_content).write_pdf(output_path)
