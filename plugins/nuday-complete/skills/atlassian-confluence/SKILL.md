---
name: atlassian-confluence
description: Read and manage pages, spaces, and content in Atlassian Confluence. Use
  when the user wants to search documentation, create wiki pages, or manage knowledge
  base content.
metadata:
  source: nuday
  catalog: platform
  category: integration
  priority: '46'
---

# Confluence Integration

## Overview
You have access to the Confluence MCP server which allows you to interact with Atlassian Confluence via the Confluence Cloud REST API.

## Available Operations
- **Search pages** — Find pages by title, content, or labels using CQL
- **Read page** — Get the full content of a specific page
- **Create page** — Create new pages in a space
- **Update page** — Edit existing page content
- **List spaces** — View available spaces
- **Add comment** — Add comments to pages
- **Manage labels** — Add or remove labels from pages

## Best Practices
- Use CQL for precise searches (e.g., `space = DEV AND type = page AND text ~ "deployment"`)
- When creating pages, use proper Confluence storage format (XHTML)
- Show page titles and space keys for easy identification
- Include links to Confluence web UI for viewing full pages
- Summarize long pages rather than returning the full content
- Preserve existing page content when making edits

## Error Handling
- If the user hasn't connected their Atlassian account, suggest they visit the Providers page
- Handle "page not found" or "space not found" errors gracefully
- Respect space permissions — users may not have access to all spaces
