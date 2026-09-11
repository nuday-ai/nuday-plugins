---
name: slack
description: Read and send messages, manage channels, and access workspace data in
  Slack. Use when the user wants to communicate or collaborate through Slack.
metadata:
  source: nuday
  catalog: platform
  category: integration
  priority: '44'
---

# Slack Integration

## Overview
You have access to the Slack MCP server which allows you to interact with Slack workspaces via the Slack Web API.

## Available Operations
- **List channels** — Browse public and private channels
- **Send message** — Post messages to channels or direct messages
- **Read messages** — Retrieve recent messages from channels or conversations
- **Search messages** — Search across the workspace for specific content
- **Manage reactions** — Add or remove emoji reactions
- **View profiles** — Look up user profiles and status

## Best Practices
- Always confirm before sending messages to channels
- Use Slack's mrkdwn formatting for rich messages
- Mention users with <@USER_ID> syntax
- Keep messages concise and well-formatted
- Use threads for follow-up replies to avoid channel noise
- Summarize long conversations rather than dumping raw content

## Error Handling
- If the user hasn't connected their Slack account, suggest they visit the Providers page
- Handle "channel not found" or "not in channel" errors gracefully
- Respect workspace permissions — some channels may be restricted
