# Security boundaries — Phase 2 prototype

**Not production-ready. Never submit PHI, PII, or real patient information.**

- All assessment requests require a locally configured bearer token (minimum 32 characters).
- No token is configured by default: requests fail closed.
- The only supported tenant is `synthetic-demo`.
- Assessment permission is checked explicitly.
- Server binds to 127.0.0.1; no TLS termination or network exposure is provided.
- Token authentication is intended exclusively for local development. It does not provide enterprise IAM, key rotation, user attribution, or sufficient healthcare security controls.
- Do not place the token in source control, shell history, logs, or shared example files.
- Production prerequisites include OIDC/OAuth2, scoped service identities, per-tenant authorization, PHI minimization, encryption, structured audit logs, abuse controls, threat modeling, penetration testing, and organizational compliance review.
