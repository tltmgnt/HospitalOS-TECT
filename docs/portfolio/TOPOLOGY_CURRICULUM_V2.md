# Topology compatibility and curriculum v2 — HospitalOS-TECT

Version 2 adapts the explicit-molecular-graph teaching pattern to this repository's actual role. This is documentation and a learning/decision framework; it introduces no mathematical engine, runtime dependency or operational permission.

## Repository decision

| Question | Repository-specific answer |
| --- | --- |
| Architectural role | application |
| Minimum useful mathematics | Typed evidence graphs and finite-state review logic |
| Relationships to preserve | Claims, evidence IDs, rule outcomes and assessment reasons |
| Concrete operation / capstone | Remove required evidence and explain the resulting assessment without making a clinical inference |
| Necessity and scope boundary | No manifold, digital twin or clinical validity is established by this assurance prototype |

The decision is a source-based recommendation, not measured proof that a new specialty improves this repository. Start with the existing implementation and compare any proposed abstraction against a simpler alternative.

## Six-criterion compatibility scorecard

Complete one scorecard per proposed candidate and per concrete operation. Leave unmeasured entries unknown. Scores are human judgments from 0 (no fit) to 5 (strong evidenced fit); unknown is not zero. Do not sum an incomplete card. A total out of 30 is a heuristic, not adoption approval, and feasibility or necessity can veto a high total.

| Criterion | Score | Required evidence |
| --- | --- | --- |
| Structural compatibility | Not yet scored | Map the repository objects and the relationships above without losing direction, labels, units or missingness. |
| Transformation support | Not yet scored | Demonstrate the capstone operation on accepted and rejected inputs. |
| Invariant preservation | Not yet scored | State the property preserved and supply a counterexample or perturbation. |
| Computational feasibility | Not yet scored | Measure size, time and memory on bounded fixtures; record limits. |
| Integration compatibility | Not yet scored | Verify existing schemas, APIs and neighboring contracts remain compatible. |
| Mathematical necessity | Not yet scored | Compare with typed evidence graphs and finite-state review logic and explain the additional capability, if any. |

## Curriculum

Prerequisites: basic programming, sets, functions and graph vocabulary. Work in six competency-gated sessions, approximately 60–90 minutes each; empirical evaluation is a separate research activity.

| Session | Learning objective | Exercise | Completion evidence |
| --- | --- | --- | --- |
| 1. Model | Identify claims, evidence ids, rule outcomes and assessment reasons. | Draw a minimal valid example and one excluded relationship. | Annotated object/relation inventory with explicit assumptions. |
| 2. Contract | Distinguish schema validity from substantive correctness. | Trace validation and propose malformed, missing and boundary inputs. | Input-to-rejection table grounded in current source. |
| 3. Operation | Explain typed evidence graphs and finite-state review logic. | Remove required evidence and explain the resulting assessment without making a clinical inference. | Hand trace compared with existing software, or a clearly labeled specification when no runtime exists. |
| 4. Preservation | State what a transformation must preserve. | Rename identifiers, reorder records, then alter one meaningful relation; predict each effect under the actual contract. | Separate invariant, expected change and unsupported transformation. |
| 5. Comparison | Justify mathematical necessity and cost. | Complete the six-criterion card for the existing approach and one proposed alternative; record unknowns honestly. | Evidence-backed recommendation with baseline and explicit veto conditions. |
| 6. Reproduction | Communicate the bounded result. | Reproduce the capstone using existing offline fixtures and record software version, inputs, outputs and limitations. | Reviewable notebook or report distinguishing computation, replay, independent evaluation and authorization. |

## Source-linked reading laboratory

The table is a guided selection of source lines, not an assertion that the whole repository is covered. Line numbers refer to the inspected source blob `a23e9f0152cbf416bf2f06f795864141328f5953` in [src/hospitalos_tect/assurance.py](../../src/hospitalos_tect/assurance.py). Recheck anchors after source changes.

| Line | Statement | Learning check |
| --- | --- | --- |
| [12](../../src/hospitalos_tect/assurance.py#L12) | `class Claim:` | State the input/output contract and trace one normal and one failing case. |
| [19](../../src/hospitalos_tect/assurance.py#L19) | `class Evidence:` | State the input/output contract and trace one normal and one failing case. |
| [27](../../src/hospitalos_tect/assurance.py#L27) | `class Rule:` | State the input/output contract and trace one normal and one failing case. |
| [34](../../src/hospitalos_tect/assurance.py#L34) | `class Assessment:` | State the input/output contract and trace one normal and one failing case. |
| [44](../../src/hospitalos_tect/assurance.py#L44) | `def assess(claim: Claim, evidence: list[Evidence], rules: list[Rule]) -> Assessment:` | State the input/output contract and trace one normal and one failing case. |
| [52](../../src/hospitalos_tect/assurance.py#L52) | `raise ValueError("Claim id and text are required")` | Construct the triggering input and explain why rejection preserves the contract. |
| [54](../../src/hospitalos_tect/assurance.py#L54) | `raise ValueError("Duplicate evidence references")` | Construct the triggering input and explain why rejection preserves the contract. |
| [56](../../src/hospitalos_tect/assurance.py#L56) | `raise ValueError("Duplicate evidence ids")` | Construct the triggering input and explain why rejection preserves the contract. |
| [58](../../src/hospitalos_tect/assurance.py#L58) | `raise ValueError("Duplicate rule ids")` | Construct the triggering input and explain why rejection preserves the contract. |
| [86](../../src/hospitalos_tect/assurance.py#L86) | `return Assessment(` | Predict the returned value and distinguish a computed result from authorization. |
## Assessment and verification

A learner must explain the model, trace the capstone, identify a counterexample and state the scope boundary. Assess these four competencies equally; a numerical score cannot compensate for an unsupported scientific or operational claim.

Relevant existing checks:

- [tests/test_assurance.py](../../tests/test_assurance.py)

Follow [README](../../README.md) for environment and installed-package instructions. Read scripts before execution; source-reading exercises do not authorize provider calls, model downloads, live orders, hardware actions or messages. Synthetic fixtures establish software behavior only. This documentation change does not report those exercises as already executed.

## Interoperability and adoption gate

Retain explicit domain contracts. Shared assurance records should refer to domain evidence and its assumptions rather than relabeling graph reachability, homology, statistical calibration and epistemic acceptance as interchangeable quantities. The canonical ResearchOs controller remains owned by ResearchOs; this curriculum does not create another controller fork.

Adopt additional mathematics only after a versioned experiment demonstrates a useful operation, the scorecard has evidence, the simpler baseline is inadequate and existing conformance checks remain satisfied. No manifold, digital twin or clinical validity is established by this assurance prototype.
