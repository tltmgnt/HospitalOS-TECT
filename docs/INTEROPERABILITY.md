# Phase 3 — Synthetic FHIR subset

## Scope
The `fhir.py` module validates a deliberately restricted, FHIR R4-inspired subset of Patient, Encounter, Observation and collection Bundle resources.

**Not FHIR conformance:** This is not an HL7-certified or complete FHIR validator, not a FHIR server, and does not connect to an EHR. No live clinical data may be processed.

## Allowed fields
- Patient: resourceType, id, meta, active
- Encounter: resourceType, id, meta, status, subject
- Observation: resourceType, id, meta, status, subject, code

Every id must begin with `synthetic-` and every resource must have the exact `synthetic` meta tag. All other fields, including demographics, identifiers, measurements and notes, are rejected. Bundle references must resolve to synthetic patients within the same bundle.

## Next
Add complete FHIR R4 schema validation in a separately reviewed service; define consent and authorization models, terminology bindings, resource provenance, threat modeling, secure transport and audit logs before any real-world EHR integration.
