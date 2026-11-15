---
type: repository
title: podman
description: "Private repo of rootless Podman Quadlet units for one workstation: a Cloudflare tunnel connector, MCPHub with Postgres, a Postgres for basic-memory, and Termix, plus health-check and backup scripts. Active."
tags: [podman, quadlet, systemd, ops, cloudflare, mcp]
repo: skogai/podman
commit: d1c56a7
last_commit: 2026-11-14
generated: { by: "claude-code", at: "2026-11-15" }
sources:
  - repos/podman/AGENTS.md
  - repos/podman/SKOGAI.md
  - repos/podman/PLAN.md
  - repos/podman/SECRETS.md
  - repos/podman/mise.toml
  - repos/podman/.gitignore
  - repos/podman/docs/networking.md
  - repos/podman/skognet-cloudflare/skognet-cloudflare.container
  - repos/podman/skognet-cloudflare/skognet-cloudflare.network
  - repos/podman/mcphub/skogai-mcphub.container
  - repos/podman/mcphub/skogai-mcphub-postgres.container
  - repos/podman/mcphub/README.md
  - repos/podman/basic-memory/basic-memory-postgres.container
  - repos/podman/termix/termix.container
  - repos/podman/termix/README.md
  - repos/podman/termix/hosts-config/hosts.yaml
  - repos/podman/bin/quadlet-health
  - repos/podman/bin/pg-backup
  - repos/podman/bin/termix-backup
  - repos/podman/bin/env-from-example
  - repos/podman/bin/postgres-password
  - repos/podman/bin/credential-key
  - repos/podman/bin/container-env
  - repos/podman/mise-tasks/setup/_default
  - repos/podman/mise-tasks/setup/cloudflare
  - repos/podman/mise-tasks/setup/mcphub
  - repos/podman/units/quadlet-health.service
  - repos/podman/units/pg-backup.service
---

# podman

**Rootless Podman Quadlet definitions for the user systemd services on one workstation, with the scripts that set them up, check them and back them up.** The repo is cloned to `~/.config/containers/systemd`, the only place podman's user generator reads quadlets from. It holds four services: the `skognet-cloudflare` tunnel connector, MCPHub with its Postgres, a Postgres for basic-memory, and Termix. Application code lives elsewhere; this repo is only unit files, env templates and shell. It is active: 50 commits of history end on 2026-11-14, and `PLAN.md` has phases 1-4 done and phase 5 on hold.

## Source map

| Path | Holds |
|---|---|
| `AGENTS.md` | Router file. Points to `SKOGAI.md`. |
| `SKOGAI.md` | The real guide: structure, commands, Quadlet rules, monitoring and backup setup. Routes to `PLAN.md` and `SECRETS.md`. |
| `PLAN.md` | Plan, decisions, open questions and a dated progress log. |
| `SECRETS.md` | Where every gitignored env file and secret comes from on a new machine. Names only, no values. |
| `docs/networking.md` | Step-by-step guide for adding a service: network, container file, bridges, public hostname, checks. |
| `mise.toml` | Env pins (`CLOUDFLARE_ACCOUNT_ID`, `CLOUDFLARE_ZONE_ID`, `SKOGNET_TUNNEL_ID`, `TERMIX_URL`), loads `termix/termix-claude.env`, pins the `mcphub` and `termix` CLIs. |
| `mise-tasks/setup/` | `setup` (default), `setup:cloudflare`, `setup:mcphub`, `setup:basic-memory`, `setup:mcphub-cli`. |
| `mise-tasks/mcphub/` | `mcphub:seed` and `mcphub:dev` for a throwaway local hub. |
| `skognet-cloudflare/` | Tunnel connector container, its network with a pinned subnet, env template. |
| `mcphub/` | `skogai-mcphub.container`, `skogai-mcphub-postgres.container`, network, env templates, README. |
| `basic-memory/` | `basic-memory-postgres.container` (pgvector), network, env template. |
| `termix/` | `termix.container`, network, `hosts-config/hosts.yaml`, env template, README. |
| `bin/quadlet-health` | The health check (241 lines, argc script). |
| `bin/pg-backup`, `bin/termix-backup` | Nightly backups (argc scripts). |
| `bin/env-from-example`, `bin/postgres-password`, `bin/credential-key`, `bin/container-env` | Helpers the setup tasks use to write env files. |
| `bin/loopback-listen.cjs` | Node preload that binds a port-only `listen()` to `127.0.0.1`. |
| `units/` | Plain systemd units: `quadlet-health` and `pg-backup`, each with a timer and a failure-notification service. |
| `.codex/config.toml` | One MCP server URL for Codex. |
| `SKOGAI.sh` | One line: a todo note, not a script. |

