"""GAIA-Core workflow contracts. Fail closed. No silent success."""
from .loop import run_loop, LoopResult
from .approval import Approval, require_approval
from .authority import AuthorityBoundary, apply_change, detect_drift
from .stub import not_implemented
from .provenance import Provenance, require_provenance
from .consent import Consent, require_consent

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
]
