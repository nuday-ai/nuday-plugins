---
name: google-calendar
description: Manage Google Calendar events via MCP tools. Use when the user wants
  to check their schedule, create meetings, update events, or manage calendar availability.
metadata:
  source: nuday
  catalog: platform
  category: integration
  priority: '31'
---

# Google Calendar

## Overview
You have access to Google Calendar MCP tools. Use them to help users manage their schedule.

## Available Tools
- **list_calendars**: Show all calendars the user has access to
- **list_events**: List events in a time range (defaults to next 7 days on primary calendar)
- **get_event**: Get full details of a specific event by ID
- **create_event**: Create a new event with title, start/end times, description, location, and attendees
- **update_event**: Modify an existing event (only changed fields need to be provided)
- **delete_event**: Remove an event by ID
- **quick_add_event**: Create an event from natural language (e.g. "Lunch with John tomorrow at noon")

## Best Practices

### Displaying Events
- Always format dates/times in a human-readable way
- Include the event title, time, location, and attendees when showing details
- When listing events, use a clean table or bullet format
- Show timezone information when relevant

### Creating Events
- Always confirm with the user before creating an event
- Ask for missing required fields (summary, start, end) if not provided
- Use ISO 8601 format for dates (e.g. '2025-03-15T09:00:00-07:00')
- Include timezone offsets in date strings when the user specifies a timezone
- For all-day events, use date-only format (e.g. '2025-03-15')

### Updating Events
- Confirm changes with the user before applying
- Only send the fields that need to change
- For recurring events, clarify whether to modify one instance or all

### Deleting Events
- Always ask for confirmation before deleting
- Show the event details so the user can verify

### Time Ranges
- If no time range is specified, default to the next 7 days
- When the user says "today", "tomorrow", or "this week", calculate appropriate time_min/time_max
- Use the user's local timezone when possible

### Error Handling
- If the user hasn't connected their Google Calendar, suggest they visit the Providers page
- If a token refresh fails, suggest reconnecting the account
- Handle "event not found" errors gracefully
