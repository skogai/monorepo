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
