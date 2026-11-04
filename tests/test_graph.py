import unittest
from hospitalos_tect.graph import Edge, EvidenceGraph, GraphError, Node


def sample():
    graph = EvidenceGraph()
    for node in (
        Node("claim-1", "claim", "Synthetic capacity report", "demo"),
        Node("ev-1", "evidence", "Synthetic observation", "demo"),
        Node("src-1", "source", "Generated test data", "demo"),
    ):
        graph.add_node(node)
    return graph


class GraphTests(unittest.TestCase):
    def test_verified_provenance_requires_review(self):
        graph = sample()
        graph.add_edge(Edge("ev-1", "claim-1", "supports"))
        graph.add_edge(Edge("ev-1", "src-1", "derived_from"))
        trace = graph.trace("claim-1")
        self.assertEqual(trace.status, "review_required")
        self.assertEqual(trace.source_ids, ("src-1",))

    def test_missing_provenance_blocks(self):
        graph = sample()
        graph.add_edge(Edge("ev-1", "claim-1", "supports"))
        self.assertEqual(graph.trace("claim-1").status, "blocked")

    def test_contradiction_blocks(self):
        graph = sample()
        graph.add_edge(Edge("ev-1", "claim-1", "contradicts"))
        graph.add_edge(Edge("ev-1", "src-1", "derived_from"))
        self.assertEqual(graph.trace("claim-1").status, "blocked")

    def test_empty_claim_blocks(self):
        self.assertEqual(sample().trace("claim-1").status, "blocked")

    def test_invalid_direction_rejected(self):
        graph = sample()
        with self.assertRaises(GraphError):
            graph.add_edge(Edge("claim-1", "ev-1", "supports"))

    def test_missing_endpoint_rejected(self):
        graph = sample()
        with self.assertRaises(GraphError):
            graph.add_edge(Edge("missing", "claim-1", "supports"))

    def test_duplicate_node_rejected(self):
        graph = sample()
        with self.assertRaises(GraphError):
            graph.add_node(Node("claim-1", "claim", "Duplicate", "demo"))

    def test_cycle_rejected(self):
        graph = sample()
        graph.add_node(Node("ev-2", "evidence", "Another synthetic observation", "demo"))
        graph.add_edge(Edge("ev-1", "ev-2", "derived_from"))
        with self.assertRaises(GraphError):
            graph.add_edge(Edge("ev-2", "ev-1", "derived_from"))

    def test_digest_stable(self):
        graph = sample()
        graph.add_edge(Edge("ev-1", "claim-1", "supports"))
        graph.add_edge(Edge("ev-1", "src-1", "derived_from"))
        self.assertEqual(graph.trace("claim-1").digest, graph.trace("claim-1").digest)


if __name__ == "__main__":
    unittest.main()
