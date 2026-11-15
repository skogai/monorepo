---
type: repository
title: cloudflare
description: Private operations repo for one Cloudflare account. Node scripts wrap the `cf` CLI to audit and change tunnels, DNS and Access, next to hand-written inventory notes. Active, with an open TODO list against live state.
tags: [cloudflare, ops, tunnels, access, dns, email]
repo: skogai/cloudflare
commit: 1167f2e
last_commit: 2026-11-13
generated: { by: "claude-code", at: "2026-11-15" }
sources:
  - repos/cloudflare/AGENTS.md
  - repos/cloudflare/CLAUDE.md
  - repos/cloudflare/TODO.md
  - repos/cloudflare/mise.toml
  - repos/cloudflare/.gitmodules
  - repos/cloudflare/.gitignore
  - repos/cloudflare/.env.example
  - repos/cloudflare/.cfrc
  - repos/cloudflare/.claude/settings.json
  - repos/cloudflare/.claude/skills/cf-manage/SKILL.md
  - repos/cloudflare/.codex/config.toml
  - repos/cloudflare/scripts/lib/cf.mjs
  - repos/cloudflare/scripts/audit-cloudflare.mjs
  - repos/cloudflare/scripts/audit-summary.mjs
  - repos/cloudflare/scripts/manage-tunnel.mjs
  - repos/cloudflare/inventory/email.md
  - repos/cloudflare/inventory/storage.md
  - repos/cloudflare/inventory/tunnels.yaml
  - repos/cloudflare/migrations/0001_skogedge_registry.sql
  - repos/cloudflare/pangolin/README.md
  - repos/cloudflare/skogix-skogai.sh
  - repos/cloudflare/old-systemd-solution/README.md
  - repos/cloudflare/old-systemd-solution/services.json
  - repos/cloudflare/.skogai/journal.md
---

# cloudflare

**An operations repo for a single Cloudflare account: scripts that inventory and change live tunnels, DNS records and Access apps, plus hand-maintained notes about that live state.** It is not an application. There is no build, test or lint pipeline, and a script run with `--apply` changes live infrastructure. The repo is active: the last commit (2026-11-13) added a new hostname behind Access, `TODO.md` lists open work, and several inventory files are marked stale by the repo itself. It also carries an archived systemd setup, Pangolin tunnel templates and one Worker as a git submodule.

## Source map

| Path | Holds |
|---|---|
| `AGENTS.md`, `CLAUDE.md` | The same 217-line guide, worded once for Codex and once for Claude. The best description of the repo. |
| `TODO.md` | Prioritized open work against live state (exposed hostnames, dead tunnels, DNS/ingress mismatches, Access cleanup, email). |
| `mise.toml`, `mise.lock` | Tool pins (`node`, `bun`, `wrangler`, `npm:cf`, `cloudflared`), the `CLOUDFLARE_ACCOUNT_ID` pin and all tasks. |
| `scripts/lib/cf.mjs` | Shared wrapper around the `cf` CLI. |
| `scripts/audit-cloudflare.mjs` | Read-only account audit, JSON output. |
| `scripts/audit-summary.mjs` | Prints counts and coverage gaps from the saved audit. |
| `scripts/manage-tunnel.mjs` | Write path for tunnel ingress, DNS CNAMEs and Access apps. Dry-run by default. |
| `inventory/` | Hand-written state notes: `tunnels.yaml`, `access.md`, `capability-map.md`, `architecture-review.md`, `requirements.md`, `email.md`, `storage.md`, `next-small-useful.md`. `current-live.json` is generated and gitignored. |
| `migrations/0001_skogedge_registry.sql` | D1 schema for the SkogEdge registry: tables `services`, `resources`, `artifacts`. |
| `workers/aliasflare` | Git submodule pointing at `skogai2/aliasflare` (email alias Worker). Not initialized in a plain clone. |
| `.claude/skills/cf-manage/`, `.agents/skills/cf-manage/` | The same `cf-manage` skill for Claude and Codex. |
| `.claude/settings.json` | Enables the `cloudflare` plugin from the `cloudflare/skills` marketplace. |
| `.codex/config.toml` | Three MCP server URLs for Codex, two of them on `skogai.se` hostnames. |
| `.cfrc` | Default zone for the `cf` CLI (`skogai.se`). |
| `.env.example` | Template naming `CLOUDFLARE_ACCOUNT_ID`, `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_API_BASE_URL`. |
| `pangolin/` | Docs and templates for a self-hosted Pangolin tunnel (Newt systemd unit, quadlet, compose files, WireGuard example). |
| `skogix-skogai.sh`, `skogix-skogdata.sh` | Two four-line scripts that run a `cloudflared` connector in podman on network `skognet`. |
| `old-systemd-solution/` | Archived systemd user units and start scripts for about 27 `skogai-*` services, with `services.json`. |
| `.skogai/journal.md`, `.skogai/logs/skogai-core/log.jsonl` | Session journal and hook log written by the skogai-core plugin. |

