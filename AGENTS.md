# AGENTS.md

Instructions for every agent working in this repository, whichever model and harness you run in.

## What this repository is

`skogai/monorepo` is the SkogAI 3.0 base: the generic setup that should always work and follow the simplest intended workflow. It is a root repository with three Git submodules (`skogai`, `skogix`, `mise-plugin`), configured with mise.

It is at an early stage. There is no application code, no chosen language, and no root CI. Do not invent build, lint, or test commands. The commands that exist are in `mise.toml`, `.config/mise/conf.d/*.toml`, and `mise-plugin/mise.toml`.

Start from the [README](README.md), then read the [decisions](doc/adr/). The plan and current work are GitHub issues on the [project board](https://github.com/orgs/skogai/projects/4); its README gives the order and the owner's direction.

## Starting a session: "hi"

When the owner opens a session with just "hi" (or a similar bare greeting), it means: present the next thing on the list. Do this:

1. Run `mise run next`. It lists open pull requests, project 4 items in progress, and the first open item per track (`roadmap`, `mise-toolkit`, `backlog`).
2. Present the state briefly. Open pull requests come first: they are waiting on review or merge. Then work in progress, then the next item per track.
3. Recommend one next item, following the order in the project 4 README. Say whether it suits a subagent: a self-contained issue with a clear checklist, no open pull request touching it, and no open decision that needs the owner. If it does not, say what is blocking it or what the owner must decide.
4. Stop and wait. Do not start work or spawn a subagent until the owner picks.

## Delivering work

Work on a branch, then decide how it lands:

- **Input needed: open a pull request and stop.** Input is needed when the change has an open question, makes or changes a decision (an ADR), cannot be verified on this machine, or is one of several parallel runs of the same task. Put the questions in the pull request description.
- **No input needed: merge to `master`.** Open the pull request for the record, squash-merge it, and delete the branch. The change must be verified, with the checks you ran stated in the pull request.

When unsure, treat it as input needed.

## Prefer mise

The goal is to use mise as much as possible. A tool or dependency that mise can install is free to use and comes first. Before you write tooling, rules, or a workflow of your own, look for a mise tool that already does the job. For example, manage decision records with `adr-tools` through mise instead of inventing a format and process. [ADR 0001](doc/adr/0001-starting-tools.md) records this.

## mise configuration and conf.d

Read [the mise guide](doc/mise.md) before changing configuration. Keep shared root policy in `mise.toml` and environment-specific tools, variables and tasks in `.config/mise/conf.d/<name>.<env>.toml`. T3 variables and playground tasks live together in `setup.t3.toml`; do not recreate `mise.t3.toml`.

- `.miserc.toml` is read before configuration discovery. It selects `skogai` by default and enables `env_conf_d = true`. Keep that setting there, not in a mise `[env]` table.
- With that setting, `<name>.toml` is shared and `<name>.<env>.toml` loads only for the selected environment. Avoid dots in the fragment's name itself; use hyphens.
- `mise -E t3` replaces the default selection. Use `mise -E skogai,t3` to combine environments; later selected environments win conflicts.
- Shared conf.d fragments load alphabetically before root `mise.toml`; environment fragments override base configuration. Keep personal overrides in ignored `mise.local.toml` or `mise.<env>.local.toml`, rather than editing shared fragments.
- `{{config_root}}` in these project fragments identifies the checkout root. Keep checkout-relative paths templated and verify them after moving configuration.
- Inspect discovery with `mise -E t3 cfg` and task availability with `mise -E t3 tasks ls`. Use `mise -E t3 run t3:info` to check paths without starting a server. Also check default and combined selections.
- Global/system mise configuration and installed tools still apply. Record those machine prerequisites; conf.d organization does not provide isolation. Never dump the full environment as validation.

Upstream reference: [mise configuration](https://mise.jdx.dev/configuration.html).

## Many agents, many environments

The same task is routinely given to several agents at once. So far that has meant Claude, Codex, and Gemini, each in its own harness, each on a different machine, all with the same prompt. Each run delivers one pull request against `master`. The owner then compares the runs and merges them.

Your output will be read next to other agents' output for the same task, produced on machines that are configured differently from yours. Write it so the comparison is possible:

1. **Identify the run.** State the agent, harness, machine, checkout path, and base commit in the pull request description and in any evidence you record. Name the branch so the agent and machine are visible, as in `t3/claude-laptop`.
2. **Separate what you read from what you ran.** A source observation is not a passing test. For each claim say which it is, and list what you did not run.
3. **Say where each fact lives.** A fact comes from tracked files in this repository, from a submodule, or from the machine: `~/.config/mise`, `/etc/mise`, dotfiles, operating system packages, installed tools. A machine fact holds for that machine only. Other agents may not be able to see it or reproduce it.
4. **Make machine dependencies explicit.** If a step needs anything outside the checkout, record it as a prerequisite. A check that passes on one workstation does not show the setup is reproducible.
5. **Do not turn proposals into decisions.** Decisions are the records in `doc/adr/`. Research notes, files removed from Git history, and tools that happen to be installed outside mise are inputs. If something is undecided, list it as an open question.
6. **Keep the shared layout.** Put files where the table below says, so that parallel runs produce diffs of the same paths.
7. **Deliver a pull request and stop.** When several agents run the same task, the owner's comparison is input, so open a pull request and leave merging to the owner (see Delivering work). Leave other agents' branches and pull requests alone.

## Where things live

| Path | Holds |
|---|---|
| `README.md` | Entry point. Setup commands go here once they are verified. |
| `AGENTS.md` | This file. |
| `CLAUDE.md` | One line that imports this file, so Claude Code loads it. A harness that reads neither file needs its own pointer here. |
| GitHub issues and [project 4](https://github.com/orgs/skogai/projects/4) | The plan and current work. Not in Git: update the issue, not a file. |
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
