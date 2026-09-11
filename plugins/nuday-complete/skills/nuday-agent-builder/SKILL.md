---
name: nuday-agent-builder
description: Build and configure NuDay agents using the MCP tools. Use when creating
  new agents, updating agent configurations, or assembling agents from available resources
  like tools, skills, guardrails, guidelines, plugins, MCP servers, and knowledge
  bases.
metadata:
  source: nuday
  catalog: platform
  category: agent-building
  priority: '5'
---

# NuDay Agent Builder

## Overview
This skill guides you through building and configuring agents in NuDay using the
NuDay Manager MCP tools. Follow this workflow to create well-structured, production-ready agents.

## Available MCP Tools

| Tool | Purpose |
|------|---------|
| `nuday_agents_list` | List existing agents in the organization |
| `nuday_agents_get` | Get agent details and current config |
| `nuday_orgs_get` | Get organization details |
| `nuday_resolved_config` | Get the fully resolved (inherited) config |
| `nuday_list_secure_tools` | Browse available secure tools |
| `nuday_list_guardrails` | Browse available guardrails |
| `nuday_list_guidelines` | Browse available guidelines |
| `nuday_list_skills` | Browse available skills |
| `nuday_list_plugins` | Browse available plugins (bundles of the above) |
| `nuday_list_mcp_servers` | Browse available MCP servers |
| `nuday_list_knowledge_bases` | Browse available knowledge bases (RAG) |
| `nuday_agent_configure` | Create or update an agent with full config |

## Agent Creation Workflow

### Step 1: Discover Available Resources
Before building an agent, survey what's available:
1. Call `nuday_list_secure_tools` to see available tools
2. Call `nuday_list_skills` to see available skills
3. Call `nuday_list_guardrails` to see available safety guardrails
4. Call `nuday_list_guidelines` to see available behavior guidelines
5. Call `nuday_list_plugins` to see pre-built bundles
6. Call `nuday_list_mcp_servers` to see available MCP servers
7. Call `nuday_list_knowledge_bases` to see available knowledge bases

### Step 2: Design the Agent
Based on the user's requirements, decide:
- **Name & Description**: Clear, descriptive name and purpose
- **System Prompt**: Detailed instructions for the agent's behavior and persona
- **Tools**: Which secure tools and MCP servers the agent needs
- **Behaviors**: Which skills, guidelines, and guardrails to apply
- **Knowledge**: Which knowledge bases to attach for RAG
- **Plugins**: Whether any pre-built plugin bundles cover the needs

### Step 3: Create the Agent
Call `nuday_agent_configure` with no `agent_id` to create a new agent. The tool takes FLAT arguments (comma-separated strings for lists), NOT a nested config object:
```json
{
  "organization_id": "<org_id>",
  "name": "My Agent",
  "description": "What this agent does",
  "system_prompt": "You are a helpful assistant that...",
  "tools": "secure_tools:calculator,secure_tools:current_time",
  "mcp_servers": "<server_id>",
  "guardrails": "<guardrail_id>",
  "guidelines": "<guideline_id>",
  "skills": "<skill_id>",
  "plugins": "<plugin_id>",
  "rag_collections": "<kb_id>",
  "labels": "Production",
  "memory_enabled": true,
  "smart_feedback": false,
  "intent_scoring": true,
  "generate_file_enabled": true,
  "render_html_enabled": false
}
```
Attaching a knowledge base via `rag_collections` is enough for retrieval (the agent gets a `search_<slug>` tool at runtime); the `secure_tools:` prefix on `tools` is reference syntax, not part of a name.

### Step 4: Verify and Iterate
1. Call `nuday_agents_get` with `include_config=true` to verify the config — the bindings you set come back under `bindings` (and `config.agent.*`)
2. Call `nuday_resolved_config` to see the fully merged config with inheritance
3. Use `nuday_agent_configure` with the `agent_id` to make incremental updates

## System Prompt Best Practices
- Start with a clear role definition: "You are a [role] that [purpose]."
- Define the agent's personality and tone
- List specific capabilities and limitations
- Include examples of expected behavior
- Specify output format preferences
- Add safety boundaries and escalation rules

## Config Structure Reference

### Tools
Tools use the format `"secure_tools:<tool_name>"`. Get tool names from `nuday_list_secure_tools`.

### Guardrails
Guardrails are keyed by ID: `{"<id>": {"enabled": true}}`. Get IDs from `nuday_list_guardrails`.

### Guidelines & Skills
Both use the same format: `[{"id": "<id>", "enabled": true, "priority": <int>}]`.
Lower priority numbers = higher precedence.

### Plugins
Plugins bundle multiple components: `[{"id": "<id>", "enabled": true}]`.
A single plugin can include skills, guidelines, guardrails, tools, and MCP servers.

### Knowledge Bases
Knowledge bases are referenced by ID: `["<kb_id>"]`. Get IDs from `nuday_list_knowledge_bases`.

## Tips
- Use `nuday_list_plugins` first — a plugin may already bundle what you need
- Always add at least basic safety guardrails for production agents
- Use `nuday_resolved_config` to verify inherited settings from the parent org
- Set `memory_enabled: true` for agents that need conversation continuity
- Set `smart_feedback: true` for agents that should provide feedback to other agents when interacting with them
- Set `generate_file_enabled: true` for agents that should be able to generate and return downloadable files (enabled by default)
- Set `render_html_enabled: true` for agents that should be able to render full HTML pages (reports, dashboards) with preview, download, and open-in-new-tab (disabled by default)
