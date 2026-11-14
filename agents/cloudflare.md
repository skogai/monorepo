# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

## What this repo is

An operations repo for a single Cloudflare account (`ae931e241550e8326149eeda10ada60d`,
`emil@skogsund.se`) — not an application codebase. It holds scripts that inventory and
mutate live Cloudflare state (tunnels, DNS, Access) plus hand-maintained notes describing
that live state. There is no build/test/lint pipeline; changes here have real effect on
live infrastructure the next time a script is run with `--apply`.

Zones in the account (per `cf zones list --account-id`, 2026-11-06): `skogai.se`,
`skogix.se`, `skogix.online`, `skogsund.se`, `skogsund.online`, `tjackgpt.win`. Default zone for the `cf` CLI is
`skogai.se` (set in `.cfrc`).

## Tooling and commands

Tool versions and task runner are managed by `mise` (`mise.toml`), not npm/package.json —
there is no root `package.json`. Tools: `node`, `bun`, `wrangler`, and `cf` (Cloudflare's
newer CLI, installed via `npm:cf`).

```sh
mise run cf-whoami        # cf auth whoami
mise run cf-audit         # run scripts/audit-cloudflare.mjs, print JSON to stdout
mise run cf-audit-write   # same, write to inventory/current-live.json (untracked)
mise run cf-summary       # print counts + tunnel-hostname/Access-app coverage gaps from current-live.json
mise run cf-refresh       # cf-audit-write, then cf-summary — the one command to run at the start of a session
```

You can also invoke the scripts directly with `node scripts/<name>.mjs`. If an older doc
mentions `bun run cf:audit`, that was a root `package.json` script removed in commit
`b1194ce`; use the `mise run` commands above instead.

Auth: the scripts shell out to `cf` (via `scripts/lib/cf.mjs`) and use whatever session
`cf auth whoami` reports — run `cf auth login` if it has expired. They no longer read
any OAuth files or tokens themselves. `scripts/lib/cf.mjs` always sets
`CLOUDFLARE_ACCOUNT_ID` (default `ae931e241550e8326149eeda10ada60d`, overridable via env or
`.env`) because the login reaches several accounts. As of 2026-11-06 every audited
endpoint, Access and AI Gateway included, succeeds under plain `cf` OAuth.

## CLI landscape — what covers what

There are four Cloudflare-adjacent CLIs installed (`cf`, `wrangler`, `cloudflared`,
`warp-cli`), plus the two scripts in this repo. They don't overlap as much as it looks;
each owns a distinct slice. As of 2026-08-14 (`cf` entry re-verified 2026-11-06):

- **`cf`** — as of v1.0.0-beta.25 (verified 2026-11-06) this is a near-complete
  wrapper over the public API: zones, DNS, accounts, Workers/Pages/D1/KV/R2/Queues/
  Vectorize/Secrets Store, **`cf tunnels`** (list, `connections list`, `config get|update`
  for remote ingress) and **`cf zero-trust access`** (applications, reusable policies,
  groups) — all working under plain OAuth. Discover commands with
  `cf cli search "<task>"`, not nested `--help`; `cf schema <cmd>` shows the underlying
  API call. Gotchas:
  - No `--account-id` flag on most commands, and the OAuth login reaches **six**
    accounts. Always `export CLOUDFLARE_ACCOUNT_ID=ae931e241550e8326149eeda10ada60d`
    before running anything.
  - Write commands take `--dry-run` (prints the exact method/URL/body, sends nothing) and
    `--body '<json>'` / `--body @file.json`. Neither is listed in top-level `--help`.
  - Writes are whole-object PUTs: `cf tunnels config update` **replaces the whole ingress
    list** (including the catch-all) and `zero-trust access applications update` replaces
    the whole app. Always `get` first, modify, and send the full object back. Doing this
    merge safely is why `manage-tunnel.mjs` still exists.
  - Lists don't auto-paginate. Use `--page`/`--per-page` (`pages list` caps at 10 per
    page). `zones list` returns zones from **all** accounts unless given `--account-id`.
  - There are no commands for app-scoped Access policies. Use reusable policies
    (`cf zero-trust access policies`), or inline policy objects in an app's `policies`
    array.
  - `.cfrc` default zone is currently `skogai.se`.
- **`wrangler`** — Workers/Pages deploy, and admin for D1, KV, R2, Queues, Vectorize,
  Secrets Store. Has an experimental `wrangler tunnel` (create/delete/list/info/run) but
  no ingress-rule editing and no Access commands.
