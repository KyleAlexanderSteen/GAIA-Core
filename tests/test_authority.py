#!/usr/bin/env python3
"""Authority lifecycle tests. Expansion cannot sneak through small allows."""
import unittest
from gaia_core.authority import (
    AuthorityBoundary,
    AuthorityError,
    apply_change,
    classify,
    detect_drift,
)

class TestAuthority(unittest.TestCase):
    def setUp(self):
        self.b = AuthorityBoundary("human:1", {"read"})

    def test_routine_stays_inside(self):
        self.assertEqual(classify(self.b, {"read"}), "routine")
        b2, change = apply_change(self.b, {"read"})
        self.assertTrue(change.accepted)
        self.assertEqual(b2.version, 1)
        self.assertEqual(b2.allowed, {"read"})

    def test_expansion_without_reauth_fails(self):
        self.assertEqual(classify(self.b, {"read", "write"}), "expanding")
        with self.assertRaises(AuthorityError):
            apply_change(self.b, {"write"}, reauthorised=False)
        self.assertEqual(self.b.allowed, {"read"})
        self.assertEqual(self.b.version, 1)

    def test_expansion_with_reauth_versions(self):
        b2, change = apply_change(self.b, {"write"}, reauthorised=True, at="2026-10-17T00:00:00Z")
        self.assertTrue(change.accepted)
        self.assertEqual(change.kind, "expanding")
        self.assertEqual(b2.version, 2)
        self.assertEqual(b2.allowed, {"read", "write"})
        self.assertEqual(b2.reauthorised_at, "2026-10-17T00:00:00Z")

    def test_sequence_of_small_allows_does_not_expand(self):
        drift = detect_drift(self.b, [{"read"}, {"write"}, {"admin"}])
        self.assertEqual(drift, ["admin", "write"])
        with self.assertRaises(AuthorityError):
            apply_change(self.b, {"write"})
        with self.assertRaises(AuthorityError):
            apply_change(self.b, {"admin"})
        self.assertEqual(self.b.allowed, {"read"})

if __name__ == "__main__":
    unittest.main()
