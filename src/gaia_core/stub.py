"""Fail-loud stub. Unbuilt paths must not report success."""
from __future__ import annotations

class NotImplementedLoud(Exception):
    """Raised when a path is not implemented. Never a success."""

def not_implemented(name: str) -> None:
    raise NotImplementedLoud(f"{name} is not implemented")
