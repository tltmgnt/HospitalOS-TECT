# Phase 4 — Evidence knowledge graph prototype

The in-memory graph supports three node types (`claim`, `evidence`, `source`) and three directed relationships (`supports`, `contradicts`, `derived_from`).

## Trace semantics
- A claim requires supporting evidence with a derivation path to a source.
- Contradictory evidence, missing provenance, or absent support produces `blocked`.
- A fully linked claim returns `review_required`, **never** approved.
- Directed derivation cycles and invalid edge types are rejected.
- SHA-256 digest is deterministic for the current graph snapshot.

## Limitations
This is a structural provenance check only. A source node does not establish that a source is credible or scientifically correct. Contradictions are explicitly recorded by callers, not inferred by AI. The graph is in-memory only; it has no persistence, authentication, tenant isolation, or PHI protections. It must only be used with synthetic, non-patient data.

## Next
Add immutable source versioning, typed evidence metadata, external integrity verification, scoped storage, policy evaluation, and human review. Independent security and clinical evaluation are required before production use.
