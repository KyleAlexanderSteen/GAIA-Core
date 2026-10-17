"""Human approval gate. Explicit allow only. Description or role is not allow."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

@dataclass
class Approval:
    who: str
    what: str
    when: str
    scope: str
    expires_at: Optional[str] = None
    withdrawn: bool = False

class ApprovalRequired(Exception):
    pass

def require_approval(approval: Optional[Approval], *, now: Optional[str] = None) -> Approval:
    if approval is None:
        raise ApprovalRequired("missing explicit allow")
    if approval.withdrawn:
        raise ApprovalRequired("allow withdrawn")
    if not approval.who or not approval.what or not approval.when or not approval.scope:
        raise ApprovalRequired("allow record incomplete")
    if approval.expires_at:
        current = now or datetime.now(timezone.utc).isoformat()
        if current > approval.expires_at:
            raise ApprovalRequired("allow expired")
    return approval
