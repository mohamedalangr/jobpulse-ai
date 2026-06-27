# ADR 0005: CQRS for the Application Layer

**Date**: 2026-06-27
**Status**: Accepted

## Context
Our API needs to handle both heavy analytical computations (e.g., generating learning plans) and state-mutating ingestion processes. A single monolithic Service class doing both violates the Single Responsibility Principle and muddies intent.

## Decision
We adopted a lightweight **Command / Query Responsibility Segregation (CQRS)** pattern for application logic. 
- **Commands**: Modify state, emit events, orchestrate updates.
- **Queries**: Never modify state, strictly handle fast data retrieval.

## Consequences
- The application layer is strictly segregated and easily searchable. 
- Queries can eventually bypass the Domain layer entirely to perform highly optimized raw SQL reads if performance demands it.
- Command Handlers are isolated and unit-testable.
