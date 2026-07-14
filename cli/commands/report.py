"""
Report command.
"""

import typer
from rich.console import Console

app = typer.Typer()
console = Console()

@app.command("view")
def view_report(
    report_id: str = typer.Argument(..., help="Report ID to view (Connected Mode only)")
) -> None:
    console.print(f"Fetching report {report_id} via API...")
    console.print("Not implemented yet.")
