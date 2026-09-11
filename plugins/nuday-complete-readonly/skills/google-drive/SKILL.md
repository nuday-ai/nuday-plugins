---
name: google-drive
description: Read and manage files in Google Drive via MCP tools. Use when the user
  wants to find files, upload or download documents, create folders, or manage sharing.
metadata:
  source: nuday
  catalog: platform
  category: integration
  priority: '34'
---

# Google Drive

## Overview
You have access to Google Drive MCP tools. Use them to help users manage their files and folders.

## Available Tools
- **list_files**: List files and folders, optionally filtered by type, parent folder, or search query
- **get_file**: Get metadata for a specific file by ID
- **search_files**: Search files by name, content, type, or other criteria
- **download_file**: Download/export file content (returns text for docs, CSV for sheets, etc.)
- **upload_file**: Upload a new file with name, content, MIME type, and optional parent folder
- **create_folder**: Create a new folder in Drive
- **move_file**: Move a file to a different folder
- **rename_file**: Rename a file or folder
- **share_file**: Share a file with specific users or make it publicly accessible
- **delete_file**: Move a file to trash

## Best Practices

### Displaying Files
- Show file name, type, size, last modified date, and owner when listing
- Use icons or labels to distinguish between files, folders, and shared items
- Format file sizes in human-readable units (KB, MB, GB)

### Uploading Files
- Confirm the file name and destination folder with the user
- Detect and set the correct MIME type automatically when possible

### Searching
- Use Drive search operators: name contains, mimeType, modifiedTime, owner
- Default to the user's My Drive root if no folder is specified

### Sharing
- Always confirm sharing permissions with the user before applying
- Explain the difference between viewer, commenter, and editor roles
- Warn when sharing publicly or with external users

### Error Handling
- If the user hasn't connected their Google Drive, suggest they visit the Providers page
- Handle "file not found" and permission errors gracefully
