---
name: agent-template
description: 'Reference for an agent-template repo (the working directory the coding
  agent is operating in, when it follows the agent-template layout): how to add agents,
  skills, guardrails, guidelines, and tools, plus the av CLI and GitHub Actions deploy
  flow. Use whenever editing or extending such a repo.'
metadata:
  source: nuday
  catalog: platform
  category: development
  priority: '25'
---

# agent-template repo

## Overview
An **agent-template** repo is the per-team home for agent definitions.
The current working directory is one if it has the layout below
(``agents/``, ``skills/``, ``guardrails/``, ``guidelines/``, ``tools/``
folders + ``environments.yml`` + a ``.github/workflows/deploy.yml``
that calls ``av deploy``). One agent-template repo can host many
agents; each lives as a single YAML file under ``agents/``. Resources
(skills, guardrails, guidelines, tools, plugins) can live inside the
repo for repo-scoped overrides, or be referenced by name from the
tenant-wide org-template repo (which the platform layers underneath).

## Layout

```
agents/              # agents/<slug>.yml — one agent per file
skills/              # skills/<name>/SKILL.md (markdown + YAML frontmatter)
guardrails/          # guardrails/<name>.md (output-evaluation prompts)
guidelines/          # guidelines/<name>.md (system-prompt rules)
tools/               # tools/<name>.py (Python @tool functions)
plugins/             # plugins/<name>.yml (re-exports of skills + guidelines)
evaluations/         # evaluations/*.yaml (test suites)
knowledge_bases/     # RAG configs (empty by default)
mcp_servers/         # MCP server configs (empty by default)
environments.yml     # per-env overrides (memory_enabled, smart_feedback, org UUIDs)
.github/workflows/deploy.yml   # manual-dispatch deploy
```

## Resource resolution order at runtime

For any resource referenced by name (a skill, guardrail, guideline,
tool, or plugin), the runtime checks in this order — first match wins:

1. **Local file in this repo** (e.g. ``skills/my-skill/SKILL.md``)
2. **Tenancy resource** (loaded from ``org-template`` for the active tenant)
3. **System resource** (shipped with NuDay Manager)

Same-named local files override org/system defaults. This is the main
mechanism for per-team customization without forking org-wide policy.

## Agent YAML

```yaml
name: agent-slug                  # used by ``av run dev --agent <slug>``
description: One-line summary
agent:
  system_prompt: |
    You are an agent that …
  llm_config: default-chat        # optional; defaults to tenancy default
  skills: [code-review, data-analysis]
  guardrails: [pii-redaction]
  guidelines: [house-style]
  tools: [execute, web_search]
  plugins: [analytics-pack]
  memory_enabled: false
  smart_feedback: false
```

Skills/guardrails/guidelines/tools/plugins are referenced by **name**.

## SKILL.md format (skills/<name>/SKILL.md)

```markdown
---
name: my-skill
description: Short description (max 1024 chars)
category: development
priority: 50
enabled: true
tags: [tag1, tag2]
allowed_tools: [execute]      # optional — gates which tools the skill can call
---

# My Skill

## Overview
One paragraph describing what + when to use.

## Usage
Step-by-step or code examples.
```

## Local development

```bash
# In the agent-template repo (i.e. the current working directory)
uv sync
cp .env.example .env             # set AGENT_VAULT_MANAGER_URL + token
av login                          # browser OAuth
av configure                      # picks tenancy + default LLM config

# Edit ``agents/<slug>.yml``, save, then:
uv run av run dev --agent <slug>  # auto-reloads on edit
```

To bootstrap a *new* agent-template repo from scratch, your
deployment provides its own template — use ``gh repo create
<repo-name> --template <your-template-org>/<your-template-repo>
--private`` against the template repo your platform admins
publish, then ``cd`` in.

## CI/CD: GitHub Actions

The deploy workflow (``.github/workflows/deploy.yml``) is **manual-dispatch
only** — pushes don't auto-deploy. Trigger it from the Actions tab:

| Input         | Type    | Notes                                      |
|---------------|---------|--------------------------------------------|
| ``environment``  | choice  | ``dev`` / ``test`` / ``prod`` (chooses GH Environment) |
| ``agent``        | string  | one slug, or ``--all``                     |
| ``dry_run``      | bool    | print plan without applying                |

**Required GH Environment vars/secrets:**
- ``AGENT_VAULT_MANAGER_URL`` (variable) — Manager URL
- ``AGENT_VAULT_API_TOKEN`` (secret) — service-principal token
- ``AGENT_VAULT_ORGANIZATION`` (variable) — tenancy UUID
  (must match the org-template's tenant)
- ``AGENT_VAULT_LLM_CONFIG_ID`` (variable, optional) — pin LLM config

**Commands the workflow runs:**
- ``uv run av deploy validate --project-dir . --env <env>`` — parse + expand
- ``uv run av deploy push --env <env> [--agent <slug>] [--dry-run] --yes`` — apply

Any ``${VAR}`` token in a manifest file resolves against the GH
Environment vars/secrets, so adding a new variable to a manifest only
needs a matching variable/secret in the Environment — no workflow edit
required.

## Common recipes

**Add a new agent:**
1. ``cp agents/hello-agent.yml agents/<new-slug>.yml``
2. Edit name, description, system_prompt, resource references
3. ``uv run av run dev --agent <new-slug>`` to test
4. Push to GitHub, run the deploy workflow with ``agent: <new-slug>``

**Add a new local skill:**
1. ``mkdir -p skills/<name>``
2. Write ``skills/<name>/SKILL.md`` with frontmatter + body
3. Reference it from ``agents/<slug>.yml`` under ``skills:``
4. The local skill overrides any same-named tenant or system skill

**Pull an existing remote agent into the repo:**
- ``uv run av deploy pull --agent-id <uuid>`` — writes ``agents/<slug>.yml``

**Run evaluations:**
- ``uv run av eval -f evaluations/my-suite.yaml --fail-threshold 0.8``
- Output a markdown report: ``av eval … --report markdown -o report.md``

## Conventions

1. Slugs are lowercase, hyphenated (``my-agent``, not ``MyAgent``).
2. Don't hardcode tenancy UUIDs in agent YAML — pull from ``environments.yml``.
3. Keep system_prompt reasonably short; offload detail to skills/guidelines.
4. Test locally with ``av run dev`` before pushing — the local resolution
   order means a missing local file silently falls back to org-template.
