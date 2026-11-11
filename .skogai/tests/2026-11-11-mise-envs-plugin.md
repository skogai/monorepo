# mise environments, conf.d and plugin evidence: 2026-11-11

Run: Claude (Fable 5.2), Claude Code harness in T3 Code; machine `skogix-workstation`; checkout `/home/skogix/dev/Work/t3-bbf2e28e-ec0f5784fdaf6e29`; base `af7504c`; plugin submodule base `d94fd33`, changed to `b972489`. mise `2026.11.5 linux-x64`.

## How the checks were isolated

Unless a row says "host", mise ran as below, with `$S` a per-session scratch directory. The machine's global config, system config, installed plugins, and tools were not read or changed.

```sh
env -i HOME="$HOME" PATH=/usr/bin:/bin \
  MISE_CONFIG_DIR=$S/iso/config MISE_SYSTEM_CONFIG_DIR=$S/iso/system MISE_DATA_DIR=$S/iso/data \
  MISE_STATE_DIR=$S/iso/state MISE_CACHE_DIR=$S/iso/cache MISE_YES=1 MISE_EXPERIMENTAL=1 \
  MISE_AUTO_INSTALL=0 MISE_TRUSTED_CONFIG_PATHS=<fixture or checkout> mise …
```

Prerequisites outside the checkout: `mise` and Git on the machine, and network access to GitHub for the `skogai` environment's first plugin clone. This is one machine. Nothing here shows the setup reproduces on another.

## Fixture: environments and conf.d

A throwaway project with `.miserc.toml` (`env = ["skogai"]`, `env_conf_d = true`), a `mise.toml`, and fragments `10-a.toml`, `10-a.skogai.toml`, `10-a.develop.toml` in `.config/mise/conf.d/`, each setting `WHO` to its own name.

| Command | Expected | Actual | Verdict |
|---|---|---|---|
| `mise cfg` | Default env loads the `skogai` fragment only | `10-a.toml`, `mise.toml`, `10-a.skogai.toml` | pass |
| `mise env --json` | Env fragment overrides `mise.toml`, which overrides the shared fragment | `WHO=10-a.skogai` | pass |
| `mise -E develop cfg` | `-E` replaces the default env | `10-a.toml`, `mise.toml`, `10-a.develop.toml` | pass |
| `mise -E skogai,develop env --json` | Last listed env wins | `WHO=10-a.develop` | pass |
| `mise -E develop,skogai env --json` | Last listed env wins | `WHO=10-a.skogai` | pass |
| `MISE_ENV= mise env --json` | No env fragments | `WHO=mise.toml`, shared fragment still loaded | pass |
| `mise -E foo cfg` with `.miserc.toml` reduced to `env_conf_d = true` | Env fragments work without a default env | `10-a.foo.toml` loaded | pass |
| `mise exec -- printenv WHO` after adding `mise.local.toml` | Local file overrides the env fragment | `mise.local.toml` | pass |
| Same, with `conf.d/10-a.local.toml` instead | Local fragment overrides the env fragment | `10-a.skogai`; the local fragment loaded first in `mise cfg` | fail |
| `mise settings get auto_install` with `auto_install = false` in `.miserc.toml` | Unknown whether `.miserc.toml` accepts it | `false`; `true` without the line | pass |
| `{{config_root}}` in a `.config/mise/conf.d/` fragment | The project root | The project root, not the `conf.d` directory | pass |

The failed row is a wrong expectation, kept as a finding: a `conf.d/*.local.toml` fragment does not override an environment fragment. `doc/mise.md` says to use `mise.local.toml`.

An earlier attempt at the `-E develop` row loaded no fragment. The cause was the test loop passing `-E develop` as one argument in zsh, not mise.

## Fixture: plugin behaviour

A probe plugin in the fixture that prints its hook context.

| Command | Expected | Actual | Verdict |
|---|---|---|---|
| `mise plugins link probe ./plug`, `_.probe = {…}` in an env fragment, `mise env --json` from the root and from `sub/deep` | `ctx` carries `options` and `config_root`; root is the same from a subdirectory | `config_root` is the project root in both; earlier `[env]` values are visible through `os.getenv` | pass |
| `_.missing = {}` with no such plugin | Warning, rest of the env loads | `WARN skipping env plugin missing: it is not installed and has no source` | pass |
| `[plugins] probe2 = "./plug"` with auto install on | Unknown | mise links the local directory itself: `plugin:probe2 ✓ linked …/proj/plug` | pass |
| Same `[plugins]` entry inside an env fragment | Linked only when the env is selected | Linked on first use of that env | pass |
| A copy of the project in a second directory, same plugin name, modified hook | Each project gets its own plugin | The second project ran the first project's hook; the link was not changed | fail |
| `file.exists` on a directory, a missing path, a file | true, false, true | true, false, true | pass |

