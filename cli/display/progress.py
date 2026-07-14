"""
Handles progress spinners for the CLI.
"""

import asyncio
from typing import Any, Coroutine

from rich.progress import Progress, SpinnerColumn, TextColumn


def run_with_progress(coro: Coroutine[Any, Any, Any], description: str = "Processing...") -> Any:
    """
    Runs an asynchronous coroutine while displaying a Rich progress spinner.
    """
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description=description, total=None)

        loop = asyncio.get_event_loop()
        return loop.run_until_complete(coro)
