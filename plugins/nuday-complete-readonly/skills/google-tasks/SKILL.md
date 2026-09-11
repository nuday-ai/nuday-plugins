---
name: google-tasks
description: Manage Google Tasks via MCP tools. Use when the user wants to view their
  to-do list, create tasks, mark tasks complete, or organize tasks with due dates.
metadata:
  source: nuday
  catalog: platform
  category: integration
  priority: '37'
---

# Google Tasks

## Overview
You have access to Google Tasks MCP tools. Use them to help users manage their tasks and to-do lists.

## Available Tools
- **list_task_lists**: Show all task lists the user has
- **list_tasks**: List tasks in a specific task list (defaults to the default list)
- **get_task**: Get full details of a specific task by ID
- **create_task**: Create a new task with title, notes, and optional due date
- **update_task**: Update an existing task (title, notes, due date, status)
- **complete_task**: Mark a task as completed
- **delete_task**: Delete a task

## Best Practices

### Displaying Tasks
- Show task title, status (completed/pending), due date, and notes
- Group tasks by status (pending first, then completed)
- Use checkboxes or status indicators for visual clarity
- Sort pending tasks by due date when available

### Creating Tasks
- Ask for at least a title; due date and notes are optional
- Parse natural language dates ("tomorrow", "next Friday", "end of week")
- Use ISO 8601 format for due dates when calling the API

### Managing Tasks
- Confirm before deleting tasks
- When marking tasks complete, show a brief confirmation
- Offer to create follow-up tasks when completing related work

### Error Handling
- If the user hasn't connected their Google account, suggest they visit the Providers page
- Handle "task not found" errors gracefully
