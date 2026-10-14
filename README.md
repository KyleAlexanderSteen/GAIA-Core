# gaia-core

**Status:** Proposed architecture component — not implemented.

**Domain:** Shared Foundation (types, contracts, utilities, error codes, event schemas)

**Visibility:** Internal

**Source:** [GAIA Super-Intelligent Application Architecture Report](https://github.com/KyleAlexanderSteen/GAIA-Documentation) (2026-10-13)

**Traceability:** GAIA-Documentation issues #1–#6

## Purpose
Shared library and contract repository for the entire GAIA system. Single source of truth for cross-cutting concerns. Dependency of all other repositories; not a running service.

## Initial Directory Structure (proposed)
```
gaia-core/
├── src/
│   ├── types/          # Shared data models (Message, Session, User, AgentTask, etc.)
│   ├── contracts/      # OpenAPI / Protobuf schemas
│   ├── errors/         # Standardized error taxonomy
│   ├── utils/          # Logging, ID generators, retry helpers
│   └── events/         # Event bus message definitions
├── package.json / pyproject.toml
├── README.md
└── tests/
```

## Proposed Interfaces and Dependencies
- Published as internal packages (`@gaia/core`, `gaia-core`).
- Depends on: none (foundation).
- Used by: all other GAIA repositories.

## Security and Access-Control Requirements
- No secrets or credentials stored here.
- Contracts must not embed privileged assumptions.
- Least-privilege by default (see GAIA-Documentation #2).

## Tests and Acceptance Criteria
- [ ] Shared types compile and are importable by dependent packages.
- [ ] Contracts are versioned and backward-compatible.
- [ ] No implementation claims beyond scaffolding.
- Linked to GAIA-Documentation #1 (service contracts).

## Development Instructions
This repository is scaffolding only. Do not claim implemented capabilities. Resolve contracts in GAIA-Documentation #1 before adding real code.

**Unresolved:** Authoritative machine-readable contracts, monorepo vs multi-repo decision, full dependency inventory.
