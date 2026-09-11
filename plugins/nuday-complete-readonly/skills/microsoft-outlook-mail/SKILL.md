---
name: microsoft-outlook-mail
description: Read and send emails via Microsoft Outlook / Exchange Online. Use when
  the user wants to manage their Outlook inbox, compose emails, or search messages.
metadata:
  source: nuday
  catalog: platform
  category: integration
  priority: '39'
---

# Microsoft Outlook Mail Integration

## Overview
You have access to the Microsoft Outlook Mail MCP server which allows you to interact with the user's Outlook mailbox via the Microsoft Graph API.

## Available Operations
- **List messages** — Retrieve recent emails from inbox or specific folders
- **Search messages** — Find emails by subject, sender, body content, or date
- **Read email** — Get the full content of a specific email
- **Send email** — Compose and send new emails
- **Reply to email** — Reply to or forward existing emails
- **Manage folders** — List, create, and organize mail folders

## Best Practices
- Always confirm before sending emails on behalf of the user
- Summarize long email threads rather than dumping raw content
- When searching, use specific criteria (sender, date range, keywords)
- Respect BCC/CC distinctions when replying
- Format email bodies with proper HTML when composing

## Error Handling
- If the user hasn't connected their Microsoft account, suggest they visit the Providers page
- Handle rate limits gracefully — Microsoft Graph has throttling limits
- If permissions are insufficient, explain which scopes are needed
