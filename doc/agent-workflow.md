# Working on this repository

Instructions for every agent working on this repository itself, whichever model and harness you run in. What the repository is and how to fetch a catalog repo: [AGENTS.md](../AGENTS.md).

It is at an early stage. There is no application code, no chosen language, and no root CI. Do not invent build, lint, or test commands. The commands that exist are in `mise.toml`, `.config/mise/conf.d/*.toml`, and `repos/mise-plugin/mise.toml` once that repo is cloned.

Start from the [README](../README.md), then read the [decisions](adr/). The plan and current work are GitHub issues on the [project board](https://github.com/orgs/skogai/projects/4); its README gives the order and the owner's direction.

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

The goal is to use mise as much as possible. A tool or dependency that mise can install is free to use and comes first. Before you write tooling, rules, or a workflow of your own, look for a mise tool that already does the job. For example, manage decision records with `adr-tools` through mise instead of inventing a format and process. [ADR 0001](adr/0001-starting-tools.md) records this.

## Many agents, many environments

The same task is routinely given to several agents at once. So far that has meant Claude, Codex, and Gemini, each in its own harness, each on a different machine, all with the same prompt. Each run delivers one pull request against `master`. The owner then compares the runs and merges them.

Your output will be read next to other agents' output for the same task, produced on machines that are configured differently from yours. Write it so the comparison is possible:

1. **Identify the run.** State the agent, harness, machine, checkout path, and base commit in the pull request description and in any evidence you record. Name the branch so the agent and machine are visible, as in `t3/claude-laptop`.
2. **Separate what you read from what you ran.** A source observation is not a passing test. For each claim say which it is, and list what you did not run.
3. **Say where each fact lives.** A fact comes from tracked files in this repository, from a cloned repo under `repos/`, or from the machine: `~/.config/mise`, `/etc/mise`, dotfiles, operating system packages, installed tools. A machine fact holds for that machine only. Other agents may not be able to see it or reproduce it.
4. **Make machine dependencies explicit.** If a step needs anything outside the checkout, record it as a prerequisite. A check that passes on one workstation does not show the setup is reproducible.
5. **Do not turn proposals into decisions.** Decisions are the records in `doc/adr/`. Research notes, files removed from Git history, and tools that happen to be installed outside mise are inputs. If something is undecided, list it as an open question.
6. **Keep the shared layout.** Put files where the table below says, so that parallel runs produce diffs of the same paths.
7. **Deliver a pull request and stop.** When several agents run the same task, the owner's comparison is input, so open a pull request and leave merging to the owner (see Delivering work). Leave other agents' branches and pull requests alone.

## Where things live

| Path | Holds |
|---|---|
| `README.md` | Entry point. Setup commands go here once they are verified. |
| `AGENTS.md` | The map: what this repository is and how to fetch a catalog repo. |
| `CLAUDE.md` | One line that imports `AGENTS.md`, so Claude Code loads it. A harness that reads neither file needs its own pointer here. |
| GitHub issues and [project 4](https://github.com/orgs/skogai/projects/4) | The plan and current work. Not in Git: update the issue, not a file. |
| `doc/adr/` | Decisions, as Context / Decision / Consequences with a status. |
| `.skogai/research/` | Research inputs, kept as written by the agent that produced them. |
| `.skogai/tests/` | Dated experiment records: what was run, where, and the result. |
| `mani.yaml` | The catalog of SkogAI repos: name, path and URL of each. |
| `repos/<name>/` | Clones of catalog repos, made with `mani sync -t <name> --ignore-sync-state`. Ignored by Git. |
| `agents/<name>.md` | Cached copy of each catalog repo's root `AGENTS.md`, readable without cloning. A repo with no root `AGENTS.md` has no file. Refresh by hand with `mise run agents:sync` and commit the diff. |
| `repos/skogix/.skogai/todo.list` | The owner's backlog (needs `mani sync -t skogix --ignore-sync-state`). |

## Fetching a catalog repo

Every project in `mani.yaml` has `sync: false` and a tag equal to its name, so nothing is cloned until someone asks. Clone one with `mani sync -t <name> --ignore-sync-state`; an unknown name fails with `cannot find tags`. Do not use `-d`: it matches path prefixes, so `-d repos/skogai` also clones `skogai-core` and `skogai-jq`. `mani sync --status` shows what is cloned. `mani.yaml` does not maintain `.gitignore`; `/repos/` is written there by hand.

- **Container.** `mise install mani` gives the pinned mani. If mise or the release download is not available, the baseline still holds with git alone: `git clone <url> repos/<name>`, with the URL from `mani.yaml`. All listed repos are public, so no credentials are needed to read. In a non-interactive container set `GIT_TERMINAL_PROMPT=0` so a repo that needs credentials fails instead of waiting at a prompt. Not yet run in a real container.
- **Read-only.** Reading is the baseline; a push or a pull request against a child works only when the environment's credentials allow it. mani adds no handling: a failed `git push` in the child is the sign. `git -C repos/<name> push --dry-run` may show it in advance (not verified).

## Recording evidence

Add to the dated file in `.skogai/tests/`. For each entry give the date, the run (agent, machine, checkout, commit), the exact command, the expected result, the actual result, a verdict of pass, fail, blocked, or not run, and the decision or next action. Keep failures; they are evidence.

## Secrets

Do not write credentials, tokens, or full environment dumps into files, logs, commit messages, or pull requests. Check `git status` before every commit.
