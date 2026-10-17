#!/usr/bin/env python3
"""Tests for Terra contracts. Fail closed."""
import unittest
from gaia_core.terra import (
    Session,
    BrownState,
    require_ariditas,
    require_brown_relation,
    AriditasSkipped,
    BrownExtracted,
)

class TestRequireAriditas(unittest.TestCase):
    def test_none_raises(self):
        with self.assertRaises(AriditasSkipped):
            require_ariditas(None)

    def test_coherence_without_ariditas_raises(self):
        session = Session(ariditas_complete=False, coherence_attempted=True)
        with self.assertRaises(AriditasSkipped):
            require_ariditas(session)

    def test_ariditas_complete_passes(self):
        session = Session(ariditas_complete=True, coherence_attempted=True)
        self.assertIs(require_ariditas(session), session)

    def test_no_coherence_passes(self):
        session = Session(ariditas_complete=False, coherence_attempted=False)
        self.assertIs(require_ariditas(session), session)

class TestRequireBrownRelation(unittest.TestCase):
    def test_none_raises(self):
        with self.assertRaises(BrownExtracted):
            require_brown_relation(None)

    def test_pure_frequency_raises(self):
        state = BrownState(wavelength=620.0)
        with self.assertRaises(BrownExtracted):
            require_brown_relation(state)

    def test_incomplete_raises(self):
        state = BrownState(wavelength=620.0, warmth=0.5)
        with self.assertRaises(BrownExtracted):
            require_brown_relation(state)

    def test_complete_relation_passes(self):
        state = BrownState(wavelength=620.0, warmth=0.5, perceiver="human")
        self.assertIs(require_brown_relation(state), state)

if __name__ == "__main__":
    unittest.main()
