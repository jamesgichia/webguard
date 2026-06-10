"""
WebGuard scanning engine.

The engine is the core of WebGuard. It is completely independent of any
interface (CLI, API, or web). It receives a ScanTarget, runs all applicable
passive checks concurrently, scores the results, and returns a ScanResult.

Public entry point: engine.orchestrator.run_scan()
"""

__version__ = "1.0.0"
