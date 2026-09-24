# NuDay plugins

Version **1.0.4** — rendered from the NuDay Manager at `https://app.nuday.ai`.
Do not edit by hand: the publish workflow in `nuday-manager` overwrites this
repository whenever the plugin content changes.

## Codex

```
codex plugin marketplace add nuday-ai/nuday-plugins
```

Then install **NuDay Complete** (or the read-only variant) from the Plugin
Directory and sign in through your browser when Codex asks
(`codex mcp login nuday-complete` if it does not).

## Claude Code

The Manager serves its own marketplace with auto-update:

```
claude plugin marketplace add https://app.nuday.ai/plugins/marketplace.json
claude plugin install nuday-complete@nuday
```

This repository also works as a marketplace (`/plugin marketplace add
nuday-ai/nuday-plugins`), pinned to the same version.

## Cursor

Team/Enterprise admins: Dashboard → Plugins → Add Marketplace → Import from
Repo, using this repository. Otherwise download the ZIP from My Devices in
the Manager and follow its `INSTALL.md`.

## Other clients

Download the ZIP from **My Devices → NuDay Plugin** in the Manager; it carries
`INSTALL.md` for OpenCode and manual setups.

The plugin holds no credentials: the browser sign-in chooses your organization
and the client keeps its own tokens. Unattended use goes through an API key
(`*-api-key.json` in the plugin).
