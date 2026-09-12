# Install NuDay Complete

These instructions are for the person installing the plugin. The `skills/`
directory supplies instructions to the AI; client manifests configure the
connection. Your password and OAuth tokens do not belong in either place.

## Choose access and sign in

Download the standard or **read-only** ZIP from NuDay Manager's connection
options. Read-only connects to `/mcp/complete-readonly`; the standard package
includes tools that can make changes. Both include the same skill reference
catalog, but the read-only server cannot execute its write workflows. Client
approval settings still control individual tool calls.

The package is configured for organization `(chosen at sign-in)` at
`https://app.nuday.ai/mcp/complete`. Choose that organization on the
NuDay consent screen. To use a different organization, download its package.

Installation may show an authentication prompt immediately, or you may need to
open your client's MCP controls and authenticate. The client opens NuDay in your
browser. Sign in, choose the organization, and authorize access. The client stores
and refreshes its tokens. A new authorization asks for an organization again;
ordinary token refresh does not. No NuDay connection-management page is required.

## Claude Code

1. Extract the ZIP to a directory you control.
2. Start `claude --plugin-dir /absolute/path/to/extracted-plugin`.
3. Open `/mcp`, choose the NuDay server, and authenticate.
4. Confirm the plugin skills appear and ask for a read-only listing of resources
   in your organization.

This directory-based path avoids dependence on ZIP-upload availability.
See [Claude plugin loading](https://code.claude.com/docs/en/plugins) and
[MCP authentication](https://code.claude.com/docs/en/mcp).

## Codex

1. Add the public marketplace: `codex plugin marketplace add nuday-ai/nuday-plugins`,
   then enable **NuDay Complete** (or **NuDay Complete (read-only)**) from the
   Plugin Directory. NuDay Desktop can do this for you from its Extensions page.
2. The manifest points Codex at `codex-mcp.json`, which registers the NuDay MCP
   server for browser sign-in. Use the server's **Authenticate** control, or run
   `codex mcp login nuday-complete` if it does not prompt.
3. Confirm NuDay tools and skills are available in a new task.

Codex reads `mcpServers` in `.codex-plugin/plugin.json` only as a path to a
servers file, so the server itself lives in `codex-mcp.json` with Codex's own
keys (`url`, `http_headers`, `bearer_token_env_var`). For an unattended
setup, register `codex-mcp-api-key.json` instead: it names `NUDAY_API_KEY` as
the bearer token variable. See
[Codex MCP configuration](https://developers.openai.com/codex/mcp).

## Cursor

1. Extract the plugin under `~/.cursor/plugins/local/nuday-complete/` (use a
   distinct `nuday-complete-readonly` directory for the read-only download).
2. Reload Cursor and enable the plugin/server in its customization controls.
3. Complete the MCP authentication prompt and test a resource listing.

If your Cursor version lacks local plugins, merge the bundled `mcp.json` into
your existing MCP configuration and install skills using that version's skill
controls. This manual fallback requires both steps.
See [Cursor local plugins](https://prod.cursor.com/docs/plugins).

## OpenCode

1. Extract the ZIP. Merge `opencode.json` into your existing configuration; do
   not overwrite unrelated servers or settings.
2. Copy the contents of `skills/` into `.opencode/skills/` in your project, or
   your configured user skill directory.
3. Run `opencode mcp auth nuday-complete` for the standard package, or use the
   server name from the read-only configuration. Complete browser consent.

`opencode-v2*.json` files are **version-specific compatibility examples**. Use
them only if your release documents the nested `mcp.servers` shape. They are not
an additional server to enable alongside the standard configuration.
See [OpenCode MCP configuration](https://opencode.ai/docs/mcp-servers).

## API keys and troubleshooting

Browser sign-in needs a client that can open a browser and receive the
loopback callback: the Claude Code CLI on your own machine, Codex, Cursor, and
OpenCode complete it. Sessions that cannot start a browser — remote or
container-based sessions, CI, scheduled jobs, and any desktop session where the
`/mcp` authenticate step reports "needs authentication" but never opens a
browser — should use the API-key configuration instead.

For those, set `NUDAY_API_KEY` in the client's environment and point the client
at the `*-api-key.json` file that replaces the OAuth one:

| Client | OAuth (default) | API key |
|---|---|---|
| Claude Code | `claude-mcp.json` | `claude-mcp-api-key.json` |
| Cursor | `mcp.json` | `mcp-api-key.json` |
| OpenCode | `opencode.json` / `opencode-v2.json` | `opencode-api-key.json` / `opencode-v2-api-key.json` |
| Codex | `codex-mcp.json` (OAuth) | `codex-mcp-api-key.json` |

For Claude Code that means swapping the `mcpServers` reference in
`.claude-plugin/plugin.json` to `./claude-mcp-api-key.json`, or adding the
server from that file with `claude mcp add-json`. Never put the key's value
into this plugin directory or share it with the AI.

The API-key manifests carry no `X-Tenant-Id` header. On connect the server's
`initialize` instructions (and `nuday_whoami`) tell the agent its
`principal_kind`:

- `tenant_pinned` — the key (or the OAuth consent) is bound to one tenancy;
  never pass `tenant_id` (it is accepted only when it equals that tenancy).
- `single_tenancy` — your only membership is resolved automatically; never
  pass `tenant_id`.
- `multi_tenancy` — pass `tenant_id` on create tools only (ids from
  `nuday_tenancies_list(query=<name>)`), or add an `X-Tenant-Id` header to the
  manifest to pin one tenancy for the client.
- `platform_admin` — lists span every tenancy and each row carries
  `tenant_id`/`tenant_name`; pass `tenant_id` to scope a list and always on
  create tools.

Nothing is remembered between calls. A wrong `tenant_id` returns an error
that names your `principal_kind` and the exact retry: on "tenant_id is not
needed" drop the argument; on "not a tenancy you can access" pick one of the
listed ids; on "does not exist" search with `nuday_tenancies_list`.
`av auth tenant <id>` pins the CLI profile the same way a header does.

- No sign-in prompt: open the client's MCP authentication controls; check that
  the plugin/server is enabled and that an API key is not overriding OAuth.
- Repeated login failure: confirm the Manager deployment includes the OAuth
  changes, and update the client if it cannot use PKCE S256 and registration.
- Organization access denied: select the organization in the downloaded package
  and confirm your current membership. A different tenant header cannot change
  an existing grant. Reauthorize after switching packages.
- "A tenancy is required": you are `multi_tenancy` or `platform_admin` and the
  call named no tenancy. Find the id with `nuday_tenancies_list(query=<name>)`
  (or `nuday_whoami`), then pass it as `tenant_id` — or pin it with an
  `X-Tenant-Id` header in the manifest.
- "tenant_id is not needed": you are `single_tenancy` or `tenant_pinned` —
  drop the argument and retry.
- Writes unavailable: check whether you installed the read-only variant.
- Duplicate tools: remove duplicate manual MCP entries when enabling the plugin.

## Verification status

Automated tests check manifests, archive layout, both endpoint variants, skills,
and server-side authorization. Documentation paths were checked against vendor
guidance. A full interactive install/login in each client remains a release
acceptance check; do not infer four-client certification from unit tests.
ChatGPT registration and publication remain a separate release step.
