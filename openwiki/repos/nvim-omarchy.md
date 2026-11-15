---
type: repository
title: nvim-omarchy
description: "Personal Neovim configuration: the LazyVim starter as the Omarchy desktop ships it, plus a remote clipboard provider, mise TOML support, SchemaStore and diffview. Two commits, both from 2026-11-13."
tags: [neovim, lazyvim, omarchy, dotfiles, mise]
repo: skogai/nvim-omarchy
commit: 8aa4f33
last_commit: 2026-11-13
generated: { by: "claude-code", at: "2026-11-15" }
sources:
  - repos/nvim-omarchy/README.md
  - repos/nvim-omarchy/CLAUDE.md
  - repos/nvim-omarchy/init.lua
  - repos/nvim-omarchy/lazyvim.json
  - repos/nvim-omarchy/mise.toml
  - repos/nvim-omarchy/.gitignore
  - repos/nvim-omarchy/lua/config/lazy.lua
  - repos/nvim-omarchy/lua/config/options.lua
  - repos/nvim-omarchy/lua/config/keymaps.lua
  - repos/nvim-omarchy/lua/config/remote_clipboard.lua
  - repos/nvim-omarchy/lua/plugins/all-themes.lua
  - repos/nvim-omarchy/lua/plugins/omarchy-theme-hotreload.lua
  - repos/nvim-omarchy/lua/plugins/miser.lua
  - repos/nvim-omarchy/lua/plugins/otter.lua
  - repos/nvim-omarchy/lua/plugins/treesitter.lua
  - repos/nvim-omarchy/lua/plugins/schemastore.lua
  - repos/nvim-omarchy/lua/plugins/diffview.lua
  - repos/nvim-omarchy/plugin/after/transparency.lua
---

# nvim-omarchy

**A personal Neovim configuration built on the LazyVim starter as the Omarchy (Arch/Hyprland) desktop ships it, with a few local additions.** It is meant to live at `~/.config/nvim`. The repo has 27 files and two commits, both dated 2026-11-13: an initial import and a cleanup. It is a small, quiet config repo with no tests. `CLAUDE.md` describes the layout accurately.

## Source map

| Path | Holds |
|---|---|
| `init.lua` | Two lines: `require("config.lazy")`. |
| `lua/config/lazy.lua` | Bootstraps lazy.nvim and loads LazyVim plus `lua/plugins/`. |
| `lua/config/options.lua` | Calls the remote clipboard setup; sets `relativenumber = false` and `vim.g.autoformat = false`. |
| `lua/config/keymaps.lua` | Maps `;` to `:` in normal mode. |
| `lua/config/autocmds.lua` | Starter comments only. |
| `lua/config/remote_clipboard.lua` | Custom clipboard provider for tmux, SSH and herdr sessions (158 lines). |
| `lua/plugins/all-themes.lua` | Declares every Omarchy theme plugin so any can be swapped in. |
| `lua/plugins/omarchy-theme-hotreload.lua` | Applies a new theme when Omarchy changes it. |
| `lua/plugins/lualine-transparent.lua`, `plugin/after/transparency.lua` | Transparent backgrounds. |
| `lua/plugins/disable-news-alert.lua`, `lua/plugins/snacks-animated-scrolling-off.lua` | Small Omarchy-shipped overrides. |
| `lua/plugins/miser.lua`, `otter.lua`, `treesitter.lua` | mise TOML editing support. |
| `lua/plugins/schemastore.lua` | SchemaStore schemas for `jsonls` and `yamlls`. |
| `lua/plugins/diffview.lua` | diffview.nvim with `<leader>g` keys. |
| `lua/plugins/example.lua` | The starter's disabled example. |
| `lazyvim.json` | Enabled LazyVim extras (13). |
| `lazy-lock.json` | Plugin lockfile. |
| `mise.toml` | One example task. |
| `stylua.toml`, `.neoconf.json` | Formatter and neoconf settings. |
| `CLAUDE.md`, `README.md`, `LICENSE` | Docs and license. |

