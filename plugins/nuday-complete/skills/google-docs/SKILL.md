---
name: google-docs
description: Read and edit Google Docs documents via MCP tools. Use when the user
  wants to view document content, create new documents, or insert and edit text.
metadata:
  source: nuday
  catalog: platform
  category: integration
  priority: '36'
---

# Google Docs

## Overview
You have access to Google Docs MCP tools. Use them to help users work with documents.

## Available Tools
- **list_documents**: List documents the user has access to
- **get_document**: Get document metadata and full text content
- **create_document**: Create a new document with a title and optional initial content
- **insert_text**: Insert text at a specific position or at the end of a document
- **replace_text**: Find and replace text within a document
- **delete_content**: Delete a range of content from a document

## Best Practices

### Reading Documents
- When showing document content, preserve the structure (headings, lists, paragraphs)
- Summarize long documents unless the user asks for the full text
- Note any images or embedded objects that can't be displayed in chat

### Creating Documents
- Ask for a descriptive title
- Offer to add initial content structure (headings, sections)

### Editing Documents
- Always confirm edits with the user before applying
- For find-and-replace, show a preview of what will change
- When inserting text, clarify the position (beginning, end, or after a specific section)

### Error Handling
- If the user hasn't connected their Google account, suggest they visit the Providers page
- Handle "document not found" errors gracefully
