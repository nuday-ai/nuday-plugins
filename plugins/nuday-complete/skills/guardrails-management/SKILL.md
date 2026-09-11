---
name: guardrails-management
description: Manage Guardrails — list, create, update, and delete agent safety guardrails
  using the Guardrails Manager MCP server. Use when an agent needs to browse available
  guardrails, define new safety policies, or maintain the guardrails registry.
metadata:
  source: nuday
  catalog: platform
  category: security
  priority: '6'
---

# Guardrails Management

## Overview
This skill enables managing Guardrails through the Guardrails Manager MCP server.
Guardrails are safety policies that constrain agent behavior — they define content
filtering rules and safety checks that run on agent inputs and/or outputs.

## Available MCP Tools

| Tool | Purpose |
|------|---------|
| `nuday_list_guardrails` | Browse guardrails with optional search/filter by category |
| `nuday_get_guardrail` | Get full details including prompt template |
| `nuday_create_guardrail` | Create a new signed guardrail |
| `nuday_update_guardrail` | Update an existing guardrail (re-signs automatically) |
| `nuday_delete_guardrail` | Delete a guardrail (creator/admin only) |

## Workflow

### Browsing Guardrails
1. Call `nuday_list_guardrails` with optional `query` or `category` filter
2. Categories include: violent_crimes, privacy, hate, custom, and more
3. Call `nuday_get_guardrail` with a `guardrail_id` to see the full prompt template

### Creating a Guardrail
1. Write a `prompt_template` — this is the LLM prompt used to check content
2. Call `nuday_create_guardrail` with `name`, `description`, and `prompt_template`
3. Set `severity`: block (reject), warn (flag but allow), or log (record only)
4. Set `applies_to`: input (user messages), output (agent responses), or both

### Prompt Template Best Practices
- Clearly define what constitutes a violation
- Include examples of violating and non-violating content
- Use a structured output format (e.g., "SAFE" or "VIOLATION: reason")
- Keep templates focused on a single policy concern

### Severity Levels
| Level | Behavior |
|-------|----------|
| `block` | Reject the message entirely |
| `warn` | Flag the content but allow it through |
| `log` | Record the detection silently |

### Permission Model
- **List/Get**: Users see their tenant's guardrails + system guardrails
- **Create**: Any authenticated user can create guardrails in their tenant
- **Update/Delete**: Only the creator or an admin can modify/delete
- **System guardrails**: Cannot be modified or deleted
Tenancy: `nuday_create_guardrail` needs a tenancy. It uses your active one; if you belong to several (or hold a platform-admin key) pass `tenant_id` — a tenancy you belong to. `nuday_whoami` lists them. Config and secrets are never returned over MCP; unknown arguments are rejected with the valid names.
