# 2026-11-20: the three unverified fetch claims (doc/questions.md Q2.11)

Run: Claude Opus 5.5 (`claude-opus-5-5`) in Claude Code 2.1.329 under T3 Code, machine `skogix-laptop` (Linux 7.2.15-1-omarchy), checkout `/home/skogix/dev/Work/a9aa117b-0c959af2e9caa08b`, base commit `92efe2e` (master). Host tools: mise 2026.11.7, mani 0.32.1, podman.

Everything below was run. Nothing was pushed; the dry runs below print what a push would do and send no objects. The container got none of the host's credentials or git config.

## 1. Remote-container path: `mise install mani`, then the tag fetch

Container: `docker.io/library/node:24-alpine` (already on the machine), `apk add git curl bash ca-certificates`, mise from `curl -fsSL https://mise.run | sh` (gave 2026.11.10), `git clone https://github.com/skogai/monorepo /work` (head `92efe2e`), `mise trust -a`, `GIT_TERMINAL_PROMPT=0`. Scripts: one `sh` file per attempt, mounted read-only.

| Command | Expected (doc/agent-workflow.md) | Actual | Verdict |
|---|---|---|---|
| `mise install mani` | installs the pinned mani | `mise ERROR [skogai] plugin not installed` | fail |
| `mise plugins install -a`, then `mise install mani` | — | the same error, before anything installs | fail |
| `(cd / && mise plugins install -y skogai 'https://github.com/skogai/mise-plugin#6f27f183680d519bd3ed2bdc56d87445eb653293')` | — | `plugin:skogai ✓` | pass |
| then `mise install mani` | installs mani | exit 0 (also ran `mise lock` and warned that code-review-graph needs uv >= 0.12.10) | pass |
| then `mise exec mani -- mani sync -t skogai-jq --ignore-sync-state` | clones skogai-jq | `skogai-jq ✓`, `repos/skogai-jq/AGENTS.md` present | pass |
| git-only fallback: `git clone https://github.com/skogai/skogai-jq` | clones | cloned | pass |

Result: the documented path does not work on a clean machine. The `_.skogai` directive in `mise.toml` makes every mise command in the checkout fail until the plugin is installed, and the plugin cannot be installed from inside the checkout. The comment in `mise.toml` ("with no source loaded, mise skips it with a warning instead of failing") does not hold for mise 2026.11.10. Installing the plugin from outside the checkout first is a working order.

Next action: owner call on whether to fix the order in `doc/agent-workflow.md` and the `mise.toml` comment, or make the directive optional (issue #31 is the isolated-runner work).

## 2. Cloning a private repo without workstation credentials

| Command | Expected | Actual | Verdict |
|---|---|---|---|
| in the container: `mani sync -t podman --ignore-sync-state` | fails, does not hang | `podman ✕`, nothing cloned | pass (fails as expected) |
| in the container: `git clone https://github.com/skogai/podman` | fails, does not hang | `fatal: could not read Username for 'https://github.com': terminal prompts disabled` | pass (fails as expected) |
| on the host, no token or global config: `env -u GITHUB_TOKEN -u GH_TOKEN GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 GIT_TERMINAL_PROMPT=0 git clone --depth 1 https://github.com/skogai/podman` | fails | same `could not read Username` | pass (fails as expected) |
| the same for `skogai/skogai-jq` (public) | clones | cloned | pass |

`gh repo view` on every `mani.yaml` URL: 9 of 29 are private: `skogai/wiki`, `skogai/podman`, `skogai/nvim-omarchy`, `skogai/cloudflare`, `skogai/docs`, `skogai/dot-skogai`, `skogai/skogfleet` (catalogued as `skogai-skogfleet`), `skogai2/core`, `skogai2/docs`. The line "All listed repos are public, so no credentials are needed to read" in `doc/agent-workflow.md` is wrong.

## 3. `git push --dry-run` as a read-only check

| Command | Expected | Actual | Verdict |
|---|---|---|---|
| `git -C repos/<n> push --dry-run` for skogai-jq, skogai2-config, skogix, skogai (workstation credentials through `gh auth git-credential`) | — | `Everything up-to-date`, exit 0 | pass |
| `git -C repos/skogai-jq push --dry-run origin HEAD:refs/heads/dryrun-probe` | shows the push | `* [new branch] HEAD -> dryrun-probe` | pass |
| afterwards `git -C repos/skogai-jq ls-remote --heads origin \| grep -c dryrun-probe` | 0 (nothing pushed) | 0 | pass |
| the same dry run with no token and no global config | fails | `fatal: could not read Username` | pass (fails as expected) |
| dry run to a public repo with no write access (`charleswei118/aliasflare`, shallow clone in the scratchpad) | fails | `remote: Permission to charleswei118/aliasflare.git denied to Skogix.` 403, exit 128 | pass (fails as expected) |

Result: `git push --dry-run` contacts GitHub and checks both authentication and write access, without sending anything. It is a usable read-only check.
