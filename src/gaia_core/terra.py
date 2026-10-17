"""Terra contracts. The ground is the precondition. Brown is not extractable. Fail closed."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

class AriditasSkipped(Exception):
    """Raised when coherence is attempted without the Ariditas phase."""
    pass

class BrownExtracted(Exception):
    """Raised when brown is treated as a pure frequency. Brown is a relation."""
    pass

@dataclass
class Session:
    """A session. Ariditas must complete before coherence."""
    ariditas_complete: bool = False
    coherence_attempted: bool = False

@dataclass
class BrownState:
    """Brown is a relation, not a pure frequency."""
    wavelength: Optional[float] = None
    warmth: Optional[float] = None
    perceiver: Optional[str] = None

def require_ariditas(session: Optional[Session]) -> Session:
    """Require the Ariditas phase before coherence.
    
    Raises AriditasSkipped if coherence is attempted without the phase.
    Returns the session if the phase is complete.
    """
    if session is None:
        raise AriditasSkipped("no session")
    if session.coherence_attempted and not session.ariditas_complete:
        raise AriditasSkipped("coherence attempted without Ariditas phase")
    return session

def require_brown_relation(state: Optional[BrownState]) -> BrownState:
    """Require brown as a relation, not a pure frequency.
    
    Raises BrownExtracted if brown is treated as a pure frequency.
    Returns the state if the relation is preserved.
    """
    if state is None:
        raise BrownExtracted("no state")
    if state.wavelength is not None and state.warmth is None and state.perceiver is None:
        raise BrownExtracted("brown treated as pure frequency")
    if state.wavelength is None or state.warmth is None or state.perceiver is None:
        raise BrownExtracted("relation incomplete")
    return state
