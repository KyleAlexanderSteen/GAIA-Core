#!/usr/bin/env python3
"""Tests for Void contracts. Fail closed."""
import unittest
from gaia_core.void import (
    NullState,
    classify_null,
    detect_void_collapse,
    NullClassifiedAsFailure,
    VoidCollapse,
)

class TestClassifyNull(unittest.TestCase):
    def test_none_is_readiness(self):
        self.assertEqual(classify_null(None), "readiness")

    def test_uninitialized_is_readiness(self):
        state = NullState(initialized=False)
        self.assertEqual(classify_null(state), "readiness")

    def test_initialized_is_active(self):
        state = NullState(initialized=True)
        self.assertEqual(classify_null(state), "active")

class TestDetectVoidCollapse(unittest.TestCase):
    def test_none_is_void(self):
        self.assertEqual(detect_void_collapse(None), "void")

    def test_can_return_is_void(self):
        state = NullState(initialized=False, can_return=True)
        self.assertEqual(detect_void_collapse(state), "void")

    def test_cannot_return_raises(self):
        state = NullState(initialized=False, can_return=False)
        with self.assertRaises(VoidCollapse):
            detect_void_collapse(state)

    def test_initialized_is_active(self):
        state = NullState(initialized=True, can_return=True)
        self.assertEqual(detect_void_collapse(state), "active")

if __name__ == "__main__":
    unittest.main()
