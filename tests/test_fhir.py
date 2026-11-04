import unittest
from hospitalos_tect.fhir import FHIRValidationError, validate_synthetic_bundle, validate_synthetic_resource


TAG = {"tag": [{"system": "https://hospitalos-tect.example/tags", "code": "synthetic"}]}
PATIENT = {"resourceType": "Patient", "id": "synthetic-p1", "meta": TAG, "active": True}
ENCOUNTER = {"resourceType": "Encounter", "id": "synthetic-e1", "meta": TAG, "status": "finished", "subject": {"reference": "Patient/synthetic-p1"}}
OBSERVATION = {"resourceType": "Observation", "id": "synthetic-o1", "meta": TAG, "status": "final", "subject": {"reference": "Patient/synthetic-p1"}, "code": {"text": "synthetic-operational-signal"}}


class FHIRTests(unittest.TestCase):
    def test_patient(self):
        self.assertEqual(validate_synthetic_resource(PATIENT).resource_type, "Patient")

    def test_bundle(self):
        bundle = {"resourceType": "Bundle", "type": "collection", "entry": [{"resource": x} for x in (PATIENT, ENCOUNTER, OBSERVATION)]}
        self.assertEqual(len(validate_synthetic_bundle(bundle)), 3)

    def test_reject_real_identifier(self):
        with self.assertRaises(FHIRValidationError):
            validate_synthetic_resource({**PATIENT, "id": "real-p1"})

    def test_reject_demographics(self):
        with self.assertRaises(FHIRValidationError):
            validate_synthetic_resource({**PATIENT, "name": [{"family": "Doe"}]})

    def test_reject_missing_synthetic_tag(self):
        with self.assertRaises(FHIRValidationError):
            validate_synthetic_resource({**PATIENT, "meta": {}})

    def test_reject_unresolved_reference(self):
        bundle = {"resourceType": "Bundle", "type": "collection", "entry": [{"resource": ENCOUNTER}]}
        with self.assertRaises(FHIRValidationError):
            validate_synthetic_bundle(bundle)

    def test_reject_duplicate(self):
        bundle = {"resourceType": "Bundle", "type": "collection", "entry": [{"resource": PATIENT}, {"resource": PATIENT}]}
        with self.assertRaises(FHIRValidationError):
            validate_synthetic_bundle(bundle)

    def test_reject_clinical_value(self):
        with self.assertRaises(FHIRValidationError):
            validate_synthetic_resource({**OBSERVATION, "valueQuantity": {"value": 99}})


if __name__ == "__main__":
    unittest.main()