- **`cloudflared`** — runs a tunnel connector locally, and `tunnel route dns` can create
  the DNS CNAME for a hostname. Its ingress commands (`tunnel ingress validate/rule`)
  only read/validate a local `config.yaml` for locally-run tunnels — they don't touch the
  _remote_ ingress config stored via the API, which is what this account's tunnels use
  (dashboard/API-managed, i.e. `remote_config: true`). `cloudflared access` is
  client-side only (login/token/curl to _reach_ an app) — no app/policy administration.
- **`warp-cli`** — controls the WARP client daemon on _this device_ (connect/disconnect,
  DNS/proxy mode, MDM, device posture). Unrelated to administering account resources;
  its `tunnel`/`connector`/`vnet` subcommands are about this machine's own WARP
  connection, not the account's Cloudflare Tunnels.

Net effect: `cf` now covers remote tunnel ingress and Access administration directly;
`wrangler`/`cloudflared`/`warp-cli` still don't. Since 2026-11-06 the repo's scripts are
thin wrappers over `cf` (see "Core scripts"); they no longer call the REST API directly.

## Cloudflare MCP plugin — preferred integration for Codex sessions

This repo also has the `cloudflare` plugin installed, which adds several MCP servers
(`cloudflare-api`, `cloudflare-bindings`, `cloudflare-builds`, `cloudflare-observability`).
For a Codex session specifically, **this is the better integration than the scripts
below** — reach for it first:

- **`cloudflare-api`**'s `execute` tool runs arbitrary `cloudflare.request()` calls against
  the full REST API (its `search` tool finds the right path/method from the OpenAPI spec,
  `docs` searches Cloudflare's documentation). Verified 2026-08-14: it reaches
  `/cfd_tunnel` and `/access/apps` with clean 200s under its own credentials — the
  Zero-Trust auth-scope problems the scripts' OAuth-file-reading sometimes hit don't
  apply here. This covers the same ground as `manage-tunnel.mjs` and
  `audit-cloudflare.mjs`, without needing either script.
- **`cloudflare-bindings`** gives dedicated tools for D1, KV, R2, Hyperdrive, and reading
  Worker scripts — narrower and more convenient than hand-writing `execute` calls for
  those specific products.
- **`cloudflare-builds`** / **`cloudflare-observability`** cover Workers Builds (CI/CD)
  and Worker logs/metrics — outside what either script does.
- These MCP tools are account-scoped by `account_id`; this repo's account is
  `ae931e241550e8326149eeda10ada60d` (<emil@skogsund.se>). The credentials available also
  reach five _other_ accounts (e.g. <Niklas@aldervall.se>, <skogix@skogai.se>) — always pass
  `account_id` explicitly rather than relying on a default, to avoid operating on the
  wrong account.
- **No built-in dry-run.** Unlike `manage-tunnel.mjs`, `execute` has no `--apply` gate —
  a write call runs immediately. When using it for tunnel ingress or Access changes,
  read the current state first, show the user the diff you intend to make, and only then
  issue the write — i.e., apply the same care the script's dry-run-by-default enforces
  mechanically.

The scripts below remain useful as a **fallback**: for a human running things from a
shell without an agent in the loop (cron, `mise run`, no MCP session), or for
`manage-tunnel.mjs`'s baked-in safety behavior (dry-run by default, ingress-list merge
that preserves the catch-all rule, DNS CNAME paired with ingress adds, `ss -ltn`-based
liveness checking for `prune`) and `audit-cloudflare.mjs`'s persistent
`inventory/current-live.json` snapshot that `mise run cf-summary` reads. For one-off
reads in a session, plain `cf` (with `CLOUDFLARE_ACCOUNT_ID` exported) is now equally
convenient. Update this note if the MCP plugin gains equivalent safety rails or a
persisted-snapshot mode.

## Core scripts

- **`scripts/lib/cf.mjs`** — shared wrapper: runs `cf` with `CLOUDFLARE_ACCOUNT_ID`
  pinned, parses JSON, pages through lists (`cfAll`), and runs writes with
  `--dry-run` unless apply is set (`cfWrite`).

- **`scripts/audit-cloudflare.mjs`** — read-only. Uses `cf` to pull zones, non-deleted
  tunnels (with ingress config, per-connection details, and DNS CNAMEs pointing at
  `*.cfargotunnel.com`), and per-product inventories (Workers, Pages, R2, D1, KV,
  Queues, Vectorize, AI Gateway, Access apps + reusable Access policies, Secrets Store).
  Each product section is fetched independently and reports its own `ok`/`error` status
  instead of failing the whole run.

