# ADR 0002: Repository and Unit of Work Patterns

**Date**: 2026-06-27
**Status**: Accepted

## Context
JobPulse AI ingests data from various disparate sources. Directly interacting with the database using SQLAlchemy sessions scattered across the application causes transaction leaks, unpredictable state mutations, and difficult-to-test service boundaries.

## Decision
We abstract all database access behind the **Repository** pattern and coordinate transactions with the **Unit of Work (UoW)** pattern.

## Consequences
- Business logic is completely decoupled from SQLAlchemy `Session` objects.
- Transactions are implicitly committed or rolled back automatically via python context managers (`with uow:`).
- Repositories can easily be mocked for lightning-fast unit tests.