## How it works

### Network model

`docs/networking.md` describes two worlds joined only by tunnels. Containers form a closed network world and are reached from outside through the Cloudflare tunnel `skognet-cloudflare`. Host tools may reach a container only through a port published on `127.0.0.1`. System-level `*-service` tunnels are run by system `cloudflared` and are not part of this repo.

Each service has its own `.network` quadlet. A container joins a second network only where a name lookup is needed, and each such link is declared with a comment `# bridge: <caller> -> <callee>` above the `Network=` line (`mcphub/skogai-mcphub.container:13-16`, `termix/termix.container:18-19`). The tunnel connector reaches `skogai-mcphub` and `termix` by container name over `skognet-cloudflare.network`.

### Services

- **`skognet-cloudflare`**: `cloudflare/cloudflared` running `tunnel --no-autoupdate run`. The tunnel is selected by `TUNNEL_TOKEN` from the env file (`skognet-cloudflare.container:10-15`). It has a fixed IP, and the network pins the subnet and restricts dynamic leases so no other container takes that address (`skognet-cloudflare.network`).
- **`skogai-mcphub`**: `samanhappy/mcphub`, no published port, requires `skogai-mcphub-postgres.service`. Served as `mcp.skogai.se` through the tunnel (`mcphub/README.md`).
- **`mcphub-postgres`** and **`basic-memory-postgres`**: `pgvector/pgvector:pg17` with named volumes and health commands. The basic-memory database publishes `127.0.0.1:5432` for the host-side `basic-memory` tool, which is installed with `uv tool` and is not a container.
- **`termix`**: web SSH manager, image pinned by tag and digest. It publishes `127.0.0.1:8080`, mounts `termix/hosts-config/` read-only, and trusts `X-Forwarded-For` only from the connector's fixed IP (`termix.container:28-32`). Registration, password reset and unsigned plugins are locked by environment variables (`:33-38`). `hosts.yaml` is the source of truth for hosts and shares one folder with user `claude`.

Every unit with `Restart=` also sets `StartLimitIntervalSec=300` and `StartLimitBurst=10`, so a broken unit ends in `failed` instead of looping.

### Health check

`bin/quadlet-health` runs the generator dry run, then prints one row per generated unit with its systemd state and an expected state: `boot`, `bound`, `manual` or `dep` (`quadlet-health:4-13`). It exits 2 when the generator fails, when a unit joins a bare-named network (`:69`) or sets `Restart=` without a start limit (`:83`). It exits 1 when a boot unit is not active, a backup is missing or older than `PG_BACKUP_MAX_AGE_HOURS` (`:132`), a declared bridge name does not resolve (`:165-188`), the tunnel has zero connections (`:207`), or a tunnel ingress hostname answers with a connection error or 502 and above (`:201-223`). The hostname list is read live with `cf tunnels config get`; nothing is committed. Rows that cannot be checked print `skip`. `units/quadlet-health.timer` runs it hourly and a failure sends a desktop notification.

### Backups

`units/pg-backup.timer` fires at 03:30 and runs `bin/pg-backup` then `bin/termix-backup`. The first writes one gzipped `pg_dump` per Postgres container to `~/backups/pg` and prunes dumps older than `PG_BACKUP_KEEP_DAYS` (`pg-backup:16-38`). The second tars the `termix-data` volume to `~/backups/termix`; the archive includes Termix's own key file, so archives are secrets (`termix-backup:5-8`).

### Setup and secrets

`mise run setup` depends on the three `setup:*` tasks, then reloads systemd and runs the health check (`mise-tasks/setup/_default`). Each task writes a missing `*.env` from its `.example` through `bin/env-from-example`, which never overwrites an existing file and writes mode 600. `bin/postgres-password` reuses the password of a running container or saved env file and refuses to generate one when a volume exists with an unknown password. `bin/credential-key` does the same for `MCPHUB_CREDENTIAL_ENCRYPTION_KEY`, generating only while the `credential_bindings` table is empty. `setup:cloudflare` fetches `TUNNEL_TOKEN` with `cf tunnels token get "$SKOGNET_TUNNEL_ID"`.

