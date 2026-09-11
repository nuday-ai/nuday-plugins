---
name: salesforce
description: Access and manage CRM data in Salesforce. Use when the user wants to
  query leads, contacts, opportunities, cases, or manage CRM records.
metadata:
  source: nuday
  catalog: platform
  category: integration
  priority: '47'
---

# Salesforce Integration

## Overview
You have access to the Salesforce MCP server which allows you to interact with Salesforce CRM via the Salesforce REST API.

## Available Operations
- **SOQL queries** — Query any Salesforce object using SOQL
- **Create records** — Create new leads, contacts, opportunities, accounts, or cases
- **Update records** — Modify existing record fields
- **Search records** — Use SOSL for full-text search across objects
- **List objects** — Discover available Salesforce objects and their fields
- **View record** — Get full details of a specific record

## Best Practices
- Use SOQL for precise queries (e.g., `SELECT Id, Name FROM Account WHERE Industry = 'Technology'`)
- When creating records, include all required fields for the object type
- Show record IDs (18-char Salesforce IDs) for reference
- Format currency values with proper symbols and decimals
- Include links to Salesforce web UI for complex record views
- Use picklist values when updating fields — don't use arbitrary values

## Error Handling
- If the user hasn't connected their Salesforce account, suggest they visit the Providers page
- Handle "record not found" or "insufficient access" errors gracefully
- SOQL syntax errors should be caught and explained clearly
- Respect object-level and field-level security
