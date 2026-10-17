# Authority lifecycle

**Status:** Implemented as a contract. Distinct from `require_approval`.

## Difference

| | Approval gate (`require_approval`) | Authority lifecycle |
| --- | --- | --- |
| What it is | One explicit allow for one action | The boundary of what may be done at all |
| Expansion | Not its job | Requires `reauthorised=True` and bumps version |
| Drift | Not detected | `detect_drift` lists scopes a sequence of allows would add |

## Rules

- A requested set inside `allowed` is `routine` and does not change the boundary.
- A requested set outside `allowed` is `expanding` and fails unless re-authorised.
- A refused expansion does not mutate the boundary.
- A sequence of small allows cannot grow the boundary by itself.

## Non-goals

- No claim this is a full governance system.
- No claim Core #3 already did this.
- Description does not grant authority.
