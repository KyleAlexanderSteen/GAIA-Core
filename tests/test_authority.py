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
        self.assertEqual(change.kind, "routine")
        self.assertEqual(b2.version, 1)
        self.assertEqual(b2.allowed, {"read"})
        self.assertIs(b2, self.b)

    def test_empty_request_is_routine(self):
        self.assertEqual(classify(self.b, set()), "routine")
        b2, change = apply_change(self.b, set())
        self.assertTrue(change.accepted)
        self.assertEqual(b2.allowed, {"read"})

    def test_subset_is_routine(self):
        b = AuthorityBoundary("human:1", {"read", "list"})
        self.assertEqual(classify(b, {"list"}), "routine")

    def test_expansion_without_reauth_fails(self):
        self.assertEqual(classify(self.b, {"read", "write"}), "expanding")
        with self.assertRaises(AuthorityError):
            apply_change(self.b, {"write"}, reauthorised=False)
        self.assertEqual(self.b.allowed, {"read"})
        self.assertEqual(self.b.version, 1)
        self.assertIsNone(self.b.reauthorised_at)

    def test_expansion_with_reauth_versions(self):
        b2, change = apply_change(self.b, {"write"}, reauthorised=True, at="2026-10-17T00:00:00Z")
        self.assertTrue(change.accepted)
        self.assertEqual(change.kind, "expanding")
        self.assertEqual(b2.version, 2)
        self.assertEqual(b2.allowed, {"read", "write"})
        self.assertEqual(b2.reauthorised_at, "2026-10-17T00:00:00Z")
        self.assertEqual(self.b.version, 1)

    def test_second_expansion_requires_another_reauth(self):
        b2, _ = apply_change(self.b, {"write"}, reauthorised=True, at="t1")
        with self.assertRaises(AuthorityError):
            apply_change(b2, {"admin"}, reauthorised=False)
        self.assertEqual(b2.allowed, {"read", "write"})
        b3, change = apply_change(b2, {"admin"}, reauthorised=True, at="t2")
        self.assertEqual(change.kind, "expanding")
        self.assertEqual(b3.version, 3)
        self.assertEqual(b3.allowed, {"read", "write", "admin"})

    def test_sequence_of_small_allows_does_not_expand(self):
        drift = detect_drift(self.b, [{"read"}, {"write"}, {"admin"}])
        self.assertEqual(drift, ["admin", "write"])
        with self.assertRaises(AuthorityError):
            apply_change(self.b, {"write"})
        with self.assertRaises(AuthorityError):
            apply_change(self.b, {"admin"})
        self.assertEqual(self.b.allowed, {"read"})

    def test_incomplete_boundary_fails(self):
        with self.assertRaises(AuthorityError):
            apply_change(AuthorityBoundary("", {"read"}), {"read"})
        with self.assertRaises(AuthorityError):
            apply_change(AuthorityBoundary("human:1", set()), {"read"})

    def test_reauth_false_is_default(self):
        with self.assertRaises(AuthorityError):
            apply_change(self.b, {"export"})

if __name__ == "__main__":
    unittest.main()
