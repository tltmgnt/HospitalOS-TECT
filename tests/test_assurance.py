import unittest
from hospitalos_tect import Claim, Evidence, Rule, assess


class AssuranceTests(unittest.TestCase):
    def setUp(self):
        self.claim = Claim("claim-1", "Synthetic operations claim", ("ev-1",))
        self.evidence = [Evidence("ev-1", "synthetic-source", True, True)]
        self.rules = [Rule("r-1", "Synthetic policy", True)]

    def test_review_required_never_approved(self):
        result = assess(self.claim, self.evidence, self.rules)
        self.assertEqual(result.status, "review_required")
        self.assertFalse(result.reasons)

    def test_missing_evidence_blocks(self):
        result = assess(self.claim, [], self.rules)
        self.assertEqual(result.status, "blocked")
        self.assertIn("missing_evidence:ev-1", result.reasons)

    def test_failed_rule_blocks(self):
        result = assess(self.claim, self.evidence, [Rule("r-1", "Synthetic policy", False)])
        self.assertIn("failed_rule:r-1", result.reasons)

    def test_unverified_blocks(self):
        result = assess(self.claim, [Evidence("ev-1", "source", True, False)], self.rules)
        self.assertEqual(result.status, "blocked")

    def test_digest_is_reproducible(self):
        self.assertEqual(
            assess(self.claim, self.evidence, self.rules).digest,
            assess(self.claim, self.evidence, self.rules).digest,
        )

    def test_no_rules_blocks(self):
        self.assertEqual(assess(self.claim, self.evidence, []).status, "blocked")


if __name__ == "__main__":
    unittest.main()