## How it works

### The `cf` wrapper

All scripts shell out to the `cf` CLI and use its OAuth session. They do not read tokens themselves. `scripts/lib/cf.mjs` loads `.env` without overriding the real environment (`cf.mjs:18-29`), then pins `CLOUDFLARE_ACCOUNT_ID` on every call (`cf.mjs:31-33`), because the login reaches several accounts and most `cf` commands have no account flag. `cfAll` pages through lists, since `cf` does not auto-paginate (`cf.mjs:52-60`). `cfWrite` adds `--dry-run` unless `apply` is true, so a dry run is still validated by `cf` (`cf.mjs:63-65`).

### Audit

`scripts/audit-cloudflare.mjs` lists zones and non-deleted tunnels (`audit-cloudflare.mjs:24-25`), collects each tunnel's ingress config and connections (`:53`), the DNS CNAMEs that point at tunnels (`:81`), and one inventory section per product: Workers, Pages, R2, D1, KV, Queues, Vectorize, AI Gateway, Access apps and policies, Secrets Store (`:33`, `:197`). Each section reports its own `ok` or `error` instead of failing the run (`:105`). `--write <path>` saves the JSON. `scripts/audit-summary.mjs` reads `inventory/current-live.json` and prints tunnel hostnames that have no matching Access app (`audit-summary.mjs:42-44`).

### Changes

`scripts/manage-tunnel.mjs` has the subcommands `list`, `add`, `rm`, `prune` and `access set-policy|create|rm` (`manage-tunnel.mjs:26-33`). Why it exists: `cf tunnels config update` replaces the whole ingress list, so the script reads the config, merges one rule and keeps the catch-all rule (`:72-90`). `add` pairs the ingress rule with a DNS CNAME and optionally an Access app (`:239`). DNS deletes only touch records that point at the given tunnel (`:125`). `prune` removes rules whose local port is not listening according to `ss -ltn` (`:212-219`, `:273`), which only means something on the connector's own host. Access policies are either an inline email allow-list (`--emails`) or existing reusable policies (`--policy`) (`:147`).

### Inventory notes

The files under `inventory/` are written by hand after querying the account. Four carry a "Stale — last verified 2026-08-14" banner: `tunnels.yaml`, `access.md`, `capability-map.md`, `architecture-review.md`. The guide says `TODO.md` and `inventory/email.md` matched live state on 2026-11-07. `inventory/storage.md` describes the SkogEdge D1 registry and R2 archive that `migrations/0001_skogedge_registry.sql` belongs to.

### Agent integration

The guide tells agent sessions to prefer the Cloudflare MCP plugin (`cloudflare-api`, `cloudflare-bindings`, `cloudflare-builds`, `cloudflare-observability`) over the scripts, and warns that its `execute` tool has no dry-run gate. The scripts remain the fallback for shell use and for the dry-run and merge safety.

## How to use it

