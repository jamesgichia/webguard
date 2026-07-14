"""
Handles printing of scan results to the console.
"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from engine.models import ScanReport


def print_scan_results(report: ScanReport, console: Console) -> None:
    """Prints the scan report summary to the terminal."""
    console.print(
        Panel(f"WebGuard Scan Results: {report.target_url}", style="bold green")
    )

    # Overall Score
    console.print(
        f"Overall Score: [bold]{report.score.overall_score}/10.0[/bold] (Grade: {report.score.overall_grade})"
    )

    # Dimensions Table
    table = Table(title="Dimensions")
    table.add_column("Dimension", style="cyan")
    table.add_column("Score", style="magenta")
    table.add_column("Grade", style="green")

    for dim in report.score.dimensions:
        table.add_row(dim.dimension, str(dim.score), dim.grade)

    console.print(table)

    # Findings
    console.print("\n[bold red]Findings:[/bold red]")
    findings_count = 0
    for res in report.results:
        if not res.passed:
            findings_count += 1
            color = "red"
            if res.severity in ("LOW", "INFO"):
                color = "yellow"
            console.print(
                f"- [[bold {color}]{res.severity}[/bold {color}]] {res.title} ({res.dimension})"
            )
            
    if findings_count == 0:
        console.print("[green]No vulnerabilities found![/green]")
