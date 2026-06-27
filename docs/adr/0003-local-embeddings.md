# ADR 0003: Local Embeddings over External APIs

**Date**: 2026-06-27
**Status**: Accepted

## Context
Semantic search requires transforming text into vectors. Using an external provider like OpenAI or Cohere imposes high latency per request, massive token costs during batch ingestion, and privacy concerns regarding user data.

## Decision
We adopted **SentenceTransformers** (specifically `all-MiniLM-L6-v2`) running locally inside the API container.

## Consequences
- **Positive**: Zero API costs. Zero latency for network calls. Completely private inference.
- **Negative**: Increased memory footprint inside the API container (requires ~500MB additional RAM). The Docker image size is heavier, requiring multi-stage builds.
