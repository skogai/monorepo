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

## Write access (later the same day)

Run: as above, base commit `449745b`.

| Command | Expected | Actual | Verdict |
|---|---|---|---|
| `gh auth status` | Find which token gh uses | The active account comes from `GITHUB_TOKEN` (the mise OAuth `ghu_` token). The keyring `gho_` login is inactive. | observed |
| `gh api /user/installations` | App permissions | `contents: read`, `metadata: read` on Skogix, skogai, skogai2 | observed |
| `git push --dry-run origin HEAD:refs/heads/zz-auth-probe` with `GITHUB_TOKEN` set | Push allowed | `403 Permission to skogai/monorepo.git denied to Skogix` | fail |
| The same command with `GITHUB_TOKEN` unset | Push allowed through the keyring login | `[new branch]` (dry run, nothing created) | pass |
| The owner gave the App Contents, Pull requests, Workflows and Issues read and write, accepted on all three installations, and ran `mise token github --oauth --refresh` | New permissions | Done by the owner | pass |
| `gh api /user/installations` and `git push --dry-run …` in a shell that still held the old token | Allowed | `401 Bad credentials`: the refresh revoked the old token | fail |
| `unset GITHUB_TOKEN`, then `mise token github` | `source: GitHub OAuth`, new token | `ghu_…(masked) (source: GitHub OAuth)` | pass |
| `gh api /user/installations` | Write permissions | `contents`, `issues`, `pull_requests`, `workflows`: write; `metadata`: read, on all three | pass |
| `git push --dry-run origin HEAD:refs/heads/zz-auth-probe` | Push allowed | `[new branch]` (dry run, nothing created) | pass |

Not run: a real push or `gh pr create` with the new token before this PR. Opening this PR is that test.

## Next action

None. AGENTS.md now describes the setup as a machine prerequisite.
