---
name: guidelines-management
description: Manage Guidelines — list, create, update, and delete agent behavioral
  guidelines using the Guidelines Manager MCP server. Use when an agent needs to browse
  available guidelines, define new behavioral rules, or maintain the guidelines registry.
metadata:
  source: nuday
  catalog: platform
  category: integration
  priority: '6'
---

# Guidelines Management

## Overview
This skill enables managing Guidelines through the Guidelines Manager MCP server.
Guidelines are behavioral rules that shape how agents respond — e.g., "use markdown",
"be concise", "use professional tone".

## Available MCP Tools

| Tool | Purpose |
|------|---------|
| `nuday_list_guidelines` | Browse guidelines with optional search/filter by category |
| `nuday_get_guideline` | Get full details including rule text |
| `nuday_create_guideline` | Create a new signed guideline |
| `nuday_update_guideline` | Update an existing guideline (re-signs automatically) |
| `nuday_delete_guideline` | Delete a guideline (creator/admin only) |

## Workflow

### Browsing Guidelines
1. Call `nuday_list_guidelines` with optional `query` or `category` filter
2. Categories: formatting, communication, behavior, safety, domain, coding, interaction, custom
3. Call `nuday_get_guideline` with a `guideline_id` to see the full rule text

### Creating a Guideline
1. Write a concise `rule_text` — this is injected directly into the agent's system prompt
2. Call `nuday_create_guideline` with `name`, `description`, and `rule_text`
3. Optionally set `category`, `tags`, `labels`, and `priority`

### Rule Text Best Practices
- Keep rules concise and unambiguous (max 1000 chars)
- Write in imperative form: "Always use...", "Never include..."
- Focus on one behavior per guideline
- Make rules testable — could someone verify compliance?

### Examples
- **Formatting**: "Always format code examples in fenced code blocks with the language identifier."
- **Communication**: "Use second person ('you') when addressing the user. Refer to yourself in first person."
- **Behavior**: "Never create new files unless explicitly asked. Prefer editing existing files."

### Permission Model
- **List/Get**: Users see their tenant's guidelines + system guidelines
- **Create**: Any authenticated user can create guidelines in their tenant
- **Update/Delete**: Only the creator or an admin can modify/delete
- **System guidelines**: Cannot be modified or deleted
Tenancy: `nuday_create_guideline` needs a tenancy. It uses your active one; if you belong to several (or hold a platform-admin key) pass `tenant_id` — a tenancy you belong to. `nuday_whoami` lists them. Config and secrets are never returned over MCP; unknown arguments are rejected with the valid names.
