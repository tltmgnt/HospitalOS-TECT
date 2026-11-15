import unittest
from hospitalos_tect.operations import HospitalSnapshot, evaluate


class OperationsTests(unittest.TestCase):
    def setUp(self):
        self.snapshot = HospitalSnapshot("synthetic-hospital-a", 100, 85, 12, 75.0, 10, 15)

    def test_metrics(self):
        report = evaluate(self.snapshot)
        self.assertEqual(report.occupancy_pct, 85.0)
        self.assertEqual(report.available_beds, 15)
        self.assertEqual(report.projected_occupied, 90)

    def test_scenario(self):
        report = evaluate(self.snapshot, admission_delta=15)
        self.assertEqual(report.projected_occupied, 105)
        self.assertIn("projected_capacity_exceeded", report.flags)

    def test_reproducible_digest(self):
        self.assertEqual(evaluate(self.snapshot).digest, evaluate(self.snapshot).digest)

    def test_bad_capacity(self):
        with self.assertRaises(ValueError):
            evaluate(HospitalSnapshot("synthetic-a", 0, 0, 0, 0, 0, 0))

    def test_no_real_hospital(self):
        with self.assertRaises(ValueError):
            evaluate(HospitalSnapshot("hospital-a", 100, 85, 12, 75, 10, 15))

    def test_no_nan(self):
        with self.assertRaises(ValueError):
            evaluate(HospitalSnapshot("synthetic-a", 100, 85, 12, float("nan"), 10, 15))

    def test_negative_deltas_rejected_when_out_of_bounds(self):
        with self.assertRaises(ValueError):
            evaluate(self.snapshot, admission_delta=-16)

    def test_ed_threshold(self):
        snapshot = HospitalSnapshot("synthetic-a", 100, 85, 12, 130, 10, 15)
        self.assertIn("synthetic_ed_wait_threshold", evaluate(snapshot).flags)


if __name__ == "__main__":
    unittest.main()
