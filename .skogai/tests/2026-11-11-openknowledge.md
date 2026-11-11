# Open Knowledge research experiments — 2026-11-11

Run: Codex (gpt-6-astra), T3 Code / Codex harness, machine skogix-workstation,
checkout `/home/skogix/dev/Work/t3-16facfd2-c69f27fa28070a33`,
base `19ede8e8443b420f2e8b9eac6f0800727c6def5e`.
Prerequisites: installed openknowledge in `~/.local/bin`, mise, authenticated gh, network and shell tools. These are machine prerequisites, not repository provisioning.

| Exact command | Expected | Actual | Verdict / next action |
| --- | --- | --- | --- |
| `openknowledge version` | Installed version | 0.13.0 | Pass; verify provenance before pinning |
| `openknowledge check --help` | Current README command available | Unknown command, exit 2 | Fail; reconcile version with docs |
| `mise registry \| rg -i 'openknowledge\|okn\|hugo\|mkdocs'` | Discover installation candidates | Hugo entries only | Pass as discovery; investigate generic backends |
| `gh api repos/skogai2/okn/releases --jq '.[] \| [.tag_name, (.assets \| map(.name))]'` | Inspect release assets | Empty output | Blocked for selecting fork release; inspect upstream or source build |
| `trial=$(mktemp -d /tmp/okn-research.XXXXXX)` | Disposable directory | `/tmp/okn-research.tqUGwH` | Pass |
| `openknowledge scaffold --name 'SkogAI research trial' --no-agents --no-setup "$trial/wiki"` | Minimal bundle | Config, index, log, SPEC created; OKF 0.2 | Pass |
| `openknowledge validate "$trial/wiki"` | Valid scaffold | 3 Markdown files; validation passed | Pass; test actual content next |
| `openknowledge export html --out "$trial/site" "$trial/wiki"` | Static output | Refused: release outputs disabled | Blocked; enable viewer in future disposable trial |
| `openknowledge search /tmp/okn-research.tqUGwH/wiki 'chronological update history' --matches` | Relevant source result | 8 matches, index Start Here ranked first, zero validation issues | Pass for smoke test only |

Source inspection (not tests): repository README, plan, ADR 0001 and mise config; fork README and installation page at `99b05e27ce328db3ae4d31cd0e30f178ead6de30`. CLI help inspected for scaffold, validate, search, view and export.

Not run: installation, actual-content retrieval evaluation, broken-link trial, live viewer, successful HTML export, hosting, CI, MCP, second machine. Next action: follow the staged pilot in the research note. No application test suite exists at the root.

## PR #8 conflict resolution

Run: Codex (gpt-6-astra), T3 Code / Codex harness, skogix-workstation; same checkout as above. Updated base: `6990cd7` (master); original PR head: `7a1ad7b`. Git configuration `git config --get pull.rebase` returned `true`, so the branch was rebased with `git rebase origin/master`.

Resolved `doc/plan.md` by preserving the complete new master roadmap and appending the wiki experiment. Updated current-work wording to reflect isolation as milestone 1. Historical research remains unchanged.

Verification: `git diff --check origin/master...HEAD` passed; `git merge-base --is-ancestor origin/master HEAD` passed. A Python assertion checked that the resolved plan starts with the exact `git show origin/master:doc/plan.md` content, scanned changed files for conflict-marker lines, and checked relative Markdown link targets in the three new pages; all passed. No application tests or runtime experiments were rerun for this documentation-only resolution. Next action: push the rebased branch for owner review.

## Open Knowledge workflow failure

Run: Claude (claude-fable-5-2), T3 Code / Claude Code harness, machine skogix-workstation,
checkout `/home/skogix/dev/Work/t3-8b954d3b-bfec7df1d5f133f0`,
base `af7504c` (master).
Prerequisites (machine, not repository): mise 2026.11.5, authenticated gh, network.

| Exact command | Expected | Actual | Verdict / next action |
| --- | --- | --- | --- |
| `gh run list --limit 15` | See failing runs | All 6 `Open Knowledge` runs failed, on master and on two pull requests | Pass as observation |
| `gh run view 42982824685 --log-failed` | Failure cause | `npm error 404 '@openknowledge-sh/openknowledge@0.13.0' is not in this registry` in the action's install step; later steps skipped | Fail; cause is the upstream action, not the wiki |
| `npm view @openknowledge-sh/openknowledge versions` | Published versions | E404 | Fail; the package is not published |
| `mise exec -- openknowledge automation github run --event push --ref master --base "$(git rev-parse HEAD~1)" --path wiki --eval .openknowledge/evals/knowledge.yaml --baseline .openknowledge/audit-sources.json --reports <scratch>/reports` | Checks pass | Exit 0; structure, quality and health `passing`; validation, audit and eval reports written | Pass |
| Same command with `--event pull_request --ref t3/8b954d3b --base "$(git merge-base HEAD origin/master)"` | Checks pass | Exit 0 | Pass |
| Fresh `git clone` of the checkout, `env -i` with an empty `HOME`, `MISE_YES=1`, `MISE_TRUSTED_CONFIG_PATHS=<clone>`, a GitHub token: `mise exec "github:openknowledge-sh/openknowledge@0.13.0" -- openknowledge --version` then `mise run wiki:validate` | mise installs the pinned release without machine state | Installed; validation passed, exit 0 | Pass; approximates a CI runner, is not one |

Source inspection (not tests): upstream `action.yml` on `main` (`99b05e27`) has the same `npm install` step, so a newer pin does not fix it. Release `v0.13.0` ships binary tarballs, which is what the `github:` mise backend installs. `jdx/mise-action` `v5.2.7` resolves to `b44d12e7d0d8ee7461bb893e1b1993500433185b`.

Change: `.github/workflows/openknowledge.yml` installs the pinned release with `jdx/mise-action` and runs the automation command the upstream action runs, then uploads the reports.

Not run before pushing: the edited workflow on GitHub; the maintenance-agent path of the upstream action (maintenance mode is `off` in `wiki/.openknowledge.toml`). Next action: read the workflow result on the pull request.

### First workflow run on pull request #12

Same run as above; commit `e035b62`.

| Exact command | Expected | Actual | Verdict / next action |
| --- | --- | --- | --- |
| GitHub Actions run 42989304228 (pull_request, `e035b62`) | Workflow passes | `mise install --monorepo github:openknowledge-sh/openknowledge` exited 1: `[monorepo].config_roots did not match any config roots`. `jdx/mise-action` adds `--monorepo` because `mise.toml` sets `monorepo.config_roots`, and the `mise-plugin` submodule is not checked out | Fail; the local clean-clone test above did not pass `--monorepo`, so it missed this |
| Clean clone as above: `mise install --monorepo github:openknowledge-sh/openknowledge` | Reproduce | Same error | Pass as reproduction |
| Clean clone as above: `mise install github:openknowledge-sh/openknowledge` | Install without submodules | Exit 0, with a warning that `mise-plugin` has no mise config file | Pass; set `monorepo: false` on the action |

Open question, not decided here: whether CI should check out the submodules instead. `skogai/mise-plugin` is public; the visibility of `skogai/skogai` and `skogai/skogix` to the workflow token was not checked.
