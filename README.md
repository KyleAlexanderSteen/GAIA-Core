# GAIA-Core

Shared foundation for GAIA: types, contracts, utilities, and event schemas.

## Workflow contracts (fail closed)

This repository now contains the minimum contracts for:

1. Intent → plan → execute → observe → audit (`run_loop`)
2. Human approval gate (`require_approval`) — explicit allow only
3. Fail-loud stub (`not_implemented`)
4. Provenance on every result (`require_provenance`)
5. Consent check before human-linked action (`require_consent`)

The research → gap → issue → PR → evidence loop is enforced in GAIA-Standards (templates and CI), not here.

No Super Operating System is claimed. These are contracts and checks. Unbuilt paths raise; they do not report success.

## Test

```bash
PYTHONPATH=src python -m unittest tests/test_workflows.py
```
