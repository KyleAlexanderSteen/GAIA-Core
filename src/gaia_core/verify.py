#!/usr/bin/env python3
"""Independent verification for the workflow contracts.

Re-checks that the public entry points exist and that the fail-closed
paths still raise. Separate from the unit tests.
"""
from __future__ import annotations
import sys

def main() -> int:
    errors = []
    try:
        from gaia_core.loop import run_loop
        from gaia_core.approval import require_approval, ApprovalRequired
        from gaia_core.stub import not_implemented, NotImplementedLoud
        from gaia_core.provenance import require_provenance, ProvenanceRequired
        from gaia_core.consent import require_consent, ConsentRequired
    except Exception as exc:
        print(f"import failed: {exc}", file=sys.stderr)
        return 1

    r = run_loop("verify", allow=False)
    if r.status != "refused" or r.executed:
        errors.append("refuse path did not refuse")
    if not r.audit or r.audit.get("outcome") != "refused":
        errors.append("refuse path missing audit")

    try:
        require_approval(None)
        errors.append("missing approval did not raise")
    except ApprovalRequired:
        pass

    try:
        not_implemented("verify")
        errors.append("stub did not raise")
    except NotImplementedLoud:
        pass

    try:
        require_provenance(None)
        errors.append("missing provenance did not raise")
    except ProvenanceRequired:
        pass

    try:
        require_consent(None, required_scope="read")
        errors.append("missing consent did not raise")
    except ConsentRequired:
        pass

    if errors:
        for e in errors:
            print(e, file=sys.stderr)
        return 1
    print("workflow contracts verification: PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
