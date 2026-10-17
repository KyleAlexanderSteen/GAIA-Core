"""Obsidian contracts. Initialization refuses inherited assumptions. Stasis is refused. Fail closed."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Set

class InheritedAssumption(Exception):
    """Raised when initialization inherits an assumption."""
    pass

class StasisRefused(Exception):
    """Raised when a state is permanent stasis."""
    pass

@dataclass
class Initialization:
    """An initialization. Must not inherit assumptions."""
    assumptions: Set[str] = None
    clean: bool = True

    def __post_init__(self):
        if self.assumptions is None:
            self.assumptions = set()

@dataclass
class State:
    """A state. Permanent stasis is refused."""
    can_transition: bool = True

def require_clean_init(init: Optional[Initialization]) -> Initialization:
    """Require clean initialization. No inherited assumptions.
    
    Raises InheritedAssumption if assumptions are present.
    Returns the initialization if clean.
    """
    if init is None:
        raise InheritedAssumption("no initialization")
    if init.assumptions:
        raise InheritedAssumption(f"inherited assumptions: {init.assumptions}")
    return init

def require_transition(state: Optional[State]) -> State:
    """Require the ability to transition. Permanent stasis is refused.
    
    Raises StasisRefused if the state cannot transition.
    Returns the state if transition is possible.
    """
    if state is None:
        raise StasisRefused("no state")
    if not state.can_transition:
        raise StasisRefused("permanent stasis")
    return state
