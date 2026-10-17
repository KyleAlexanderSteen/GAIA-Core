"""Provenance required on every result. Missing provenance is incomplete, not success."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

EVIDENCE_STATES = {"verified", "unverified", "reconstructed", "unavailable"}

@dataclass
class Provenance:
    source: str
    version: str
    evidence_state: str

class ProvenanceRequired(Exception):
    pass

def require_provenance(provenance: Optional[Provenance]) -> Provenance:
    if provenance is None:
        raise ProvenanceRequired("result missing provenance")
    if not provenance.source or not provenance.version:
        raise ProvenanceRequired("provenance source and version required")
    if provenance.evidence_state not in EVIDENCE_STATES:
        raise ProvenanceRequired(f"invalid evidence_state: {provenance.evidence_state}")
    return provenance
