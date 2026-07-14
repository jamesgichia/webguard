"""
Scan command.
"""

import asyncio
from datetime import datetime, timezone
from typing import Optional

import typer
from rich.console import Console

from cli.display.progress import run_with_progress
from cli.display.results import print_scan_results
from engine.fetcher import fetch_target
from engine.models import ScanReport
from engine.orchestrator import ScanOrchestrator
from engine.reporter import Reporter
from engine.scorer import Scorer

app = typer.Typer()
console = Console()


@app.command("run")
def run_scan(
    url: str = typer.Argument(..., help="Target URL to scan"),
    profile: str = typer.Option(
        "Standard", "--profile", "-p", help="Scan profile: Quick, Standard, Deep"
    ),
    api_key: Optional[str] = typer.Option(
        None, "--api-key", envvar="WEBGUARD_API_KEY", help="API Key for Connected Mode"
    ),
    format_output: str = typer.Option(
        "json", "--format", "-f", help="Output format: json, html, pdf"
    ),
    output: Optional[str] = typer.Option(
        None, "--output", "-o", help="Output file path"
    ),
) -> None:
    if api_key:
        console.print("[blue]Running in CONNECTED mode using API...[/blue]")
        # Connected mode logic goes here (calling the REST API)
        console.print("Connected mode is not fully implemented yet.")
        return

    console.print("[green]Running in OFFLINE mode...[/green]")

    async def _do_scan() -> ScanReport:
        target = await fetch_target(url)
        orchestrator = ScanOrchestrator()
        results = orchestrator.run_all(target)

        scorer = Scorer()
        score = scorer.calculate(results)

        report = ScanReport(
            target_url=target.url,
            scan_time_utc=datetime.now(timezone.utc).isoformat(),
            score=score,
            results=results,
        )
        return report

    report = run_with_progress(_do_scan(), description=f"Scanning {url}...")

    if output:
        reporter = Reporter()
        if format_output == "json":
            with open(output, "w") as f:
                f.write(reporter.generate_json(report))
        elif format_output == "html":
            with open(output, "w") as f:
                f.write(reporter.generate_html(report))
        elif format_output == "pdf":
            reporter.generate_pdf(report, output)
        console.print(f"Report saved to {output}")
    else:
        print_scan_results(report, console)
