#!/usr/bin/env python3
"""Tests for Obsidian contracts. Fail closed."""
import unittest
from gaia_core.obsidian import (
    Initialization,
    State,
    require_clean_init,
    require_transition,
    InheritedAssumption,
    StasisRefused,
)

class TestRequireCleanInit(unittest.TestCase):
    def test_none_raises(self):
        with self.assertRaises(InheritedAssumption):
            require_clean_init(None)

    def test_assumptions_raise(self):
        init = Initialization(assumptions={"prior"})
        with self.assertRaises(InheritedAssumption):
            require_clean_init(init)

    def test_clean_passes(self):
        init = Initialization()
        self.assertIs(require_clean_init(init), init)

class TestRequireTransition(unittest.TestCase):
    def test_none_raises(self):
        with self.assertRaises(StasisRefused):
            require_transition(None)

    def test_stasis_raises(self):
        state = State(can_transition=False)
        with self.assertRaises(StasisRefused):
            require_transition(state)

    def test_transition_passes(self):
        state = State(can_transition=True)
        self.assertIs(require_transition(state), state)

if __name__ == "__main__":
    unittest.main()
