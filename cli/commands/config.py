"""
Config command.
"""

import typer
from rich.console import Console

app = typer.Typer()
console = Console()


@app.command("show")
def show_config() -> None:
    console.print("Current configuration:")
    console.print("API Key: [red]Not configured[/red]")
