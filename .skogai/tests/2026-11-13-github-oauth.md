# 2026-11-13: GitHub OAuth for mise

Run: Claude Opus 5.5, Claude Code CLI, machine `skogix-laptop`, checkout `/home/skogix/Work`, base commit `d918585`, mise 2026.11.7 linux-x64.

Everything here is a machine fact. The configuration is in `~/.config/mise/config.toml`, outside this repository.

| Command | Expected | Actual | Verdict |
|---|---|---|---|
| `mise settings ls` (before) | No `github.oauth_client_id` set, or a valid one | `github.oauth_client_id = "ls"`, a placeholder | fail, fixed below |
| `mise token github` (before) | A token source | `github.com: (none)` | fail |
| The owner created a GitHub App with device flow enabled and installed it | A client ID | `Iv23liQkKChCS4oXgq10` | pass (done by the owner) |
| `sed` on `~/.config/mise/config.toml`, then `mise settings get github.oauth_client_id` | The new client ID | `Iv23liQkKChCS4oXgq10` | pass |
| `env` checked for `MISE_GITHUB_TOKEN`, `GITHUB_API_TOKEN`, `GITHUB_TOKEN`, `GH_TOKEN` | None set, so none overrides OAuth | None set | pass |
| `mise token github --oauth` (run by the owner) | Device flow completes | Completed; output not recorded | pass |
| `mise token github` (run by the owner) | `source: GitHub OAuth` | `github.com: ghu_…(masked) (source: GitHub OAuth)` | pass |

## Not run

- `mise token github --oauth --refresh`.
- Any other machine.
- Checking that `GITHUB_TOKEN` is exported in an activated shell.

## Next action

None. AGENTS.md now describes the setup as a machine prerequisite.
