# AGENTS.md

Instructions for every agent working in this repository, whichever model and harness you run in.

## What this repository is

`skogai/monorepo` is the SkogAI 3.0 base: the generic setup that should always work and follow the simplest intended workflow. It is a root repository with three Git submodules (`skogai`, `skogix`, `mise-plugin`), configured with mise.

It is at an early stage. There is no application code, no chosen language, and no root CI. Do not invent build, lint, or test commands. The commands that exist are in `mise.toml` and `mise-plugin/mise.toml`.

Start from the [README](README.md), then read the [plan](doc/plan.md) and the [decisions](doc/adr/).

## Prefer mise

The goal is to use mise as much as possible. A tool or dependency that mise can install is free to use and comes first. Before you write tooling, rules, or a workflow of your own, look for a mise tool that already does the job. For example, manage decision records with `adr-tools` through mise instead of inventing a format and process. [ADR 0001](doc/adr/0001-starting-tools.md) records this.

## Many agents, many environments

The same task is routinely given to several agents at once. So far that has meant Claude, Codex, and Gemini, each in its own harness, each on a different machine, all with the same prompt. Each run delivers one pull request against `master`. The owner then compares the runs and merges them.

Your output will be read next to other agents' output for the same task, produced on machines that are configured differently from yours. Write it so the comparison is possible:

1. **Identify the run.** State the agent, harness, machine, checkout path, and base commit in the pull request description and in any evidence you record. Name the branch so the agent and machine are visible, as in `t3/claude-laptop`.
2. **Separate what you read from what you ran.** A source observation is not a passing test. For each claim say which it is, and list what you did not run.
3. **Say where each fact lives.** A fact comes from tracked files in this repository, from a submodule, or from the machine: `~/.config/mise`, `/etc/mise`, dotfiles, operating system packages, installed tools. A machine fact holds for that machine only. Other agents may not be able to see it or reproduce it.
4. **Make machine dependencies explicit.** If a step needs anything outside the checkout, record it as a prerequisite. A check that passes on one workstation does not show the setup is reproducible.
5. **Do not turn proposals into decisions.** Decisions are the records in `doc/adr/`. Research notes, files removed from Git history, and tools that happen to be installed outside mise are inputs. If something is undecided, list it as an open question.
6. **Keep the shared layout.** Put files where the table below says, so that parallel runs produce diffs of the same paths.
7. **Deliver a pull request and stop.** Leave merging to the owner. Leave other agents' branches and pull requests alone.

## Where things live

| Path | Holds |
|---|---|
| `README.md` | Entry point. Setup commands go here once they are verified. |
| `AGENTS.md` | This file. |
| `CLAUDE.md` | One line that imports this file, so Claude Code loads it. A harness that reads neither file needs its own pointer here. |
| `doc/plan.md` | The current working plan. |
| `doc/adr/` | Decisions, as Context / Decision / Consequences with a status. |
| `.skogai/research/` | Research inputs, kept as written by the agent that produced them. |
| `.skogai/tests/` | Dated experiment records: what was run, where, and the result. |
| `skogix/.skogai/todo.list` | The owner's backlog. |

## Recording evidence

Add to the dated file in `.skogai/tests/`. For each entry give the date, the run (agent, machine, checkout, commit), the exact command, the expected result, the actual result, a verdict of pass, fail, blocked, or not run, and the decision or next action. Keep failures; they are evidence.

## GitHub authentication for mise

mise calls the GitHub API to resolve and download tools. Without a token those calls hit the anonymous rate limit. To see which token mise uses and where it came from, run `mise token github`. It masks the token. Do not use `--unmask` or `--raw` in logs, files, or pull requests.

mise uses the first token it finds, in this order:

1. `MISE_GITHUB_ENTERPRISE_TOKEN`, for enterprise hosts
2. `MISE_GITHUB_TOKEN`, then `GITHUB_API_TOKEN`, then `GITHUB_TOKEN`
3. `github.credential_command`
4. Native GitHub OAuth
5. `github_tokens.toml`
6. The gh CLI `hosts.yml`
7. `git credential fill`, when `github.use_git_credentials` is on

The repository's `mise.toml` sets the client ID of the owner's GitHub App, `skogix-mise`, which has device flow enabled:

```toml
[settings.github]
oauth_client_id = "Iv23liQkKChCS4oXgq10"
```

A different App can be used on a machine without editing the file. Set `MISE_GITHUB_OAUTH_CLIENT_ID` in the shell; it overrides the file. A `MISE_GITHUB_OAUTH_CLIENT_ID` in a mise `[env]` table does not work, because mise does not read its own settings from `[env]`. Each machine still needs a person to authorize it once.

The same token is also used for `git push` and `gh`. mise exports it as `GITHUB_TOKEN`, gh prefers `GITHUB_TOKEN` over its own login, and the git credential helper is `gh auth git-credential`. So the App needs these repository permissions, granted on every installation (Skogix, skogai, skogai2):

| Permission | Access | Used for |
|---|---|---|
| Metadata | Read | Required by GitHub |
| Contents | Read and write | Tool downloads, `git push` |
| Pull requests | Read and write | `gh pr` |
| Workflows | Read and write | Pushing changes under `.github/workflows/` |
| Issues | Read and write | `gh issue` |

With read-only Contents, `git push` fails with `403 Permission … denied`.

A client ID is not a secret. The OAuth token mise caches is a secret. To set this up on another machine:

1. Trust the checkout with `mise trust`.
2. Run `mise run github:auth` and approve the device code in a browser. This step needs a person. The same task refreshes the token later.
3. Check that the task output reports `source: GitHub OAuth`.

While a token is cached, mise exports it as `GITHUB_TOKEN` through `mise activate`, `mise exec` and `mise env`. The `github.oauth_export_env` setting changes the variable name, and `""` turns the export off. A `GITHUB_TOKEN` you set yourself sits higher in the order, so mise will use it instead of OAuth. After you change the app's permissions or installations, run `mise run github:auth`. The refresh revokes the old token. A shell that still holds the old token gets `401 Bad credentials` until mise updates the variable at the next prompt, or until you run `unset GITHUB_TOKEN`. Documentation: <https://mise.jdx.dev/dev-tools/github-tokens.html>.

## Secrets

Do not write credentials, tokens, or full environment dumps into files, logs, commit messages, or pull requests. The repository currently has no `.gitignore`, so check `git status` before every commit.
