# Phase 5 — Adversarial verification prototype

The deterministic campaign injects four negative cases into the Phase 1 assurance evaluator:

1. Remove a referenced evidence record.
2. Mark referenced evidence as unverified.
3. Mark referenced evidence as contradictory.
4. Fail a policy rule.

Each case must result in `blocked` with the expected reason. A repeated baseline assessment must have the same SHA-256 input digest. A passing campaign is labeled `review_required` and **never** authorizes clinical action.

## What this does not do

This is a small mutation-testing harness for the local deterministic evaluator. It does not red-team a generative AI model, test hallucinations, detect implicit clinical contradictions, prove formal correctness, establish model robustness, or validate clinical safety. No patient data or live clinical use is permitted.

## Next steps

Add independent test oracles, property-based tests, fuzzing, threat scenarios, source integrity checks, coverage reporting, reviewer sign-off, and clinical evaluation protocols before any production consideration.
