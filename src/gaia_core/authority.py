"""Authority lifecycle. Distinct from the moment-in-time approval gate.

An approval allows one action. An authority boundary says what may be done
at all. Expanding the boundary requires re-authorisation. A sequence of
small allows cannot silently grow the boundary.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class AuthorityBoundary:
    principal: str
    allowed: set[str]
    version: int = 1
    reauthorised_at: Optional[str] = None

@dataclass
class AuthorityChange:
    kind: str  # routine | expanding
    requested: set[str]
    accepted: bool
    reason: str

class AuthorityError(Exception):
    pass

def classify(boundary: AuthorityBoundary, requested: set[str]) -> str:
    if requested <= boundary.allowed:
        return "routine"
    return "expanding"

def apply_change(
    boundary: AuthorityBoundary,
    requested: set[str],
    *,
    reauthorised: bool = False,
    at: Optional[str] = None,
) -> tuple[AuthorityBoundary, AuthorityChange]:
    if not boundary.principal or not boundary.allowed:
        raise AuthorityError("boundary incomplete")
    kind = classify(boundary, requested)
    if kind == "routine":
        change = AuthorityChange("routine", requested, True, "within boundary")
        return boundary, change
    if not reauthorised:
        change = AuthorityChange("expanding", requested, False, "re-authorisation required")
        raise AuthorityError("scope expansion requires re-authorisation")
    expanded = AuthorityBoundary(
        principal=boundary.principal,
        allowed=set(boundary.allowed) | set(requested),
        version=boundary.version + 1,
        reauthorised_at=at,
    )
    change = AuthorityChange("expanding", requested, True, "re-authorised")
    return expanded, change

def detect_drift(boundary: AuthorityBoundary, allows: list[set[str]]) -> list[str]:
    """Return scopes that a sequence of allows would add beyond the boundary."""
    drift = set()
    for allow in allows:
        drift |= allow - boundary.allowed
    return sorted(drift)
