---
name: notion
description: Read and manage pages, databases, and content in Notion workspaces. Use
  when the user wants to search, create, or update Notion pages and databases.
metadata:
  source: nuday
  catalog: platform
  category: integration
  priority: '48'
---

# Notion Integration

## Overview
You have access to the Notion MCP server which allows you to interact with Notion workspaces via the Notion API.

## Available Operations
- **Search pages** — Find pages and databases by title or content
- **Read page** — Get the full content of a specific page
- **Create page** — Create new pages in a workspace or database
- **Update page** — Edit page properties and content
- **Query database** — Retrieve and filter entries from Notion databases
- **Add blocks** — Append content blocks (text, headings, lists, code, etc.)

## Best Practices
- Use search with specific terms to find relevant pages
- When creating pages, structure content with proper headings and blocks
- For databases, use filters and sorts for efficient queries
- Show page titles and icons for easy identification
- Include links to Notion web UI for full-page viewing
- Preserve existing page structure when making edits
- Use proper block types (paragraph, heading_1/2/3, bulleted_list, numbered_list, code, etc.)

## Error Handling
- If the user hasn't connected their Notion account, suggest they visit the Providers page
- Handle "page not found" or "database not found" errors gracefully
- Respect workspace permissions — the integration can only access shared pages
