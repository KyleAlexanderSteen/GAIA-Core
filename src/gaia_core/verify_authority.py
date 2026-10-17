#!/usr/bin/env python3
"""Independent verification for the authority lifecycle."""
import sys
from gaia_core.authority import AuthorityBoundary, AuthorityError, apply_change, detect_drift

def main() -> int:
    b = AuthorityBoundary("human:1", {"read"})
    try:
        apply_change(b, {"write"}, reauthorised=False)
        print("expansion without reauth did not fail", file=sys.stderr)
        return 1
    except AuthorityError:
        pass
    if b.allowed != {"read"} or b.version != 1:
        print("boundary mutated on refused expansion", file=sys.stderr)
        return 1
    drift = detect_drift(b, [{"write"}, {"admin"}])
    if drift != ["admin", "write"]:
        print(f"unexpected drift: {drift}", file=sys.stderr)
        return 1
    print("authority lifecycle verification: PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
