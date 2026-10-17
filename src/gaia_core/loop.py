"""Intent → plan → execute → observe → audit.

Unexecuted or refused intents still produce an audit record.
No stage reports success for work that did not happen.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Optional

@dataclass
class LoopResult:
    intent_id: str
    planned: bool
    executed: bool
    observed: Optional[str]
    audit: dict
    status: str  # executed | refused | not_implemented

def run_loop(
    intent_id: str,
    *,
    plan: Optional[dict] = None,
    execute: Optional[Callable[[], Any]] = None,
    allow: bool = False,
) -> LoopResult:
    now = datetime.now(timezone.utc).isoformat()
    if not allow:
        audit = {
            "intent_id": intent_id,
            "at": now,
            "stage": "audit",
            "outcome": "refused",
            "reason": "no explicit allow",
        }
        return LoopResult(intent_id, planned=False, executed=False, observed=None, audit=audit, status="refused")
    if plan is None or execute is None:
        audit = {
            "intent_id": intent_id,
            "at": now,
            "stage": "audit",
            "outcome": "not_implemented",
            "reason": "plan or execute missing",
        }
        return LoopResult(intent_id, planned=plan is not None, executed=False, observed=None, audit=audit, status="not_implemented")
    try:
        result = execute()
        observed = str(result)
        status = "executed"
    except NotImplementedError as exc:
        observed = None
        status = "not_implemented"
        result = str(exc)
    audit = {
        "intent_id": intent_id,
        "at": now,
        "stage": "audit",
        "outcome": status,
        "observed": observed,
    }
    return LoopResult(intent_id, planned=True, executed=(status == "executed"), observed=observed, audit=audit, status=status)
