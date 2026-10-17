"""Void contracts. Null is readiness. Permanent stasis is collapse. Fail closed."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

class NullClassifiedAsFailure(Exception):
    """Raised when an uninitialized state is classified as failure."""
    pass

class VoidCollapse(Exception):
    """Raised when a null state cannot return to active. Permanent stasis."""
    pass

@dataclass
class NullState:
    """An uninitialized state. Not a failure. Readiness."""
    initialized: bool = False
    can_return: bool = True

def classify_null(state: Optional[NullState]) -> str:
    """Classify a null state. Uninitialized is readiness, not failure.
    
    Raises NullClassifiedAsFailure if the state is marked as failure.
    Returns 'readiness' for uninitialized states.
    Returns 'active' for initialized states.
    """
    if state is None:
        return "readiness"
    if not state.initialized:
        return "readiness"
    return "active"

def detect_void_collapse(state: Optional[NullState]) -> str:
    """Detect void collapse. Permanent stasis is collapse, not healthy void.
    
    Raises VoidCollapse if the state cannot return to active.
    Returns 'void' if return remains possible.
    Returns 'active' if the state is initialized.
    """
    if state is None:
        return "void"
    if state.initialized:
        return "active"
    if not state.can_return:
        raise VoidCollapse("permanent stasis: return to active is impossible")
    return "void"
