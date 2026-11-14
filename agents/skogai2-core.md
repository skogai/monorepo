# skogai/core — Agent Entrypoint

**Generated:** 2026-08-22
**Commit:** `4166a81`
**Branch:** `master`

## OVERVIEW

| intent                                | go to                                                          |
| ------------------------------------- | -------------------------------------------------------------- |
| understand file layout                | [`FILESTRUCTURE.md`](FILESTRUCTURE.md)                         |
| current direction and near-term work  | [`PLAN.md`](PLAN.md)                                           |
| human-readable overview               | [`README.md`](README.md)                                       |
| command source                        | [`Argcfile.sh`](Argcfile.sh) / `scripts/argc/skogai` (symlink) |
| dependency and bootstrap expectations | [`docs/dependencies.md`](docs/dependencies.md)                 |
| backlog and deferred ideas            | [`todo.list`](todo.list)                                       |
| why a hard-to-reverse decision was made | [`docs/decisions/`](docs/decisions/)                          |
`skogai/core` is the SkogAI fleet control plane: it discovers, registers, inspects, and prepares repository work contexts. Keep project-specific commands in their target repository or generated worktree helper.

## STRUCTURE

```text
.
├── Argcfile.sh       # source for the fleet-control CLI
├── scripts/          # bootstrap, build, and context emitters
├── docs/             # dependency notes plus captured tool references
├── settings/         # global-tool configuration references
├── tests/            # root argc parser smoke test
├── bin/              # committed generated wrapper
└── tmp/              # scratch builds, man pages, and live context
```

## WHERE TO LOOK

| Task | Location | Notes |
|---|---|---|
| Command behavior | `Argcfile.sh` | `repo::*` orchestrates; `tools::*` wraps curated CLIs. |
| Command conventions | `.claude/live-rules/rules/argc-conventions.md` | Argc tags own parsing and validation; injected automatically when editing `Argcfile.sh`/`scripts/argc/**`. |
| Build outputs | `scripts/build.sh` | Builds from `scripts/argc/skogai` → `Argcfile.sh`. |
| Worktree setup | `scripts/bootstrap.sh`, `.config/wt.toml` | Shared environment path for direnv and Worktrunk. |
| Context payloads | `scripts/context/` | `repo workon` / `repo review` populate `tmp/context/`. |
| Environment boundaries | `docs/dependencies.md` | Separates machine CLIs from Python maintenance dependencies. |
| Direction and layout | `PLAN.md`, `FILESTRUCTURE.md` | Keep root all-caps files short and link-oriented. |

## CODE MAP

| Surface | Location | Role |
|---|---|---|
| Fleet CLI | `Argcfile.sh` | Declares `repo`, `marketplace`, and `tools` command trees. |
| Work-context flow | `repo::workon`, `_repo_review_pr` | Switches worktrees and writes the context bundle. |
| Generated wrapper | `scripts/build.sh` | Produces `bin/skogai`, scratch binary, man pages, and completions. |
| Parser contract | `tests/argc-smoke.sh` | Checks help and selected argc function names. |

Reference counts are unmeasured: this repository has no usable codegraph symbols and Bash LSP is not installed.

## CONVENTIONS

- `AGENTS.md` is a symlink to this file; edit `SKOGAI.md` and preserve the link.
- `scripts/argc/skogai` is a symlink to `Argcfile.sh`; keep source and build path aligned.
- Define CLI parsing, defaults, required values, and choices through argc annotations, not command-body bash.
- Use `repo::*` for fleet concepts and `tools::*` only for curated tool-specific escape hatches.
- `.envrc` owns bootstrap and build activation; `settings/` holds global-tool references, not root command logic.

## ANTI-PATTERNS (THIS PROJECT)

- Do not turn this repository into a generic project helper.
- Do not edit `bin/skogai` or new `tmp/` artifacts as source; rebuild or explicitly promote them.
- Do not hand-roll argc validation, defaulting, dispatch, or dependency checks already expressible in annotations.
- Never `chmod +x` an argc script; invoke it through `argc`.
- Do not treat `.github/workflows/claude.yml` as a build or test workflow.

## COMMANDS

```bash
argc --argc-eval Argcfile.sh --help
bash tests/argc-smoke.sh
./scripts/build.sh
./bin/skogai repo list --type active
```

## NOTES

- Commands assume the machine CLI toolchain, including `argc`, is already on `PATH`; bootstrap does not install it.
- `repo status`, `repo update`, and `repo add` need `gita`; repository lookup also needs authenticated `gh`.
- `tmp/context/` is live, readable session state; new scratch content is non-durable unless promoted.
- `docs/argc/AGENTS.md` covers the captured argc reference material; it is not the root command source.

<!-- OPENWIKI:START -->

## OpenWiki

This repository has a generated `openwiki/` evidence index. It is optional just-in-time context, not required startup reading.

- Treat source code and tests as authoritative. A brief's unknowns and review items are verification gaps, not automatic requirements.
- Prefer the narrowest quiet validation that proves the changed behavior. Preserve complete failure output.

The scheduled OpenWiki GitHub Actions workflow refreshes the repository wiki. Do not hand-edit generated OpenWiki pages unless explicitly asked; prefer updating source code/docs and letting OpenWiki regenerate.

<!-- OPENWIKI:END -->
