---
name: skills-management
description: Manage Skills — list, create, update, and delete agent skill definitions
  using the Skills Manager MCP server. Use when an agent needs to browse available
  skills, author new instruction sets, or maintain the skills registry.
metadata:
  source: nuday
  catalog: platform
  category: integration
  priority: '6'
---

# Skills Management

## Overview
This skill enables managing Skills through the Skills Manager MCP server.
Skills are reusable instruction sets (markdown documents) that give agents
specific capabilities — e.g., code review, data analysis, debugging.

## Available MCP Tools

| Tool | Purpose |
|------|---------|
| `nuday_list_skills` | Browse skills with optional search/filter by category |
| `nuday_get_skill` | Get full details including instruction text |
| `nuday_create_skill` | Create a new signed skill |
| `nuday_update_skill` | Update an existing skill (re-signs automatically) |
| `nuday_delete_skill` | Delete a skill (creator/admin only) |

## Workflow

### Browsing Skills
1. Call `nuday_list_skills` with optional `query` or `category` filter
2. Categories: development, documentation, creative, communication, data, integration, automation, security, devops, domain, custom
3. Call `nuday_get_skill` with a `skill_id` to see the full instruction text

### Creating a Skill
1. Write the instruction text in Markdown — this becomes part of the agent's system prompt
2. Call `nuday_create_skill` with `name` (lowercase-hyphenated), `description`, and `instruction_text`
3. Optionally set `category`, `tags`, `labels`, and `priority` (1-100, lower = higher precedence)

### Skill Instruction Text Best Practices
- Start with a `# Title` and `## Overview` section
- Use structured sections with clear headings
- Include examples and code blocks where appropriate
- Keep instructions actionable and specific
- Define output format expectations

### Permission Model
- **List/Get**: Users see their tenant's skills + system skills
- **Create**: Any authenticated user can create skills in their tenant
- **Update/Delete**: Only the creator or an admin can modify/delete
- **System skills**: Cannot be modified or deleted
- **Duplicate names**: Not allowed within the same tenant
Tenancy: `nuday_create_skill` needs a tenancy. It uses your active one; if you belong to several (or hold a platform-admin key) pass `tenant_id` — a tenancy you belong to. `nuday_whoami` lists them. Config and secrets are never returned over MCP; unknown arguments are rejected with the valid names.
