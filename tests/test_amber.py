#!/usr/bin/env python3
"""Tests for Amber contracts. Fail closed."""
import unittest
from gaia_core.amber import (
    StorageNote,
    Computation,
    require_durable,
    require_cost,
    WrittenNotDurable,
    MissingCost,
)

class TestRequireDurable(unittest.TestCase):
    def test_none_raises(self):
        with self.assertRaises(WrittenNotDurable):
            require_durable(None)

    def test_written_not_durable_raises(self):
        note = StorageNote(written=True, durable=False)
        with self.assertRaises(WrittenNotDurable):
            require_durable(note)

    def test_durable_passes(self):
        note = StorageNote(written=True, durable=True)
        self.assertIs(require_durable(note), note)

    def test_not_written_passes(self):
        note = StorageNote(written=False, durable=False)
        self.assertIs(require_durable(note), note)

class TestRequireCost(unittest.TestCase):
    def test_none_raises(self):
        with self.assertRaises(MissingCost):
            require_cost(None)

    def test_missing_cost_raises(self):
        comp = Computation(result="ok")
        with self.assertRaises(MissingCost):
            require_cost(comp)

    def test_cost_present_passes(self):
        comp = Computation(result="ok", energy_cost=1.5)
        self.assertIs(require_cost(comp), comp)

if __name__ == "__main__":
    unittest.main()
