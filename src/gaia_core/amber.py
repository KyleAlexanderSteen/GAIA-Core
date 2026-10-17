"""Amber contracts. Written is not durable. Missing cost is not efficiency. Fail closed."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

class WrittenNotDurable(Exception):
    """Raised when written is reported as durable."""
    pass

class MissingCost(Exception):
    """Raised when a computation has no energy cost."""
    pass

@dataclass
class StorageNote:
    """A storage note. Written is not durable until durability is confirmed."""
    written: bool = False
    durable: bool = False

@dataclass
class Computation:
    """A computation. Missing cost is not efficiency."""
    result: Optional[str] = None
    energy_cost: Optional[float] = None

def require_durable(note: Optional[StorageNote]) -> StorageNote:
    """Require durability before reporting success.
    
    Raises WrittenNotDurable if written is reported as durable without confirmation.
    Returns the note if durability is confirmed or not yet written.
    """
    if note is None:
        raise WrittenNotDurable("no note")
    if note.written and not note.durable:
        raise WrittenNotDurable("written but not durable")
    return note

def require_cost(comp: Optional[Computation]) -> Computation:
    """Require an energy cost before reporting efficiency.
    
    Raises MissingCost if the computation has no cost.
    Returns the computation if the cost is present.
    """
    if comp is None:
        raise MissingCost("no computation")
    if comp.energy_cost is None:
        raise MissingCost("missing energy cost")
    return comp
