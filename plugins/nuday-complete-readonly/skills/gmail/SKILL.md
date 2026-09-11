---
name: gmail
description: Read and send emails via Gmail MCP tools. Use when the user wants to
  check their inbox, read emails, send messages, reply to threads, or manage labels.
metadata:
  source: nuday
  catalog: platform
  category: integration
  priority: '33'
---

# Gmail

## Overview
You have access to Gmail MCP tools. Use them to help users manage their email.

## Available Tools
- **list_messages**: List messages from inbox or search with a query (supports Gmail search operators)
- **get_message**: Get full details of a specific message by ID
- **send_message**: Send a new email with to, subject, body (HTML supported), cc, bcc
- **reply_to_message**: Reply to an existing email thread
- **list_labels**: List all Gmail labels (system and custom)
- **modify_labels**: Add or remove labels from a message (e.g., mark as read, archive)

## Best Practices

### Displaying Messages
- Show sender, subject, date, and a snippet when listing messages
- Format email content cleanly — strip excessive HTML if needed
- Indicate unread status and important labels
- For long threads, summarize the conversation

### Sending Emails
- Always confirm with the user before sending an email
- Ask for missing required fields (to, subject, body) if not provided
- Support both plain text and HTML body content
- Warn the user if they're about to send to many recipients

### Replying
- Show the original message context before composing a reply
- Confirm the reply content with the user before sending

### Searching
- Use Gmail search operators: from:, to:, subject:, has:attachment, is:unread, after:, before:
- Default to recent messages (last 7 days) if no time range specified

### Error Handling
- If the user hasn't connected their Gmail account, suggest they visit the Providers page
- If a token refresh fails, suggest reconnecting the account
- Handle permission errors gracefully
