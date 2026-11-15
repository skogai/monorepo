# AGENTS.md

This file provides guidance to Codex (claude.ai/code) when working with code in this repository.

## What this is

A personal Neovim config built on the [LazyVim](https://lazyvim.github.io) starter, running on an Omarchy (Arch/Hyprland) desktop. Many files here are shipped and managed by Omarchy; the rest are the user's own additions. Git repo: `skogai/nvim-omarchy` (private), cloned by `mise bootstrap` (`[bootstrap.repos]`); not tracked by `mise dotfiles`.

## Commands

- Format Lua: `stylua lua/ plugin/` (config in `stylua.toml`: 2-space indent, 120 cols)
- Check config loads cleanly: `nvim --headless "+Lazy! sync" +qa` (installs/updates plugins and rewrites `lazy-lock.json`) or `nvim --headless +qa` to just load
- Health check inside Neovim: `:checkhealth`, `:Lazy`, `:LazyExtras`

There are no tests.

## Architecture

- `init.lua` → `lua/config/lazy.lua` bootstraps lazy.nvim, imports `lazyvim.plugins`, then every file in `lua/plugins/` (each returns a lazy spec that is merged with LazyVim's). Custom plugins are **not** lazy-loaded by default (`defaults.lazy = false`).
- `lua/config/{options,keymaps,autocmds}.lua` are LazyVim hook files: options load before lazy.nvim; keymaps/autocmds on `VeryLazy`. `options.lua` calls `config.remote_clipboard.setup()`.
- `lazyvim.json` holds the enabled LazyVim extras (managed via `:LazyExtras`, don't hand-edit unless intended).
- `lua/plugins/example.lua` is the starter's disabled example (`if true then return {} end`) — ignore it.

### Omarchy theme system

- `lua/plugins/theme.lua` is a **symlink** to `~/.local/state/omarchy/current/theme/neovim.lua`, gitignored; Omarchy creates and rewrites it when the system theme changes. Don't edit it here.
- `all-themes.lua` pre-declares every theme plugin (lazy) so any can be hot-swapped. The `aether` entry's `name`/`branch` must match Omarchy 4's generated spec (see comment in file).
- `omarchy-theme-hotreload.lua` listens for `User LazyReload`, re-requires `plugins.theme`, unloads the old theme modules, applies the new colorscheme, then re-sources `plugin/after/transparency.lua`.
- Transparency is split between `plugin/after/transparency.lua` (clears `bg` on highlight groups) and `lualine-transparent.lua` (clears `b`/`c` section backgrounds).

### Remote clipboard

`lua/config/remote_clipboard.lua` installs a custom `vim.g.clipboard` only under tmux, SSH, or the `herdr` multiplexer. Copies go to `wl-copy` and OSC 52 (via `tmux load-buffer` when in tmux); pastes read tmux buffer / `wl-paste` with fallback to the last in-process copy. It deliberately never reads via OSC 52 (blocks paste for ~10 s). Opt-outs: `vim.g.omarchy_remote_clipboard_osc52 = false`, `vim.g.omarchy_remote_clipboard_sync = false`.

### mise integration

`miser.lua`, `otter.lua`, and the `is-mise?` treesitter predicate in `treesitter.lua` support editing mise TOML files (embedded-language highlighting/LSP inside `run = "..."` tasks). `schemastore.lua` feeds SchemaStore schemas to `jsonls` and `yamlls` (yamlls' built-in store disabled).

## Conventions

- Omarchy-shipped files (`all-themes.lua`, `omarchy-theme-hotreload.lua`, `lualine-transparent.lua`, `disable-news-alert.lua`, `snacks-animated-scrolling-off.lua`, `plugin/after/transparency.lua`) use tabs; user-added files use 2 spaces. Match the file you're editing.
- Notable user settings: `vim.g.autoformat = false` (no format-on-save), `relativenumber = false`, `;` maps to `:` in normal mode.
