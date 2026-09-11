---
name: mcp-server-builder
description: Build Model Context Protocol (MCP) servers and tools. Use when creating
  custom MCP servers, defining tools, or integrating MCP capabilities.
metadata:
  source: nuday
  catalog: platform
  category: integration
  priority: '32'
---

# MCP Server Builder

## Overview
This skill helps build Model Context Protocol (MCP) servers for extending AI capabilities.

## MCP Server Structure

### Basic Server Setup (Python, mcp 2.x)
```python
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("my-server")


@mcp.tool()
def my_tool(param1: str) -> str:
    """Description of what the tool does."""
    return process_request(param1)


# Serve over Streamable HTTP (stateless — safe behind a load balancer):
# mcp.run(transport="streamable-http", stateless_http=True)
# or mount mcp.streamable_http_app() into an existing ASGI app (the HOST
# app's lifespan must enter mcp.session_manager.run()).
```

The input schema is derived from the function signature and docstring. For an
exact hand-written schema or full result control (_meta, is_error), drop to the
low-level Server: handlers are constructor kwargs (`Server("my-server",
on_list_tools=..., on_call_tool=...)`), each `async (ctx, params) -> Result`,
and you build `CallToolResult(content=[...])` yourself. Note: a low-level
handler exception becomes a generic JSON-RPC error — return
`CallToolResult(is_error=True, ...)` when the model should read the failure.

### Tool Design Guidelines

#### Input Schema
- Use clear, descriptive property names
- Provide helpful descriptions
- Set appropriate required fields
- Use enum for fixed choices

#### Tool Naming
- Use kebab-case: `my-tool-name`
- Be descriptive but concise
- Group related tools with prefixes

#### Error Handling
- Return meaningful error messages
- Use appropriate error types
- Include context in errors
- Log errors for debugging

## Server Configuration

### Transport Options
- **stdio**: For local processes
- **Streamable HTTP**: For HTTP-based servers (stateless with mcp 2.x / the 2026-07-28 spec; SSE is superseded, WebSocket was removed)

### Security
- Validate all inputs
- Sanitize outputs
- Use authentication when needed
- Limit resource access

## Testing
- Test each tool individually (the in-memory `Client(mcp)` needs no transport)
- Verify error handling
- Check edge cases
- Test with actual AI interactions
