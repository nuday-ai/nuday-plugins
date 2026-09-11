---
name: atlassian-jira
description: Manage issues, projects, and boards in Atlassian Jira. Use when the user
  wants to create, update, or search issues, manage sprints, or track project progress.
metadata:
  source: nuday
  catalog: platform
  category: integration
  priority: '45'
---

# Jira Integration

## Overview
You have access to the Jira MCP server which allows you to interact with Atlassian Jira via the Jira Cloud REST API.

## Available Operations
- **Search issues** — Find issues using JQL (Jira Query Language)
- **Create issue** — Create new issues (bugs, stories, tasks, epics)
- **Update issue** — Modify issue fields (summary, description, assignee, priority)
- **Transition issue** — Move issues through workflow statuses (To Do → In Progress → Done)
- **Add comment** — Add comments to issues
- **List projects** — View available projects and their boards
- **Sprint management** — View sprints and their contents

## Best Practices
- Use JQL for precise issue searches (e.g., `project = PROJ AND status = "In Progress"`)
- When creating issues, include: summary, description, issue type, priority, and assignee
- Show issue keys prominently (e.g., PROJ-123)
- Format descriptions using Jira wiki markup or markdown
- Include links to Jira web UI for complex operations
- Display status, priority, and assignee in issue summaries

## Error Handling
- If the user hasn't connected their Atlassian account, suggest they visit the Providers page
- Handle "issue not found" or "project not found" errors gracefully
- Respect project permissions — users may not have access to all projects
