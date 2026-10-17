"""GAIA-Core workflow contracts. Fail closed. No silent success."""
from .loop import run_loop, LoopResult
from .approval import Approval, require_approval
from .authority import AuthorityBoundary, apply_change, detect_drift
from .stub import not_implemented
from .provenance import Provenance, require_provenance
from .consent import Consent, require_consent
from .void import NullState, classify_null, detect_void_collapse
from .terra import Session, BrownState, require_ariditas, require_brown_relation
from .amber import StorageNote, Computation, require_durable, require_cost
from .obsidian import Initialization, State, require_clean_init, require_transition

__all__ = [
    "run_loop",
    "LoopResult",
    "Approval",
    "require_approval",
    "AuthorityBoundary",
    "apply_change",
    "detect_drift",
    "not_implemented",
    "Provenance",
    "require_provenance",
    "Consent",
    "require_consent",
    "NullState",
    "classify_null",
    "detect_void_collapse",
    "Session",
    "BrownState",
    "require_ariditas",
    "require_brown_relation",
    "StorageNote",
    "Computation",
    "require_durable",
    "require_cost",
    "Initialization",
    "State",
    "require_clean_init",
    "require_transition",
]
