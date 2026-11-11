# Open Knowledge and a current-work wiki

Status: proposal, 2026-11-11. No adoption or hosting decision made.
Run: Codex (gpt-6-astra), T3 Code / Codex harness, skogix-workstation,
checkout `/home/skogix/dev/Work/t3-16facfd2-c69f27fa28070a33`,
base `19ede8e8443b420f2e8b9eac6f0800727c6def5e`.

## Recommendation

Start recording current work in `doc/current-work.md` immediately. Pilot Open Knowledge as a reading, search, and validation layer over a small `doc/wiki/` bundle next. Keep the existing plan, ADRs, research, and experiment records authoritative in their established locations. A wiki should help a new session answer what is happening, why, what is blocked, and what happens next.

Git Markdown remains editable and readable without the executable. Avoid migrating the entire repository before learning whether the wiki helps. The pilot can be removed without losing the current-work record.

## Sources and findings

Repository source inspected: README, `doc/plan.md`, ADR 0001, and root `mise.toml` at the base above. The plan defers a docs site until a need appears; this request supplies a concrete need for ongoing-work documentation, but does not choose hosting.

External source: [skogai2/okn README](https://github.com/skogai2/okn/blob/99b05e27ce328db3ae4d31cd0e30f178ead6de30/README.md) and [installation documentation](https://github.com/skogai2/okn/blob/99b05e27ce328db3ae4d31cd0e30f178ead6de30/Wiki/features/installation.md), read through GitHub API on 2026-11-11. This repository is a fork of openknowledge-sh/openknowledge. Its README describes Markdown setup, search, validation, a local viewer, static publication, and optional MCP. These are source observations, not integration test results.

Machine observation: `/home/skogix/.local/bin/openknowledge` reports 0.13.0. Its provenance is unverified. It supports scaffold, validate, search, view and export; `check --help` fails with unknown command, despite current main documenting check. Do not copy current-main setup instructions into a reproducible recipe for this binary.

Local help says search uses lexical and hashed local vector features without an embedding service. A scratch scaffold validated and search returned heading/line evidence. This establishes basic command behavior only, not retrieval quality on our documentation. Viewer help defaults to loopback; no browser or server was started. Export refused the default scaffold because release outputs were disabled.

## Installation route

`mise registry | rg -i 'openknowledge|okn|hugo|mkdocs'` found Hugo entries but no named Open Knowledge entry on this machine. This does not rule out generic mise backends. The fork releases API returned an empty list. The upstream installer documentation describes release archives and an npm wrapper (`@openknowledge-sh/openknowledge`), defaulting to the upstream release repository.

First investigate a pinned mise npm or GitHub backend installation in isolation. Verify archive availability, binary aliases, platform support and version before adding configuration. If fork changes are required, pin a fork commit and document its source-build prerequisites instead. Do not assume an upstream package represents skogai2/okn main. No installation was attempted here.

## Pilot plan

1. Maintain `doc/current-work.md`: each active item has status, owner, last update, next action, blocker and source/PR links. Update it in the PR that changes the work; the owner resolves competing updates during review. Move completed details into evidence or durable documentation and keep a short completion link.
2. Select and pin a reproducible executable through mise. Acceptance: a second checkout can obtain the same version without relying on `~/.local/bin`.
3. Create `doc/wiki/` with an index, current-work navigation, a workflow page and a dated log. Use an isolated scaffold first and inspect generated instructions. Do not replace repository AGENTS.md. Confirm how links outside the bundle behave before choosing adoption or a generated projection of existing pages. Any projection must identify its source and be regenerated, never maintained independently.
4. Trial three real queries: “what are we doing now?”, “what blocks fresh checkout setup?”, and “which decisions are accepted?”. Acceptance: each returns the correct maintained page with inspectable evidence. Also deliberately break one internal link and confirm validation catches it.
5. Browse locally and verify navigation, external source links and search. Restore the broken-link fixture. Record commands, version, results and prerequisites in `.skogai/tests/`; repeat on another machine before calling the setup reproducible.
6. Only then evaluate static HTML publication. Enable viewer output in a disposable fixture, inspect exported files and source archives, and establish intended audience and hosting. Acceptance: reviewed content only, working links under the hosting base path, repeatable build and a rollback to the previous artifact. No hosting provider is selected here.

Prefer Open Knowledge's built-in viewer/export for this pilot; a separate site generator adds a second layer before its value is demonstrated. Keep Git PRs as the editing workflow initially. Consider MCP only if agents need access beyond checkout files; defer claims, semantic queries, production runtimes and automated knowledge gates until a specific need exists.

## Open questions

- Is the wiki private to the crew or intended for public readers?
- Is upstream release compatibility enough, or are fork-specific changes required?
- Can the chosen version navigate existing documents outside its bundle without copying them?
- Who owns keeping current-work entries fresh after merged PRs?

No root CI, application tests, live viewer, publication, managed installation, second-machine reproduction or production MCP was run.