Prerequisites: `mise` (it installs the pinned tools), a valid `cf auth login` session, and for the Worker `git submodule update --init`. `mise.toml` sets `CLOUDFLARE_ACCOUNT_ID` for the whole repo; `.env` (gitignored) can override it.

| Task | Does |
|---|---|
| `mise run cf-whoami` | `cf auth whoami` |
| `mise run cf-audit` | Audit to stdout |
| `mise run cf-audit-write` | Audit to `inventory/current-live.json` |
| `mise run cf-summary` | Counts and coverage gaps from that file |
| `mise run cf-refresh` | `cf-audit-write`, then the summary. The guide's start-of-session command. |
| `mise run aliasflare-install`, `-test`, `-dev`, `-deploy`, `-tail` | npm and wrangler commands inside `workers/aliasflare`; `-deploy` depends on `-test`. |

Changes go through `node scripts/manage-tunnel.mjs <subcommand> ...`, first without `--apply`, then with it. The `cf-manage` skill fixes the order: audit, dry-run, review, apply, update `inventory/`. `pangolin/README.md` describes three ways to connect to a Pangolin server; the credentials it needs are `NEWT_ID` and `NEWT_SECRET` in `/etc/newt/newt.env`.

## Relations to other SkogAI repos

- **podman**: runs the connector for tunnel `skognet-cloudflare` as a quadlet and reads that tunnel's ingress with `cf`. It pins the same `CLOUDFLARE_ACCOUNT_ID`. `TODO.md` here records the podman connector pattern (containers on a podman network, ingress targets by container name). Both repos change the same live tunnel and Access state.
- **skogai2/aliasflare**: the submodule at `workers/aliasflare`. `inventory/email.md` calls it a fork of an upstream project and holds its routing state and secret names.
- **systemd**: `old-systemd-solution/` is an archived copy of systemd user units for `skogai-*` services. The catalog also has a `systemd` repo; this page did not compare the two.
- **skogai-core**: its hooks write `.skogai/journal.md` and `.skogai/logs/skogai-core/log.jsonl`.
- `.codex/config.toml` points Codex at `mcp.skogai.se`, the MCPHub instance defined in the podman repo.
- Journal and log paths show the working checkout at `~/.local/src/cloudflare`.

## Gaps and stale references

- Open security follow-ups are tracked in the repo itself (`TODO.md`); they are not repeated in this wiki.
- `TODO.md` "Do first" items, open since 2026-11-07, include the Access decision for `mcp.skogai.se` and restoring the `skogai.se` MX records.
- `TODO.md` says 13 tunnels exist and 2 are healthy; the rest await a keep, revive or delete decision. It also lists duplicate ingress rules, CNAMEs without rules, rules without DNS and Access apps without hostnames.
- Podman's `PLAN.md` says `termix.skogai.se` moved to `skognet-cloudflare` on 2026-11-13 and its Access app was deleted on 2026-11-14. `TODO.md` here still shows it with an Access app and counts one hostname on that tunnel.
- `manage-tunnel.mjs rm` and `prune` are untested live, per `TODO.md` §4.
- `AGENTS.md` says `NEWT.env` is at the repo root; it is at `pangolin/NEWT.env`. It also says `old-systemd-solution/` was archived "per the most recent commit", which is no longer the most recent.
- `old-systemd-solution/README.md` documents `bin/status`, `bin/check`, `bin/verify` and `bin/diff-live`. No `bin/` directory exists in that folder.
- `skogix-skogai.sh` starts the connector for tunnel `skogai`, which `TODO.md` lists as down. `skogix-skogdata.sh` is for a tunnel that never got ingress.
- `pangolin/a.yml` and `pangolin/docker-compose.yml` are identical in structure and use a `pangolin-cli` image with `NET_ADMIN`, while the README says the compose method uses `fosrl/newt` without it.
- The Worker submodule was not initialized in the clone, so its code was not read. The inventory files and the journal were read only in part.
