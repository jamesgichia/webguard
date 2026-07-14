"""
Main entry point for WebGuard CLI.
"""

import typer

from cli.commands import config, report, scan

app = typer.Typer(
    name="webguard",
    help="WebGuard CLI - Passive OWASP Top 10 web vulnerability scanner",
    add_completion=False,
)

app.add_typer(scan.app, name="scan", help="Run security scans against targets.")
app.add_typer(report.app, name="report", help="Generate and view reports.")
app.add_typer(config.app, name="config", help="Manage CLI configuration.")

if __name__ == "__main__":
    app()
