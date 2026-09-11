---
name: org-template
description: 'Reference for an org-template repo (the working directory the coding
  agent is operating in, when it follows the org-template layout): how to manage tenant-wide
  config (LLM providers, configs, rate limits, skills, guardrails, users, alerting)
  and the av org CLI deploy flow. Use whenever editing or extending such a repo.'
metadata:
  source: nuday
  catalog: platform
  category: development
  priority: '25'
---

# org-template repo

## Overview
An **org-template** repo is the per-tenant home for organization-wide
configuration: who can access the tenant, which LLMs are available,
what rate limits apply, plus shared skills, guardrails, guidelines,
MCP servers, and alerting receivers. The current working directory is
one if it has the layout below (``organization.yml`` +
``environments.yml`` + ``llm-providers/`` / ``llm-configs/`` /
``llm-rate-limits/`` / ``skills/`` / ``guardrails/`` / ``guidelines/``
/ ``users/`` / ``alerting/`` folders + a ``.github/workflows/deploy.yml``
that calls ``av org``). One org-template repo provisions one tenancy;
agent-template repos under that tenant inherit everything by name.

## Layout

```
organization.yml     # tenancy display names per env, auto-access, embedding config
environments.yml     # per-env shallow-merge overrides
llm-providers/       # llm-providers/<name>.yml — credential envelopes
llm-configs/         # llm-configs/<name>.yml — model + fallback chain
llm-rate-limits/     # llm-rate-limits/<name>.yml — token caps
guidelines/          # guidelines/<name>.md — tenancy-wide system-prompt rules
guardrails/          # guardrails/<name>.md — tenancy-wide output policies
skills/              # skills/<name>/SKILL.md — tenancy-wide skills
mcp_servers/         # MCP server configs
connections/         # OAuth provider configs (Google, Microsoft, Slack, etc.)
alerting/
  receivers/         # alerting/receivers/<name>.yml — email, Slack, webhook
  inhibit-rules/     # suppress lower-severity alerts under critical
users/               # users/<email>.yml — seed users + permissions
.github/workflows/deploy.yml
```

## organization.yml

```yaml
names:
  dev: My Tenancy {env_label}     # {env_label} → "Dev" / "Prod"
  prod: My Tenancy
auto_access:
  - email_domain: example.com
    permission: CAN_VIEW          # or CAN_MANAGE
embedding:
  provider: openai
  model: text-embedding-3-small
  api_key: ${OPENAI_API_KEY}
  dim: 1536
sub_orgs:                         # optional nested tree
  - name: engineering
    sub_orgs:
      - name: platform
```

Names (not UUIDs) are stable IDs. ``{env_label}`` resolves at push.

## LLM stack

Three layers, all referenced by **name** at push time (resolved to
UUIDs in Manager):

**Provider** (``llm-providers/openai.yml``) — credentials only:

```yaml
name: openai
provider: openai
api_key: ${OPENAI_API_KEY}
```

**Config** (``llm-configs/default-chat.yml``) — model + fallback chain:

```yaml
name: default-chat
llm_provider: openai
model: gpt-4o-mini
fallbacks: [fallback-mini, fallback-mid]
```

**Rate limit** (``llm-rate-limits/per-user-daily.yml``) — token caps:

```yaml
name: per-user-daily
llm_config: default-chat
scope: user                       # or tenant
direction: input                  # or output
period: day                       # or hour, week
mode: enforce                     # or warn
max_tokens: 100000
```

## Users + permissions

```yaml
# users/alice@example.com.yml
email: alice@example.com
permission: CAN_MANAGE            # CAN_VIEW / CAN_USE / CAN_MANAGE
envs: [dev, prod]                 # optional — restrict to specific envs
```

## Local development

```bash
# In the org-template repo (i.e. the current working directory)
uv sync
cp .env.example .env
av login

# Validate without applying:
uv run av org validate --project-dir . --env dev

# Pull existing tenancy config into the repo:
uv run av org pull --project-dir . --env dev
```

To bootstrap a *new* org-template repo from scratch, your deployment
provides its own template — use ``gh repo create <repo-name>
--template <your-template-org>/<your-template-repo> --private``
against the template repo your platform admins publish, then ``cd``
in.

## CI/CD: GitHub Actions

Same shape as agent-template — manual dispatch only, ``environment`` +
``dry_run`` inputs. The workflow runs:

- ``uv run av org validate --project-dir . --env <env>``
- ``uv run av org push --env <env> [--dry-run] --yes``

The push step prints ``tenancy_uuid=<uuid>`` so downstream
agent-template workflows can reference the right tenant.

**Required GH Environment vars/secrets:**
- ``AGENT_VAULT_MANAGER_URL`` (variable)
- ``AGENT_VAULT_API_TOKEN`` (secret)
- ``OPENAI_API_KEY`` (secret) — if the org uses OpenAI
- ``EMBEDDING_*`` — if RAG / semantic memory is enabled
- ``SLACK_WEBHOOK_OPS`` (secret) — if Slack alerting is configured

## Push ordering

The reconciler applies in this order — each step idempotent:

1. Root org (tenancy) + sub-orgs
2. LLM providers → LLM configs (fallback chains in pass 2)
3. Guidelines → guardrails → skills → MCP servers
4. Connections (OAuth)
5. Users + permissions
6. Alerting receivers + inhibit rules
7. LLM rate limits (resolves config name → id)
8. Email-domain auto-access

## Common recipes

**Add a new tenant-wide skill** (visible to every agent in this org):
1. ``mkdir -p skills/<name> && edit skills/<name>/SKILL.md``
2. ``av org push --env dev --dry-run`` — preview
3. ``av org push --env dev --yes`` — apply
4. Agent-template agents reference by name in their YAML: ``skills: [<name>]``

**Add a new LLM provider:**
1. Create ``llm-providers/<name>.yml`` (api_key via ``${ENV_VAR}``)
2. Create ``llm-configs/<name>.yml`` referencing it
3. Add the corresponding GH Environment secret
4. Push

**Add a user with manage permissions:**
1. ``users/<email>.yml`` with ``permission: CAN_MANAGE``
2. Push — user appears in the NuDay UI on next login

## Conventions

1. Names are lowercase, hyphenated, stable across envs.
2. Never hardcode UUIDs — references are by name; UUIDs are tenancy-private.
3. Keep secrets in GH Environment, reference via ``${VAR}`` — never paste them.
4. Use ``environments.yml`` for per-env overrides; keep ``organization.yml`` env-agnostic.
5. Always ``--dry-run`` first when changing rate limits or auto-access rules.
