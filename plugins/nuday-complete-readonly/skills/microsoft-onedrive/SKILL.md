---
name: microsoft-onedrive
description: Read and manage files in Microsoft OneDrive. Use when the user wants
  to browse, upload, download, or organize files in OneDrive.
metadata:
  source: nuday
  catalog: platform
  category: integration
  priority: '41'
---

# Microsoft OneDrive Integration

## Overview
You have access to the Microsoft OneDrive MCP server which allows you to interact with the user's OneDrive storage via the Microsoft Graph API.

## Available Operations
- **List files** — Browse files and folders in OneDrive
- **Search files** — Find files by name, type, or content
- **Upload files** — Upload new files to OneDrive
- **Download files** — Retrieve file contents
- **Create folders** — Organize files into folder structures
- **Move/rename** — Move or rename files and folders
- **Share files** — Manage sharing permissions and links

## Best Practices
- Show file sizes in human-readable format (KB, MB, GB)
- Display modification dates relative to now ("2 hours ago")
- When listing folders, show item counts
- Confirm before overwriting existing files
- Respect sharing permissions — don't expose shared links unnecessarily

## Error Handling
- If the user hasn't connected their Microsoft account, suggest they visit the Providers page
- Handle "file not found" and "access denied" errors gracefully
- Large file operations may take time — indicate progress
