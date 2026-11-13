# Shared T3 configuration

2026-11-13. Codex in Codex Desktop on `skogix-workstation`, checkout
`/home/skogix/Work`, base `d36b1485e6c77ef8a358e704c5b2a74e0590f033`.

The tracked shared fragment uses the installed CLI from PATH, state in
`/home/skogix/Work/.t3`, and port 3773. This run used mise 2026.11.5 and T3 v0.1.9.

| Command | Expected | Actual and verdict |
| --- | --- | --- |
| `mise run t3:info` | Load T3 tasks by default | Work project, `/home/skogix/Work/.t3`, port 3773. Pass. |
| `mise -E develop run t3:info` | Load the same tasks with an explicit environment | Same paths and port. Pass. |
| `MISE_ENV= mise run t3:info` | Load the same tasks with an empty selection | Same paths and port. Pass. |
| `mise exec -- which t3` | Resolve the workstation CLI | `/home/skogix/.local/bin/t3`. Pass. |
| `PYTHONDONTWRITEBYTECODE=1 python3 .skogai/tests/test_t3_picker.py` | Pass picker tests | Four passed. |
| `mise run t3:health` | Connect to the configured port | Connection refused. Blocked by the stopped server. |

Browser pairing and a live agent turn were not run. Start the installed
T3 instance before checking live workflows.

## Shared backend follow-up

Same checkout and workstation, starting from `166529c`. The tracked base
moved from `/home/skogix/Work/.t3` to `/home/skogix/Work/t3`. With no T3
listener or native T3 unit present, the stopped checkout-local state was
copied to the new base. Runtime files are ignored.

| Command | Expected | Actual and verdict |
| --- | --- | --- |
| `bash -n t3/install-service.sh` | Valid installer syntax | Exit 0. Pass. |
| `systemd-analyze --user verify "$PWD/t3/skogai-t3.service"` | Valid unit | Exit 0. Pass. |
| `./t3/install-service.sh` | Install, enable and start the backend | Enabled and started. Pass. |
| `systemctl --user show skogai-t3 -p ActiveState -p SubState -p WorkingDirectory` | Active and running from `/home/skogix/Work/t3` | As expected. Pass. |
| `mise run t3:health` | HTTP 200 after startup | HTTP 200 after initial connection refusals and one HTTP 503. Pass. |
| `mise run t3:projects` | Existing Monorepo project | Listed at `/home/skogix/Work`. Pass. |
| `t3 pair --base-dir /home/skogix/Work/t3 --label 'Codex Browser'` | Pair browser to the backend | Browser accepted token and showed Monorepo. Pass. |

User lingering was already enabled on this workstation. Reboot, remote
pairing and a live agent turn were not tested.

## Native service and Tailscale pairing

Same workstation and checkout, base `8715293`, Codex Desktop. Both
`skogai-t3.service` and `t3code.service` were enabled and active, but
`ss -ltnp '( sport = :3773 )'` showed only the custom unit's process listening.
Stopped and disabled the custom unit, then restarted `t3code.service` using
the existing `Work/t3` native configuration.

| Command | Expected | Actual and verdict |
| --- | --- | --- |
| `./t3/install-service.sh` | Retain the native service and disable the custom unit | Native service already installed and enabled. Pass. |
| `mise run t3:health` | Native backend responds | HTTP 200. Pass. |
| `mise run t3:threads` | Existing thread remains available | One thread. Pass. |
| `t3 pair --base-dir "$PWD/t3" --tailscale --label 'Codex Browser verification'` | HTTPS pairing URL for this backend | Opened in the browser and reached Monorepo. Pass. |

Tailscale Serve was already configured on the workstation. Pairing from a
second physical device, reboot and an agent turn were not run.
