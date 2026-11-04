"""Deterministic, non-clinical evidence assurance prototype.

This is NOT a medical decision support or medical-device implementation.
"""
from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
import json


@dataclass(frozen=True)
class Claim:
    id: str
    text: str
    evidence_ids: tuple[str, ...]


@dataclass(frozen=True)
class Evidence:
    id: str
    source: str
    supports: bool
    verified: bool


@dataclass(frozen=True)
class Rule:
    id: str
    description: str
    passed: bool


@dataclass(frozen=True)
class Assessment:
    claim_id: str
    status: str
    reasons: tuple[str, ...]
    evidence_ids: tuple[str, ...]
    rule_ids: tuple[str, ...]
    digest: str
    assessed_at: str


def assess(claim: Claim, evidence: list[Evidence], rules: list[Rule]) -> Assessment:
    """Fail closed for missing evidence, contradictions, or failed rules.

    The digest covers deterministic inputs, not timestamps; this permits
    comparison across repeated assessments. 'review_required' is never an
    authorization for clinical action.
    """
    if not claim.id or not claim.text.strip():
        raise ValueError("Claim id and text are required")
    if len(set(claim.evidence_ids)) != len(claim.evidence_ids):
        raise ValueError("Duplicate evidence references")
    if len({e.id for e in evidence}) != len(evidence):
        raise ValueError("Duplicate evidence ids")
    if len({r.id for r in rules}) != len(rules):
        raise ValueError("Duplicate rule ids")

    by_id = {e.id: e for e in evidence}
    reasons = []
    if not claim.evidence_ids:
        reasons.append("no_evidence")
    for evidence_id in claim.evidence_ids:
        item = by_id.get(evidence_id)
        if item is None:
            reasons.append(f"missing_evidence:{evidence_id}")
        elif not item.verified:
            reasons.append(f"unverified_evidence:{evidence_id}")
        elif not item.supports:
            reasons.append(f"contradictory_evidence:{evidence_id}")
    if not rules:
        reasons.append("no_rules")
    for rule in rules:
        if not rule.passed:
            reasons.append(f"failed_rule:{rule.id}")
    # This prototype never returns a clinical approval status.
    status = "review_required" if not reasons else "blocked"
    payload = {
        "claim": {"id": claim.id, "text": claim.text, "evidence_ids": claim.evidence_ids},
        "evidence": [vars(e) for e in sorted(evidence, key=lambda e: e.id)],
        "rules": [vars(r) for r in sorted(rules, key=lambda r: r.id)],
        "reasons": reasons,
    }
    digest = sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
    return Assessment(
        claim_id=claim.id, status=status, reasons=tuple(reasons),
        evidence_ids=claim.evidence_ids,
        rule_ids=tuple(r.id for r in rules), digest=digest,
        assessed_at=datetime.now(timezone.utc).isoformat(),
    )