The failed row is why the default environment does not use a local path: a plugin link belongs to the mise data directory, so checkouts that share one share the link.

## This checkout

| Command | Expected | Actual | Verdict |
|---|---|---|---|
| `mise cfg` | `mise.toml` and `plugin.skogai.toml` | Those two; plugin cloned from `https://github.com/skogai/mise-plugin#d94fd33` | pass |
| `mise exec -- sh -c 'echo $SKOGAI_MONOREPO_DIR …'` | Old hook values, since the plugin's default branch is unchanged | `/home/skogix/Work`, `SKOGAI_ENV_VAR` set, `~/.local/bin` on PATH | pass, see next action |
| `mise -E develop cfg` | `mise.toml` and `plugin.develop.toml`; submodule linked | Those two; `skogai-develop ✓ linked …/mise-plugin` | pass |
| `mise -E develop exec -- sh -c 'echo $SKOGAI_MONOREPO_DIR …'` | The checkout; no example variable; PATH untouched | `/home/skogix/dev/Work/t3-bbf2e28e-ec0f5784fdaf6e29`, unset, `/usr/bin:/bin` | pass |
| `mise -E develop exec -- printenv SKOGAI_MONOREPO_DIR` from `mise-plugin/` | The checkout | The checkout | pass |
| `MISE_ENV= mise exec -- sh -c 'echo ${SKOGAI_MONOREPO_DIR-unset}'` | unset | unset | pass |
| `mise tasks --all` | Wiki tasks and the three plugin tasks | `//:wiki:eval`, `//:wiki:export`, `//:wiki:validate`, `//mise-plugin:lint`, `//mise-plugin:lint-fix`, `//mise-plugin:test` | pass |
| `mise -E develop tasks --all` | The same plus `//:plugin:link` | As expected | pass |
| `mise -E develop run //:plugin:link` from `wiki/` | Link points at this checkout's submodule | `readlink` gives `…/t3-bbf2e28e-ec0f5784fdaf6e29/mise-plugin` | pass |
| host: `mise exec -- sh -c 'echo $SKOGAI_MONOREPO_DIR'` | Old values | `/home/skogix/Work` | pass, machine |
| host: `mise -E develop exec -- sh -c 'echo $SKOGAI_MONOREPO_DIR'` | The checkout | `/home/skogix/Work` | fail, machine |

The last row fails because this machine already has `~/.local/share/mise/plugins/skogai-develop` linked to `/home/skogix/Work/mise-plugin`, a different checkout with the old hooks. That is the shared-link behaviour above. The link was left alone; `mise -E develop run //:plugin:link` in the wanted checkout changes it.

## Plugin submodule, commit `b972489`

Run on the host from `mise-plugin/`, with the plugin's development tools already installed there.

| Command | Expected | Actual | Verdict |
|---|---|---|---|
| `mise run test` | All hook checks pass | 9 of 9 `ok`, `all checks passed` | pass |
| `mise run lint`, now `hk check --all` | Lint examines files | actionlint on 1 file, stylua and lua-language-server on 5 Lua files, no problems | pass |

The first run of the test failed two PATH checks because `mise env --dotenv` does not print `PATH`. The script now reads values with `mise exec -- printenv`. The test builds its own isolated mise directories and a project path containing a space.

## Read, not run

- The file names and precedence rules come from the mise documentation pages linked in `doc/mise.md`, fetched on 2026-11-11. Only the rows above were checked against the installed binary.
- `/etc/mise/conf.d` and `~/.config/mise/conf.d` exist on this machine. Whether they follow `env_conf_d` was not tested; the documentation says a project `.miserc.toml` governs project directories only.

## Not run

Plugin CI on GitHub, a fresh recursive clone, a second machine, the `skogai` environment against the new hooks, a pinned plugin revision in `[plugins]`, `mise mcp` with environments, platform environments (`auto_env`), hook caching, and `mise run wiki:eval` and `wiki:export`. `mise run wiki:validate` was run on the host after the cleanup and printed `OK Validation passed`.

## Open questions

- `SKOGAI_MONOREPO_DIR` now defaults to the checkout. A fixed directory is still possible with `root = "~/Work"`. Which one the owner wants is undecided, as are the variable names.
- Whether the default environment should follow the plugin's default branch or a pinned revision.
- What belongs in an always-loaded fragment. None was added.

## Next action

Merge the plugin pull request before the monorepo one, then repeat the second row of "This checkout" and expect the checkout path.
