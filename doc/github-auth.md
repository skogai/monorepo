# GitHub authentication for mise

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