## How to use it

Prerequisites, per `SECRETS.md` and `SKOGAI.md`: clone to `~/.config/containers/systemd`, `mise trust`, rootless podman, `argc` from mise, `cf` logged in, `jq`, `openssl`. Run everything as the owning user without `sudo`.

| Command | Does |
|---|---|
| `mise run setup` | Write missing env files, reload units, run the health check, then log in the mcphub CLI profiles. Does not start containers or install timers. |
| `mise run setup:<cloudflare\|mcphub\|basic-memory>` | One part of setup. |
| `bin/quadlet-health` | One-shot health check. |
| `/usr/lib/systemd/user-generators/podman-user-generator -user -dryrun` | Inspect generated units. |
| `systemctl --user daemon-reload` | Regenerate units after an edit. |
| `mise run mcphub:seed`, `mise run mcphub:dev` | Copy prod settings without users, then run a file-mode hub on `127.0.0.1:3000`. |

Rules from `SKOGAI.md`: control services with `systemctl --user`, never `podman stop` or `podman rm`. To keep a service off, remove its `[Install]` section and commit. The timers are installed by hand with `systemctl --user link` and `enable --now`; the commands are in `SKOGAI.md`.

Secrets by name: `TUNNEL_TOKEN`; `JWT_SECRET`, `DB_URL`, `ADMIN_PASSWORD`, `MCPHUB_CREDENTIAL_ENCRYPTION_KEY`; `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` (twice); `TERMIX_API_KEY` in `termix/termix-claude.env`. Agents use Termix as user `claude` through that API key (`termix/README.md`).

## Relations to other SkogAI repos

- **cloudflare**: same account pin (`CLOUDFLARE_ACCOUNT_ID`), same `cf` CLI. This repo runs the connector for tunnel `skognet-cloudflare`; the cloudflare repo's scripts and TODO manage that tunnel's ingress, DNS and Access. `PLAN.md` records ingress and DNS cleanup done from here with `cf`.
- **dash-skogai**: `PLAN.md` phase 5 plans a `fnox.toml` with an age provider and names the age recipients in `~/.local/src/dash-skogai/fnox.toml`.
- **dotfiles**: `SECRETS.md` says the repo is registered in gita through `~/.dotfiles/config/gita/repos.csv`.
- **Removed services**: `SECRETS.md` and `PLAN.md` name skogchattr, paperclip, agentchattr, agentbot, pangolin and termix-guacd as pruned. Their checkouts lived under `~/.local/src/`.
- **Conventions**: router-style `AGENTS.md` with `<routes>` and `permalink` frontmatter, `SKOGAI.md` as the guide, `.skogai/logs/log.jsonl` hook log, argc scripts in `bin/`, mise file tasks.
- **Machine assumptions**: hostname `skogix-workstation`, user home paths, `notify-send` for alerts, an Omarchy desktop.

## Gaps and stale references

- `SECRETS.md` states there is no backup of the gitignored env files. Phase 5 of `PLAN.md` (fnox with age) would fix that and is on hold; tasks 5.1-5.7 and the "who decrypts" question are open.
- `SECRETS.md` carries a security note dated 2026-10-09: a branch of the public `skogai/skogchattr` repo contains a committed credentials file with a live token pair, to be revoked and scrubbed. The repo does not say whether that was done.
- `PLAN.md` notes that a `cf` OAuth token was once committed here and later untracked. It may remain in git history; not checked.
- `SKOGAI.md` mentions `*.build` files and `config.toml.example`. Neither exists in the tree.
- `PLAN.md` says `docs/networking.md` is linked from `AGENTS.md` and `CLAUDE.md`. There is no `CLAUDE.md`, and `AGENTS.md` only routes to `SKOGAI.md`.
- `SKOGAI.md` has `permalink: skogai/skogai`, which looks copied from another repo.
- The progress log notes that hostnames behind Access return 302 and count as up, so the check cannot see a dead origin behind Access.
- `termix/README.md`: the second factor is off "to revisit", and the Termix Access app was deleted on 2026-11-14, so the Termix password and API key are the only gates on `termix.skogai.se`.
- `mise.toml` says the login spans five accounts; the cloudflare repo says six.
- `docs/networking.md`, `mcphub/skogai-mcphub.env.example` and the lower half of `bin/quadlet-health` were read in outline only.
