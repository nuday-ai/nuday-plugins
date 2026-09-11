---
name: google-contacts
description: Read and manage Google Contacts via MCP tools. Use when the user wants
  to look up contact information, add new contacts, or update existing contact details.
metadata:
  source: nuday
  catalog: platform
  category: integration
  priority: '38'
---

# Google Contacts

## Overview
You have access to Google Contacts MCP tools. Use them to help users manage their contacts.

## Available Tools
- **list_contacts**: List contacts, optionally filtered by group or search query
- **get_contact**: Get full details of a specific contact by resource name
- **search_contacts**: Search contacts by name, email, phone number, or company
- **create_contact**: Create a new contact with name, email, phone, company, and notes
- **update_contact**: Update an existing contact's information
- **delete_contact**: Delete a contact

## Best Practices

### Displaying Contacts
- Show name, email, phone number, and company when listing contacts
- Format phone numbers consistently
- Indicate primary vs. secondary contact methods

### Creating Contacts
- Ask for at least a name; other fields are optional
- Validate email format before creating
- Offer to add additional details (phone, company, address, notes)

### Searching
- Support fuzzy name matching
- Search across name, email, and phone fields
- Show the most relevant results first

### Privacy
- Be cautious about displaying full contact details — only show what's relevant
- Confirm before sharing contact information in group contexts

### Error Handling
- If the user hasn't connected their Google account, suggest they visit the Providers page
- Handle "contact not found" errors gracefully
