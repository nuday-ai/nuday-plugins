---
name: secure-tools-management
description: Build, test, list, update, and delete cryptographically signed Secure
  Tools via the AV Manager MCP server — including executing a tool with sample args
  to verify it works. Use when an agent needs to author new tool definitions, test
  them, or maintain the tool registry.
metadata:
  source: nuday
  catalog: platform
  category: integration
  priority: '6'
---

# Secure Tools — Build & Test

## Overview
Secure Tools are cryptographically signed, tamper-proof Python tool
definitions that agents can invoke at runtime. This skill covers the full
lifecycle — author, **test**, refine, and maintain — via the NuDay Manager
MCP server. (See also [[nuday-agent-builder]] to attach a finished tool to
an agent, and [[skills-management]] for instruction-only capabilities.)

## Available MCP Tools

| Tool | Purpose |
|------|---------|
| `nuday_list_secure_tools` | Browse available tools (optional `query`) |
| `nuday_get_secure_tool` | Full details of a tool, including source code |
| `nuday_create_secure_tool` | Create a new signed tool |
| `nuday_test_secure_tool` | Execute a tool with args to verify it works |
| `nuday_update_secure_tool` | Update a tool (re-signs automatically) |
| `nuday_delete_secure_tool` | Delete a tool (creator/admin only) |

## Build → test → iterate loop
Always test a tool right after creating or updating it — never hand an
unverified tool to an agent.

### 1. Author
Write the Python source using the `@tool` decorator from LangChain:
```python
@tool
def my_tool(param1: str, param2: int = 10) -> str:
    """One-line summary the model reads to decide when to call this.

    Args:
        param1: what it is.
        param2: what it is (defaults to 10).
    """
    # Implementation here
    return f"Result: {param1} with {param2}"
```
Call `nuday_create_secure_tool` with `name`, `description`, and `source_code`
(optionally `tags`, `labels`). The tool is signed with Ed25519 on save.

### 2. Test
Call `nuday_test_secure_tool` with the tool `name` and a JSON `args` string:
```
nuday_test_secure_tool(tool_name="my_tool", args='{"param1": "hi", "param2": 3}')
```
It runs the tool in the sandbox and returns `success`, the `result` (or
`error`), and `execution_time_ms`. Test the happy path AND at least one
edge/error case (missing arg, wrong type, empty input).

### 3. Iterate
If a test fails, call `nuday_get_secure_tool` to review the source, fix it with
`nuday_update_secure_tool` (re-signs automatically), and test again. Repeat
until the tool behaves correctly.

## Tool-authoring best practices
- **Docstring is the contract** — the first line + `Args:` are what the
  model uses to decide when and how to call the tool. Be precise.
- **Type every parameter** — types drive the generated input schema.
- **Return strings (or JSON-serializable values)** the model can read; never
  return objects that don't serialize.
- **Handle errors in-tool** — catch and return a clear message rather than
  raising; a raised exception surfaces as a failed call.
- **Never inline secrets or credentials** in source — read them from the
  environment / platform secret injection, never hardcoded literals.
- **Keep tools focused and deterministic** — one job per tool; avoid hidden
  global state.
- **Prefer the standard library** or already-available deps; exotic imports
  may not be present in the sandbox.

## Permission model
- **List/Get/Test**: users see + can test their tenant's tools + system tools.
- **Create**: any authenticated user can create tools in their tenant.
- **Update/Delete**: only the creator or an admin can modify/delete.
- **System tools**: cannot be modified or deleted.

## Tenancy
Call `nuday_whoami` once (or read the connect-time instructions) for your
`principal_kind`: `single_tenancy` and `tenant_pinned` never pass `tenant_id`;
`multi_tenancy` passes `tenant_id` on `nuday_create_secure_tool` only;
`platform_admin` always passes `tenant_id` on creates and may pass it to scope
`nuday_list_secure_tools` (rows carry `tenant_id`/`tenant_name`), finding ids
with `nuday_tenancies_list(query=…)`. On a "tenant_id is not needed" error drop
the argument; on "not a tenancy you can access" pick one of the listed ids.
Tool source is returned, but credentials never are: reference secrets by
name, never inline them.
