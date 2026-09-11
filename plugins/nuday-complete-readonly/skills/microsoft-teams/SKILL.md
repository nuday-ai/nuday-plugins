---
name: microsoft-teams
description: Send messages, manage channels, and access teams in Microsoft Teams.
  Use when the user wants to communicate or collaborate through Teams.
metadata:
  source: nuday
  catalog: platform
  category: integration
  priority: '42'
---

# Microsoft Teams Integration

## Overview
You have access to the Microsoft Teams MCP server which allows you to interact with Microsoft Teams via the Microsoft Graph API.

## Available Operations
- **List teams** — View teams the user belongs to
- **List channels** — Browse channels within a team
- **Send message** — Post messages to channels or chats
- **Read messages** — Retrieve recent messages from channels or chats
- **Create channel** — Create new channels in a team
- **Manage memberships** — View and manage team members

## Best Practices
- Always confirm before sending messages to channels
- Format messages using Teams-compatible markdown
- Mention users with @-syntax when appropriate
- Keep channel messages focused and relevant
- Summarize long threads rather than dumping raw content

## Error Handling
- If the user hasn't connected their Microsoft account, suggest they visit the Providers page
- Handle "team not found" or "channel not found" errors gracefully
- Respect team/channel permissions — some may be restricted
