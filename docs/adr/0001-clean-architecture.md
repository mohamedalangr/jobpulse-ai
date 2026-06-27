# ADR 0001: Clean Architecture

**Date**: 2026-06-27
**Status**: Accepted

## Context
JobPulse AI requires a robust backend architecture that can scale, adapt to changing machine learning models, and remain highly testable. Traditional layered architectures often couple business logic to database ORMs or HTTP frameworks, making it extremely difficult to swap out persistence layers or test the domain without spinning up a database.

## Decision
We adopted **Clean Architecture** combined with **Domain-Driven Design (DDD)** concepts. The application is strictly segmented into four concentric layers:
1. **Domain Layer**: Houses pure Python business entities (e.g., `JobPosting`, `CandidateProfile`). No external imports allowed.
2. **Application Layer**: Contains Use Cases and orchestrates workflows. Interfaces with infrastructure via abstract interfaces.
3. **Intelligence / Processing Layer**: Implementations of external services (e.g., FAISS embeddings, remote API fetching).
4. **API / Dashboard Layer**: The HTTP ingress (FastAPI) and reference UI (Streamlit).

## Consequences
**Positive**:
- The domain is 100% unit testable without mocks.
- The UI and HTTP controllers are completely decoupled from ML inference implementations.
- Architecture tests can easily verify boundary compliance (`pytest-archon`).

**Negative**:
- Increased upfront boilerplate. Entities must be mapped into DTOs and SQLAlchemy Models repeatedly.
- Steeper learning curve for junior contributors unfamiliar with dependency inversion.
