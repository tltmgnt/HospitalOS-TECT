"""Deterministic adversarial challenges for synthetic assurance assessments.

A challenge passing means the evaluator blocked the mutation, not that a
clinical model is safe or validated.
"""
from dataclasses import dataclass
from hashlib import sha256
import json

from .assurance import Claim, Evidence, Rule, assess


@dataclass(frozen=True)
class ChallengeResult:
    name: str
    detected: bool
    observed_status: str
    reasons: tuple[str, ...]


@dataclass(frozen=True)
class Campaign:
    baseline_status: str
    baseline_digest: str
    reproducible: bool
    challenges: tuple[ChallengeResult, ...]
    status: str
    digest: str


def run_campaign(claim: Claim, evidence: list[Evidence], rules: list[Rule]) -> Campaign:
    """Run controlled negative cases and fail closed if any is not detected.

    Baseline must be structurally valid and have a review_required result.
    No campaign result authorizes clinical use.
    """
    baseline = assess(claim, evidence, rules)
    repeat = assess(claim, evidence, rules)
    reproducible = baseline.digest == repeat.digest
    challenges: list[ChallengeResult] = []

    def check(name: str, modified_claim: Claim, modified_evidence: list[Evidence],
              modified_rules: list[Rule], expected_reason: str) -> None:
        outcome = assess(modified_claim, modified_evidence, modified_rules)
        challenges.append(ChallengeResult(
            name, outcome.status == "blocked" and expected_reason in outcome.reasons,
            outcome.status, outcome.reasons,
        ))

    if claim.evidence_ids:
        selected = claim.evidence_ids[0]
        check("remove_evidence", claim, [e for e in evidence if e.id != selected],
              rules, f"missing_evidence:{selected}")
        check("unverify_evidence", claim,
              [Evidence(e.id, e.source, e.supports, False) if e.id == selected else e for e in evidence],
              rules, f"unverified_evidence:{selected}")
        check("contradict_evidence", claim,
              [Evidence(e.id, e.source, False, True) if e.id == selected else e for e in evidence],
              rules, f"contradictory_evidence:{selected}")
    else:
        challenges.append(ChallengeResult("missing_baseline_evidence", False, baseline.status, baseline.reasons))

    if rules:
        first = rules[0]
        check("fail_rule", claim,
              evidence, [Rule(r.id, r.description, False) if r.id == first.id else r for r in rules],
              f"failed_rule:{first.id}")
    else:
        challenges.append(ChallengeResult("missing_baseline_rules", False, baseline.status, baseline.reasons))

    status = ("review_required" if baseline.status == "review_required"
              and reproducible and all(c.detected for c in challenges) else "blocked")
    payload = {
        "baseline_digest": baseline.digest,
        "baseline_status": baseline.status,
        "reproducible": reproducible,
        "challenges": [
            {"name": c.name, "detected": c.detected,
             "observed_status": c.observed_status, "reasons": c.reasons}
            for c in challenges
        ],
        "status": status,
    }
    digest = sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
    return Campaign(baseline.status, baseline.digest, reproducible,
                    tuple(challenges), status, digest)
