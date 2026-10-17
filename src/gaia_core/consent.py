"""Consent check before any human-linked action. Fail closed."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

@dataclass
class Consent:
    principal: str
    scope: str
    granted: bool
    withdrawn: bool = False

class ConsentRequired(Exception):
    pass

def require_consent(consent: Optional[Consent], *, required_scope: str) -> Consent:
    if consent is None:
        raise ConsentRequired("missing consent")
    if not consent.granted or consent.withdrawn:
        raise ConsentRequired("consent not granted or withdrawn")
    if not consent.principal or not consent.scope:
        raise ConsentRequired("consent record incomplete")
    if required_scope not in consent.scope and consent.scope != "*":
        raise ConsentRequired(f"consent scope does not cover {required_scope}")
    return consent
