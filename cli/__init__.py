"""
WebGuard CLI tool.

Provides the `webguard` command with two operating modes (ADR-001):

  Offline mode (default):
    Calls the core engine directly in-process.
    No API dependency. No authentication required.
    Results output to terminal or local file.

  Connected mode (--api-key flag):
    Calls the FastAPI backend via HTTP using an API key.
    Scan history stored in the database.
    Results accessible from the web dashboard.

Entry point: cli.main:app (registered in pyproject.toml)
"""

__version__ = "1.0.0"
