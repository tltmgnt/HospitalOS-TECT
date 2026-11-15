import unittest
from hospitalos_tect import Claim, Evidence, Rule
from hospitalos_tect.adversarial import run_campaign


class AdversarialTests(unittest.TestCase):
    def setUp(self):
        self.claim = Claim("synthetic-c1", "Synthetic operational claim", ("ev1",))
        self.evidence = [Evidence("ev1", "synthetic-dataset", True, True)]
        self.rules = [Rule("r1", "Synthetic approval gate", True)]

    def test_all_four_negative_challenges_detected(self):
        result = run_campaign(self.claim, self.evidence, self.rules)
        self.assertEqual(result.status, "review_required")
        self.assertEqual(len(result.challenges), 4)
        self.assertTrue(all(c.detected for c in result.challenges))

    def test_baseline_failure_blocks(self):
        result = run_campaign(self.claim, [], self.rules)
        self.assertEqual(result.status, "blocked")

    def test_missing_rules_blocks(self):
        result = run_campaign(self.claim, self.evidence, [])
        self.assertEqual(result.status, "blocked")

    def test_reproducibility(self):
        result = run_campaign(self.claim, self.evidence, self.rules)
        self.assertTrue(result.reproducible)
        self.assertEqual(result.digest, run_campaign(self.claim, self.evidence, self.rules).digest)

    def test_unverified_baseline_blocks(self):
        result = run_campaign(self.claim, [Evidence("ev1", "synthetic", True, False)], self.rules)
        self.assertEqual(result.status, "blocked")

    def test_challenge_names(self):
        result = run_campaign(self.claim, self.evidence, self.rules)
        self.assertEqual(
            {c.name for c in result.challenges},
            {"remove_evidence", "unverify_evidence", "contradict_evidence", "fail_rule"},
        )


if __name__ == "__main__":
    unittest.main()
