# NuDay Complete

Version **1.0.1**

Updatable installs: Claude Code — `claude plugin marketplace add <manager>/plugins/marketplace.json`
then `claude plugin install nuday-complete@nuday`; Codex — `codex plugin marketplace add nuday-ai/nuday-plugins`.
This ZIP is the same package for clients without a marketplace.

NuDay Complete packages the public NuDay platform skills with the aggregate
NuDay MCP endpoint. The same plugin directory supports Claude Code, Codex, and
Cursor. OpenCode uses the bundled `opencode.json` plus the same `skills/`
directory.

Download this plugin from your NuDay Manager connection-details or API-key
modal. That download replaces the example endpoint and tenant below with the
values for your organization.

The download is a single plugin ZIP. Its `.claude-plugin`, `.codex-plugin`,
`.cursor-plugin`, `skills`, and MCP configuration paths are all at the archive
root so local-plugin uploaders can recognize it directly. Do not wrap the
plugin in another directory before creating the archive.

## Installation

Start with [the installation and troubleshooting guide](INSTALL.md). It explains
the standard/read-only choice, browser organization selection, and the difference
between client configuration and AI skill instructions.

Follow the client-specific steps in INSTALL.md. Local import availability varies
by client version and workspace policy; extract the archive when using a local
plugin directory. All client manifests remain at the extracted root.

ChatGPT distribution is a separate release step. Its MCP-backed plugin needs a
registered ChatGPT app and an `.app.json` mapping for that registration. Add
those after the public OAuth endpoint has been deployed and verified; do not
put a placeholder app ID in this archive.

## Authentication

Browser sign-in is the default for interactive clients. The first connection
returns an OAuth challenge; your client opens NuDay Manager, you sign in and
explicitly approve access, and the client securely stores and refreshes its own
token. NuDay validates the exact MCP resource and `mcp:tools` scope on every
OAuth request; a token minted for another NuDay service is rejected.

- Claude Code: open `/mcp`, select `nuday-complete`, and authenticate.
- Codex: select **Authenticate** in the MCP server list or run
  `codex mcp login nuday-complete`.
- Cursor: enable the server and complete the sign-in prompt.
- OpenCode: run `opencode mcp auth nuday-complete` if it does not prompt on
  first use.

The flow needs a client that can open a browser on the machine you are using
and receive its loopback callback. Remote sessions, containers, CI, and any
desktop session where the server reports "needs authentication" but no browser
opens cannot complete it — use the API-key configuration below for those
(`INSTALL.md` has the per-client file mapping).

The flow uses OAuth Authorization Code with PKCE and dynamic public-client
registration. Native clients register loopback callbacks and web clients
register HTTPS callbacks. No client secret is stored in this plugin. Dynamic
registration remains the broad compatibility path for Claude Code, Codex,
Cursor, and OpenCode; a later release can add Client ID Metadata Document
support without changing this package.

API keys remain available for scheduled processes, CI, and other unattended
agents. The archive deliberately does not contain one. Use the API-key variants
bundled beside the default configuration:

- Claude Code: `claude-mcp-api-key.json`
- Cursor: `mcp-api-key.json`
- OpenCode: `opencode-api-key.json` or `opencode-v2-api-key.json`
- Codex: its manifest supports `NUDAY_API_KEY` when the variable is present and
  otherwise falls back to OAuth.

For a one-shell test:

```powershell
$env:NUDAY_API_KEY = "<your-key>"
```

```bash
export NUDAY_API_KEY="<your-key>"
```

Do not commit the key or paste it into a shared plugin directory.

OAuth `client_credentials` is also a non-browser machine flow. Registered
NuDay agent clients use a generated client secret and can request a
resource-bound token from `/oauth2/token` with scope `mcp:tools` and resource
set to this package's MCP URL. Existing agent identities created before 0.1.0
should be rotated once before using this flow. Interactive editors should use
the browser/PKCE flow above instead.

## Included capability

- All enabled, public platform skills from NuDay Manager's catalog, rendered
  into `skills/` when the ZIP is built so they always match the deployed
  Manager.
- One MCP connection to `https://app.nuday.ai/mcp/complete` for
  organization `(chosen at sign-in)`.
- Root-level native manifests for Claude Code, Codex, and Cursor.
- OAuth-first and API-key configuration examples, including stable and v2
  OpenCode forms. Copy `skills/*` into an
  OpenCode-discovered skills directory such as `.opencode/skills/` or
  `~/.config/opencode/skills/`.

Claude's MCP definition is deliberately named `claude-mcp.json` rather than
`.mcp.json`. This prevents Codex from auto-discovering Claude-specific header
substitution in addition to the native MCP definition in the Codex manifest.

The aggregate endpoint is intentional: it is NuDay Manager's canonical
external integration surface and already combines Manager, Apps, Evaluations,
Workspaces, connectors, and the Code Sandbox.