## How it works

`init.lua` requires `config.lazy`. That file clones lazy.nvim if it is missing (`lua/config/lazy.lua:1-15`), then sets up two specs: LazyVim's own plugins and every file in `lua/plugins/` (`:17-23`). Custom plugins are not lazy-loaded by default (`:27`) and plugins track the latest commit (`:30`). `options.lua`, `keymaps.lua` and `autocmds.lua` are LazyVim hook files.

### Omarchy theme system

`lua/plugins/theme.lua` is not in the repo. It is a symlink into `~/.local/state/omarchy/current/theme/` that Omarchy creates and rewrites, and it is gitignored. `all-themes.lua` pre-declares about 19 theme plugins. Its `aether` entry sets `branch = "v3"` and `name = "aether"` so the plugin directory matches what Omarchy generates (`all-themes.lua:16-24`). `omarchy-theme-hotreload.lua` listens for the `User LazyReload` event, re-requires `plugins.theme`, applies the new colorscheme and re-sources `plugin/after/transparency.lua` (`omarchy-theme-hotreload.lua:11-80`).

### Remote clipboard

`remote_clipboard.lua` installs a custom `vim.g.clipboard` only when in tmux, in SSH, or under the `herdr` multiplexer, which it detects by `HERDR_PANE_ID` or by walking parent processes (`remote_clipboard.lua:22-45`). Copies go to `wl-copy` and to the terminal through OSC 52 (`:65-78`). Pastes read `wl-paste` or the tmux buffer (`:108-123`). Opt-outs are `vim.g.omarchy_remote_clipboard_osc52` and `vim.g.omarchy_remote_clipboard_sync` (`:78`, `:153`).

### mise support

`treesitter.lua` registers a treesitter predicate `is-mise?` that matches mise config file names (`treesitter.lua:4-14`). `otter.lua` activates otter.nvim on TOML files for embedded-language support inside task `run` strings. `miser.lua` loads `carldaws/miser.nvim` after requiring `lspconfig.util`, because miser prepends an older lspconfig copy to the runtime path (`miser.lua:5-8`).

## How to use it

- Install: clone to `~/.config/nvim`. The README says `mise bootstrap` does this from `[bootstrap.repos]` in `~/.config/mise/config.toml`.
- Commands from `CLAUDE.md`: `stylua lua/ plugin/` to format; `nvim --headless "+Lazy! sync" +qa` to load and sync plugins (rewrites `lazy-lock.json`); `:checkhealth`, `:Lazy`, `:LazyExtras` inside Neovim.
- Extras are managed through `:LazyExtras`, which writes `lazyvim.json`.
- Convention: Omarchy-shipped files use tabs, user-added files use two spaces.
- Assumptions: an Omarchy desktop for the theme symlink, Wayland tools `wl-copy` and `wl-paste` for the clipboard path.

## Relations to other SkogAI repos

- The files show no dependency on another SkogAI repo.
- The README says the clone is driven by the user's global mise config, and points to `~/.config/skogai/desktop/nvim.md` for how it fits the machine. That file is outside this repo; which repo owns it was not determined.
- The mise TOML plugins match the mise-based task convention used across the other repos.
- `CLAUDE.md` says the repo is not tracked by `mise dotfiles`.

## Gaps and stale references

- `lua/plugins/theme.lua` is required by the hot-reload plugin but exists only on an Omarchy machine. `omarchy-theme-hotreload.lua` guards the require with `pcall`; behaviour without Omarchy was not tested.
- `lua/plugins/example.lua` is dead starter code (197 lines).
- `mise.toml` holds only a placeholder task.
- `schemastore.lua` contains one comment in Swedish; the rest of the repo is English.
- No `AGENTS.md`; only `CLAUDE.md`. The monorepo has no cached copy for this repo.
