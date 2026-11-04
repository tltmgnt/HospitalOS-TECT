"""Run with PYTHONPATH=src python examples/evidence_graph.py."""
from dataclasses import asdict
import json
from hospitalos_tect.graph import Edge, EvidenceGraph, Node

graph = EvidenceGraph()
graph.add_node(Node("claim-1", "claim", "Synthetic occupancy report", "generated-demo"))
graph.add_node(Node("evidence-1", "evidence", "Synthetic occupancy count", "generated-demo"))
graph.add_node(Node("source-1", "source", "Synthetic dataset v1", "generated-demo"))
graph.add_edge(Edge("evidence-1", "claim-1", "supports"))
graph.add_edge(Edge("evidence-1", "source-1", "derived_from"))
print(json.dumps(asdict(graph.trace("claim-1")), indent=2))
