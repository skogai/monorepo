# AGENTS.md

Instructions for every agent working in this repository, whichever model and harness you run in.

## What this repository is

`skogai/monorepo` is the SkogAI 3.0 base: the generic setup that should always work and follow the simplest intended workflow. It is a root repository with three Git submodules (`skogai`, `skogix`, `mise-plugin`), configured with mise.

It is at an early stage. There is no application code, no chosen language, and no root CI. Do not invent build, lint, or test commands. The commands that exist are in `mise.toml` and `mise-plugin/mise.toml`.

Start from the [README](README.md), then read the [plan](doc/plan.md) and the [decisions](doc/adr/).

## Many agents, many environments

The same task is routinely given to several agents at once. So far that has meant Claude, Codex, and Gemini, each in its own harness, each on a different machine, all with the same prompt. Each run delivers one pull request against `master`. The owner then compares the runs and merges them.

Your output will be read next to other agents' output for the same task, produced on machines that are configured differently from yours. Write it so the comparison is possible:

1. **Identify the run.** State the agent, harness, machine, checkout path, and base commit in the pull request description and in any evidence you record. Name the branch so the agent and machine are visible, as in `t3/claude-laptop`.
2. **Separate what you read from what you ran.** A source observation is not a passing test. For each claim say which it is, and list what you did not run.
3. **Say where each fact lives.** A fact comes from tracked files in this repository, from a submodule, or from the machine: `~/.config/mise`, `/etc/mise`, dotfiles, installed tools. A machine fact holds for that machine only. Other agents may not be able to see it or reproduce it.
4. **Make machine dependencies explicit.** If a step needs anything outside the checkout, record it as a prerequisite. A check that passes on one workstation does not show the setup is reproducible.
5. **Do not turn proposals into decisions.** Decisions are the records in `doc/adr/`. Research notes, files removed from Git history, and tools that happen to be installed are inputs. If something is undecided, list it as an open question.
6. **Keep the shared layout.** Put files where the table below says, so that parallel runs produce diffs of the same paths.
7. **Deliver a pull request and stop.** Leave merging to the owner. Leave other agents' branches and pull requests alone.

## Where things live

| Path | Holds |
|---|---|
| `README.md` | Entry point. Setup commands go here once they are verified. |
| `AGENTS.md` | This file. |
| `doc/plan.md` | The current working plan. |
| `doc/adr/` | Decisions, as Context / Decision / Consequences with a status. |
| `.skogai/research/` | Research inputs, kept as written by the agent that produced them. |
| `.skogai/tests/` | Dated experiment records: what was run, where, and the result. |
| `skogix/.skogai/todo.list` | The owner's backlog. |

`skogix` is a private repository. A run without access to it cannot read the backlog, and should say so.

## Recording evidence

Add to the dated file in `.skogai/tests/`. For each entry give the date, the run (agent, machine, checkout, commit), the exact command, the expected result, the actual result, a verdict of pass, fail, blocked, or not run, and the decision or next action. Keep failures; they are evidence.

## Secrets

Do not write credentials, tokens, or full environment dumps into files, logs, commit messages, or pull requests. The repository currently has no `.gitignore`, so check `git status` before every commit.