- **`scripts/manage-tunnel.mjs`** — the safe write path for tunnel ingress, their DNS
  CNAMEs, and Access apps, built on `cf`. **Every mutating subcommand is dry-run by
  default.** In dry-run, writes still go through `cf … --dry-run`, so cf validates them.
  It only commits when you pass `--apply`. Subcommands: `list`, `add`, `rm`, `prune`
  (removes ingress rules whose local port isn't listening, per `ss -ltn`; warns if the
  tunnel isn't healthy, since liveness is only meaningful on the connector's host), and
  `access set-policy|create|rm`. Access policies: `--emails` makes an inline app-scoped
  `allow-list` policy, and `--policy name-or-id,...` attaches existing reusable
  policies. DNS deletes only touch records that point at that tunnel.

Follow the `cf-manage` skill workflow when touching tunnels/DNS/Access: audit first
(`mise run cf-refresh`), dry-run the change, review the diff carefully (right tunnel? right
hostname? right Access emails?), only then re-run with `--apply`, and update the relevant
file under `inventory/` afterward so it stays a true reflection of live state.

## `inventory/` — hand-maintained state notes

These are prose/table docs an operator (or a previous Codex session) wrote after querying
the live account; they are not auto-generated except `current-live.json` (gitignored, local only).
Treat dates in these files literally — they record when something was last verified, not
necessarily current truth. Before relying on any specific resource name, tunnel ID, or
Access policy mentioned in these docs for a live change, re-verify with `mise run cf-refresh`
rather than trusting the doc. As of 2026-11-07, `TODO.md` (repo root) and `email.md`
match live state; the files marked "last verified 2026-08-14" predate a large change in
tunnel state and are background only.

- `tunnels.yaml` — canonical-ish list of tunnels and their ingress routes/services.
- `architecture-review.md` — classification framework (Tunnel vs Worker vs Pages vs R2 vs
  D1/KV/Queues/Vectorize vs external SaaS) plus a hostname-by-hostname decision table.
- `access.md` — Cloudflare Access apps/policies detail.
- `capability-map.md` — what Cloudflare products/resources exist in the account.
- `requirements.md` — local CLI/auth prerequisites for running the scripts in this repo.
- `email.md` — Email Routing per zone and the `aliasflare` Worker (secrets, gotchas, rollback).
- `storage.md` — SkogEdge D1 registry + R2 archive layout and planned import work.
- `next-small-useful.md` — data-store choices (D1/R2/DO/Vectorize) for the next Worker app.

`TODO.md` at the repo root is the prioritized list of open work against live state.

## `workers/aliasflare/`

Git submodule (`skogai2/aliasflare`) holding the live `aliasflare` Worker: self-hosted
email aliases behind Email Routing catch-alls, with a dashboard, REST API and MCP
endpoint at `https://aliasflare.skogai.workers.dev`. Live routing state, secret names,
gotchas and rollback live in `inventory/email.md`.

- Work in the submodule like any repo (commit and push there), then commit the bumped
  submodule pointer here.
- `mise run aliasflare-install | aliasflare-test | aliasflare-dev | aliasflare-deploy |
  aliasflare-tail`. `aliasflare-deploy` runs the tests first, then applies D1 migrations
  and deploys.
- `mise.toml` sets `CLOUDFLARE_ACCOUNT_ID`; without it wrangler refuses to pick one of
  the six reachable accounts in non-interactive mode.
- Local dev secrets go in `workers/aliasflare/.dev.vars` (gitignored by the submodule).
- After a fresh clone: `git submodule update --init`.

## `pangolin/`

Setup docs and config templates for a self-hosted tunnel to `pangolin.aldervall.se`
(Newt binary + systemd, Docker Compose, or raw WireGuard), used as a complement to
Cloudflare Tunnel for hobby/server-park services that don't need to go through
Cloudflare. `NEWT.env` and `.cfrc` at repo root hold live-ish values for a specific
machine's setup, referenced by `pangolin/README.md`.

## `old-systemd-solution/`

Archived systemd user-unit configuration for SkogAI services (moved out of active use
per the most recent commit). Its own `AGENTS.md`/`README.md` describe a now-superseded
workflow (`systemd-analyze verify`, `systemctl --user restart`, etc.) — treat as
historical reference, not current operating procedure for this repo.

## Working with secrets

`.env`, `NEWT.env`, and files under `inventory/` may contain or reference live
credentials/secrets for this account. Never commit real tokens — `.env` is gitignored and
`.env.example` is the template to extend. When editing `inventory/` docs, avoid pasting
raw secret values even though the account owner considers them "not a secret inventory"
for resource _names_.
