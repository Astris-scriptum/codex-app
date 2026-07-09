# Codex Monorepo v0.1-alpha

This is the first unified repository scaffold for the Codex ecosystem.

## Components

- `engine/` — Codex Engine core.
- `studio/` — Codex Studio desktop/application layer.
- `api/` — future local/cloud API surface.
- `cloud/` — future sync, accounts, collaboration, and hosted jobs.
- `plugins/` — discovery, scoring, exporter, and provider plugins.
- `language_packs/` — configurable language behaviour.
- `docs/` — canonical architecture and interface documentation.
- `tests/` — integration and cross-component tests.
- `release/` — release packaging scripts and manifests.

## Core rule

Codex Studio must not depend directly on Codex Engine internals. It talks through a stable service layer so future backends can be swapped without rebuilding the user interface.
