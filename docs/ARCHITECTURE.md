# HospitalOS | TECT architecture (Phase 1)

## Scope
This repository currently implements a deterministic **prototype** assurance evaluator.
It is not an EHR, clinical decision support system, HIPAA-compliant service, or medical device.

## Pipeline
Claim -> evidence reference resolution -> evidence quality flags -> policy rules -> fail-closed assessment -> reproducible SHA-256 digest.

## Safety boundaries
- Only synthetic, non-patient inputs are permitted.
- No AI output is automatically authorized for clinical use.
- All successful evaluations return `review_required`, never `approved`.
- Missing, contradictory, or unverified evidence blocks an assessment.
- The local API has no authentication, persistence, or PHI safeguards and MUST NOT be publicly exposed.

## Roadmap
1. Typed API schemas, robust validation, threat modeling, security tests.
2. Immutable provenance and tamper-evident audit storage.
3. FHIR adapters with data minimization and access-control enforcement.
4. Knowledge graph, evidence versioning, and policy-as-code.
5. Adversarial testing harness and model evaluation.
6. Human review workflows and approval segregation.
7. Operational digital twin using synthetic datasets.
8. Independent clinical safety, privacy, and regulatory assessments before any clinical deployment.
