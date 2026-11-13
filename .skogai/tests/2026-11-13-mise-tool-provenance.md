# mise tool provenance and pinning evidence: 2026-11-13

Run: Claude (Fable 5.2), Claude Code harness in the Claude desktop app; machine `skogix-workstation`; checkout `/home/skogix/Work`; base `a7f92ff`; branch `mise-13-provenance/claude-skogix-workstation`. Issue: [#13](https://github.com/skogai/monorepo/issues/13).

Everything under "Machine state" is a machine fact for `skogix-workstation` only. Prerequisites outside the checkout: a `mise` binary, and network access to GitHub releases for installs.

## Machine state (read, nothing changed)

| Command | Actual |
|---|---|
| `which -a mise` (zsh, and `fish -lc`) | `~/.local/bin/mise` first, then `/usr/bin/mise` |
| `~/.local/bin/mise --version` | `2026.11.5`; has `self_update`; not owned by a package |
| `/usr/bin/mise --version` | `2026.11.6`; self-update disabled |
| `pacman -Qo /usr/bin/mise /usr/bin/usage /usr/bin/fnox` | `mise-bin 2026.11.6-1`, `usage 6.12.1-1`, `fnox-bin 1.48.0-1` |
| `pacman -Qi mise-bin`, "Required By" | `omarchy-fish`, `omarchy-zsh` |
| `pacman -Qi usage fnox-bin`, "Required By" | None, both explicitly installed |
| `which -a usage` (zsh, fish, `bash -li`) | mise install or shim first, `/usr/bin/usage` after |
| `which -a fnox` (zsh, fish) | mise install or shim first, `/usr/bin/fnox` after |
| `usage --version`; `/usr/bin/usage --version` | `7.3.0`; `6.12.1` |
| `fnox --version`; `/usr/bin/fnox --version` | `1.44.0`; `1.48.0` |
| `env -i HOME=$HOME PATH=/usr/bin:/bin bash -c 'command -v mise usage fnox'` | `/usr/bin/mise`, `/usr/bin/usage`, `/usr/bin/fnox` |
| `mise settings ls`, lock settings | `locked_scopes = ["global", "project"]` from `/etc/mise/conf.d/omarchy-tools.toml` (package `omarchy-settings`) |
| Where `fnox` is requested | `~/.config/mise/config.toml` at `latest`. Not in this repository. |

Findings:

- Issue #13 says the pacman copies of `usage` and `fnox` win on PATH. On 2026-11-13 that holds only where mise is not activated and its shims are not on PATH. In activated zsh, fish and login bash the mise copies win.
- There are two `mise` files, not three. `~/.local/share/../bin/mise` is `~/.local/bin/mise` by another path.
- `mise-bin` cannot be removed without removing `omarchy-fish` and `omarchy-zsh`. The pacman `usage` is a major version behind the mise one.
- `~/.bashrc` runs `usage g completion-init bash`, and `~/.config/fish/config.fish` runs `fnox activate`. Both resolve to the mise copies in those shells.

## Pinning and lockfile (run in this checkout)

| Command | Expected | Actual | Verdict |
|---|---|---|---|
| `mise ls usage worktrunk` before the change | `latest` resolves to something | `usage 7.3.0`, `worktrunk 0.81.0`, both requested as `latest` | pass |
| Edit `mise.toml`: `usage` to `7.3.0`, `worktrunk` to `0.81.0`; `mise ls --local` | Requested version equals installed version | `usage 7.3.0`, `worktrunk 0.81.0` | pass |
| `mise lock` | Writes `mise.lock` | 14 targets (2 tools, 7 platforms), each with URL, sha256 and sigstore signer | pass |
| `mise exec -- usage --version`; `mise exec -- wt --version` | Pinned versions | `usage 7.3.0`; `wt v0.81.0` | pass |

## Isolated install from the lockfile

mise ran as below, with `$S` a per-session scratch directory, so the machine's global config, system config and installed tools were not read. The binary was `/usr/bin/mise` 2026.11.6.

```sh
env -i HOME="$HOME" PATH=/usr/bin:/bin \
  MISE_CONFIG_DIR=$S/iso/config MISE_SYSTEM_CONFIG_DIR=$S/iso/system MISE_DATA_DIR=$S/iso/data \
  MISE_STATE_DIR=$S/iso/state MISE_CACHE_DIR=$S/iso/cache MISE_YES=1 MISE_EXPERIMENTAL=1 \
  MISE_ENV= MISE_TRUSTED_CONFIG_PATHS=$PWD mise …
```

| Command | Expected | Actual | Verdict |
|---|---|---|---|
| `mise install --locked` | Both tools install from locked URLs | `usage@7.3.0`, `worktrunk@0.81.0` installed, checksums verified, exit 0 | pass |
| `mise exec -- sh -c 'command -v usage wt'` | Paths inside the isolated data directory | `$S/iso/data/installs/usage/7.3.0/…`, `…/worktrunk/0.81.0/…` | pass |
| `mise install --locked` after changing the `linux-x64` checksum of `usage` in `mise.lock` and clearing the data directory | Install refused | `Checksum mismatch`, install failed. `mise.lock` restored afterwards. | pass |

## Not run

- Removing any pacman package or `~/.local/bin/mise`. These need the owner and `sudo`.
- Any platform other than `linux-x64`. The other six lockfile entries were resolved by `mise lock` but not installed.
- A second machine. Nothing here shows the setup reproduces elsewhere.
- `mise install` without `--locked` against a tampered lockfile.

## Next action

The owner accepted [ADR 0002](../../doc/adr/0002-mise-binary-and-tool-source.md) on 2026-11-13 with any working `mise` as the prerequisite. The machine cleanup commands listed there are optional and not run.
