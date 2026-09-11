---
name: microsoft-outlook-calendar
description: Read and manage Outlook Calendar events and scheduling. Use when the
  user wants to view, create, or manage calendar events in Microsoft Outlook.
metadata:
  source: nuday
  catalog: platform
  category: integration
  priority: '40'
---

# Microsoft Outlook Calendar Integration

## Overview
You have access to the Microsoft Outlook Calendar MCP server which allows you to interact with the user's Outlook Calendar via the Microsoft Graph API.

## Available Operations
- **List events** — Retrieve upcoming events from the user's calendar
- **Create event** — Schedule new meetings and appointments
- **Update event** — Modify existing event details (time, location, attendees)
- **Delete event** — Cancel or remove calendar events
- **Check availability** — View free/busy times for scheduling
- **Manage calendars** — List available calendars

## Best Practices
- Always confirm event details before creating or modifying
- Include timezone information when displaying times
- When scheduling meetings, check for conflicts first
- Use the availability check before proposing meeting times
- Include relevant details: subject, location, attendees, description

## Error Handling
- If the user hasn't connected their Microsoft account, suggest they visit the Providers page
- Handle "event not found" errors gracefully
- Respect calendar permissions — some calendars may be read-only
