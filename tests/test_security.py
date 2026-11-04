import os
import unittest
from unittest.mock import patch
from hospitalos_tect.security import Principal, authenticate, permitted


class SecurityTests(unittest.TestCase):
    def test_missing_configuration_denies(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertIsNone(authenticate("Bearer " + "x" * 32))

    def test_short_secret_denies(self):
        with patch.dict(os.environ, {"HOSPITALOS_DEV_TOKEN": "short"}):
            self.assertIsNone(authenticate("Bearer short"))

    def test_correct_token(self):
        token = "a" * 32
        with patch.dict(os.environ, {"HOSPITALOS_DEV_TOKEN": token}):
            self.assertIsNotNone(authenticate("Bearer " + token))
            self.assertIsNone(authenticate("Bearer " + "b" * 32))

    def test_tenant_isolation(self):
        principal = Principal("tenant-a", "dev", frozenset({"assurance:assess"}))
        self.assertTrue(permitted(principal, "tenant-a", "assurance:assess"))
        self.assertFalse(permitted(principal, "tenant-b", "assurance:assess"))

    def test_role_required(self):
        principal = Principal("tenant-a", "dev", frozenset())
        self.assertFalse(permitted(principal, "tenant-a", "assurance:assess"))


if __name__ == "__main__":
    unittest.main()
