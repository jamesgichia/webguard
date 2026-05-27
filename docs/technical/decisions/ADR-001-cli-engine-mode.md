# ADR-001: CLI Tool Operating Modes

**Date:** May 2026
**Status:** Accepted
**Author:** James Gichia

## Context

The CLI tool needs to run scans. Two possible approaches exist:
calling the core engine directly or calling the REST API.
Both approaches serve different user needs.

## Decision

The CLI tool operates in two modes:

**Offline Mode (default)**
The CLI calls the core engine directly.
No API dependency. No network requirement beyond the target URL.
Results output to terminal or local file.
No scan history stored.

**Connected Mode (--api-key flag)**
The CLI calls the REST API using an API key.
Scan history stored in the database.
Results accessible from the web dashboard.
Requires API to be running and reachable.

## Rationale

Primary user Daniel needs pipeline integration that works
without external service dependencies. Offline mode serves him.

Secondary user Amara needs scan history and web dashboard
access. Connected mode serves her.

Option C serves both without forcing either to compromise.

## Alternatives Considered

Option A — CLI calls engine only
Rejected: No path to scan history for CLI users.

Option B — CLI calls API only
Rejected: Breaks CI/CD pipelines when API is unavailable.
Introduces unnecessary latency for local development use.

## Consequences

The CLI codebase must handle both code paths cleanly.
The engine must be callable both directly and via the API worker.
Documentation must clearly explain both modes to users.
