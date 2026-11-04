"""In-memory evidence provenance graph for synthetic, non-clinical claims.

No PHI storage, persistence, inference, or clinical authorization.
"""
from dataclasses import dataclass
from hashlib import sha256
import json
import re

IDENTIFIER = re.compile(r"^[A-Za-z0-9._-]{1,100}$")
KINDS = frozenset({"claim", "evidence", "source"})
RELATIONS = frozenset({"supports", "contradicts", "derived_from"})


class GraphError(ValueError):
    pass


@dataclass(frozen=True)
class Node:
    id: str
    kind: str
    label: str
    provenance: str


@dataclass(frozen=True)
class Edge:
    source: str
    target: str
    relation: str


@dataclass(frozen=True)
class Trace:
    claim_id: str
    supporting_evidence: tuple[str, ...]
    contradicting_evidence: tuple[str, ...]
    source_ids: tuple[str, ...]
    unresolved_evidence: tuple[str, ...]
    status: str
    digest: str


class EvidenceGraph:
    def __init__(self):
        self._nodes: dict[str, Node] = {}
        self._edges: set[Edge] = set()

    def add_node(self, node: Node) -> None:
        if not isinstance(node, Node) or not IDENTIFIER.fullmatch(node.id):
            raise GraphError("Invalid node identifier")
        if node.kind not in KINDS or not node.label.strip() or not node.provenance.strip():
            raise GraphError("Node kind, label and provenance required")
        if node.id in self._nodes:
            raise GraphError("Duplicate node identifier")
        self._nodes[node.id] = node

    def add_edge(self, edge: Edge) -> None:
        if not isinstance(edge, Edge) or edge.relation not in RELATIONS:
            raise GraphError("Invalid relationship")
        if edge.source not in self._nodes or edge.target not in self._nodes:
            raise GraphError("Both endpoints must exist")
        origin, target = self._nodes[edge.source], self._nodes[edge.target]
        if edge.relation in {"supports", "contradicts"}:
            if origin.kind != "evidence" or target.kind != "claim":
                raise GraphError("Support/contradiction must connect evidence to claim")
        elif origin.kind != "evidence" or target.kind not in {"evidence", "source"}:
            raise GraphError("Derivation must connect evidence to evidence/source")
        if edge.source == edge.target:
            raise GraphError("Self-reference forbidden")
        if edge in self._edges:
            raise GraphError("Duplicate relationship")
        if edge.relation == "derived_from" and self._would_cycle(edge.source, edge.target):
            raise GraphError("Derivation cycle forbidden")
        self._edges.add(edge)

    def _would_cycle(self, source: str, target: str) -> bool:
        stack = [target]
        seen = set()
        while stack:
            current = stack.pop()
            if current == source:
                return True
            if current in seen:
                continue
            seen.add(current)
            stack.extend(e.target for e in self._edges if e.source == current and e.relation == "derived_from")
        return False

    def trace(self, claim_id: str) -> Trace:
        if claim_id not in self._nodes or self._nodes[claim_id].kind != "claim":
            raise GraphError("Claim not found")
        supporting = sorted(e.source for e in self._edges if e.target == claim_id and e.relation == "supports")
        contradicting = sorted(e.source for e in self._edges if e.target == claim_id and e.relation == "contradicts")
        referenced = set(supporting + contradicting)
        sources: set[str] = set()
        unresolved: set[str] = set()
        for evidence_id in referenced:
            stack = [evidence_id]
            visited = set()
            reached_source = False
            while stack:
                current = stack.pop()
                if current in visited:
                    continue
                visited.add(current)
                if self._nodes[current].kind == "source":
                    sources.add(current)
                    reached_source = True
                stack.extend(e.target for e in self._edges if e.source == current and e.relation == "derived_from")
            if not reached_source:
                unresolved.add(evidence_id)
        status = ("blocked" if contradicting or unresolved or not supporting else "review_required")
        payload = {
            "claim": claim_id,
            "nodes": [vars(self._nodes[n]) for n in sorted(self._nodes)],
            "edges": [vars(e) for e in sorted(self._edges, key=lambda e: (e.source, e.target, e.relation))],
        }
        digest = sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
        return Trace(claim_id, tuple(supporting), tuple(contradicting),
                     tuple(sorted(sources)), tuple(sorted(unresolved)), status, digest)
