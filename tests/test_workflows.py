#!/usr/bin/env python3
"""Tests for the six workflow contracts. Fail closed."""
import unittest
from gaia_core.loop import run_loop
from gaia_core.approval import Approval, require_approval, ApprovalRequired
from gaia_core.stub import not_implemented, NotImplementedLoud
from gaia_core.provenance import Provenance, require_provenance, ProvenanceRequired
from gaia_core.consent import Consent, require_consent, ConsentRequired

class TestLoop(unittest.TestCase):
    def test_refused_without_allow_still_audited(self):
        r = run_loop("i1", allow=False)
        self.assertEqual(r.status, "refused")
        self.assertFalse(r.executed)
        self.assertEqual(r.audit["outcome"], "refused")

    def test_missing_plan_is_not_implemented(self):
        r = run_loop("i2", allow=True, plan=None, execute=None)
        self.assertEqual(r.status, "not_implemented")
        self.assertFalse(r.executed)

    def test_executed_only_when_allow_and_execute(self):
        r = run_loop("i3", allow=True, plan={"steps": 1}, execute=lambda: "ok")
        self.assertEqual(r.status, "executed")
        self.assertTrue(r.executed)
        self.assertEqual(r.observed, "ok")

class TestApproval(unittest.TestCase):
    def test_missing_raises(self):
        with self.assertRaises(ApprovalRequired):
            require_approval(None)

    def test_withdrawn_raises(self):
        a = Approval("h", "act", "2026-10-17T00:00:00Z", "scope", withdrawn=True)
        with self.assertRaises(ApprovalRequired):
            require_approval(a)

    def test_expired_raises(self):
        a = Approval("h", "act", "2026-10-17T00:00:00Z", "scope", expires_at="2026-10-16T00:00:00Z")
        with self.assertRaises(ApprovalRequired):
            require_approval(a, now="2026-10-17T00:00:00Z")

    def test_incomplete_raises(self):
        a = Approval("", "act", "2026-10-17T00:00:00Z", "scope")
        with self.assertRaises(ApprovalRequired):
            require_approval(a)

    def test_explicit_passes(self):
        a = Approval("h", "act", "2026-10-17T00:00:00Z", "scope")
        self.assertIs(require_approval(a), a)

class TestStub(unittest.TestCase):
    def test_stub_raises(self):
        with self.assertRaises(NotImplementedLoud):
            not_implemented("future-runtime")

class TestProvenance(unittest.TestCase):
    def test_missing_raises(self):
        with self.assertRaises(ProvenanceRequired):
            require_provenance(None)

    def test_bad_state_raises(self):
        p = Provenance("fixture", "1.0.0", "guessed")
        with self.assertRaises(ProvenanceRequired):
            require_provenance(p)

    def test_valid_passes(self):
        p = Provenance("fixture", "1.0.0", "unverified")
        self.assertIs(require_provenance(p), p)

class TestConsent(unittest.TestCase):
    def test_missing_raises(self):
        with self.assertRaises(ConsentRequired):
            require_consent(None, required_scope="read")

    def test_withdrawn_raises(self):
        c = Consent("human:1", "read", granted=True, withdrawn=True)
        with self.assertRaises(ConsentRequired):
            require_consent(c, required_scope="read")

    def test_scope_mismatch_raises(self):
        c = Consent("human:1", "read", granted=True)
        with self.assertRaises(ConsentRequired):
            require_consent(c, required_scope="write")

    def test_valid_passes(self):
        c = Consent("human:1", "read", granted=True)
        self.assertIs(require_consent(c, required_scope="read"), c)

if __name__ == "__main__":
    unittest.main()
