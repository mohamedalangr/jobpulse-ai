# ADR 0004: FAISS as the Initial Vector Store

**Date**: 2026-06-27
**Status**: Accepted

## Context
After calculating embeddings, we need to perform nearest-neighbor searches across millions of job descriptions efficiently. Full-blown vector databases (ChromaDB, Pinecone, Qdrant) introduce heavy operational complexity during local development and CI/CD.

## Decision
We integrated **Meta's FAISS** as an embedded, in-memory vector store backed by file-system persistence. 

## Consequences
- **Positive**: Sub-10ms search latency without deploying an additional database container. Highly portable (stored in `embeddings/`).
- **Negative**: Lacks native distributed scaling out-of-the-box. As dataset size breaches RAM capacity, we will eventually need to migrate to a dedicated vector database.
