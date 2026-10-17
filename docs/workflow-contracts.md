# Workflow contracts (specification)

**Status:** Implemented in this PR. Contracts and checks only. No Super Operating System is claimed.

## 1. Intent → plan → execute → observe → audit

`run_loop(intent_id, *, plan, execute, allow)`

- Without `allow=True`, status is `refused` and an audit record is written. Nothing executes.
- With allow but missing plan or execute, status is `not_implemented`. Nothing executes.
- With allow, plan, and execute, status is `executed` and the observed result is recorded.
- Refused and unexecuted paths still produce an audit record.

## 2. Human approval gate

`require_approval(approval)`

- `None` raises `ApprovalRequired`.
- Withdrawn or expired allow raises.
- Incomplete record (missing who/what/when/scope) raises.
- Description or role is not an allow.

## 3. Fail-loud stub

`not_implemented(name)` raises `NotImplementedLoud`. It never returns success.

## 4. Provenance

`require_provenance(provenance)` requires source, version, and an evidence state in `{verified, unverified, reconstructed, unavailable}`. Missing provenance raises `ProvenanceRequired`.

## 5. Consent

`require_consent(consent, required_scope=...)` requires a granted, non-withdrawn consent whose scope covers the action. Missing or withdrawn consent raises `ConsentRequired`.

## 6. Research → gap → issue → PR → evidence

Enforced in GAIA-Standards (templates and CI). Not reimplemented here.

## Non-goals

- No runtime that executes real intents against external systems.
- No claim that a Super Operating System exists.
- No authority grant from a description or label.
