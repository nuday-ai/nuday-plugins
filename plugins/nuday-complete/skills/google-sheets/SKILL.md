---
name: google-sheets
description: Read and edit Google Sheets spreadsheets via MCP tools. Use when the
  user wants to view spreadsheet data, update cells, create new spreadsheets, or analyze
  tabular data.
metadata:
  source: nuday
  catalog: platform
  category: integration
  priority: '35'
---

# Google Sheets

## Overview
You have access to Google Sheets MCP tools. Use them to help users work with spreadsheets.

## Available Tools
- **list_spreadsheets**: List spreadsheets the user has access to
- **get_spreadsheet**: Get spreadsheet metadata (sheets, properties)
- **read_range**: Read cell values from a named range (e.g., "Sheet1!A1:D10")
- **write_range**: Write values to a cell range
- **append_rows**: Append rows to the end of a sheet
- **create_spreadsheet**: Create a new spreadsheet with a title
- **add_sheet**: Add a new sheet/tab to an existing spreadsheet
- **clear_range**: Clear values from a cell range

## Best Practices

### Reading Data
- Use A1 notation for ranges (e.g., "Sheet1!A1:D10", "Sheet1!A:A" for entire column)
- When displaying spreadsheet data, format it as a clean table
- Show column headers when available
- Summarize large datasets rather than dumping all rows

### Writing Data
- Always confirm changes with the user before writing
- Use appropriate data types (numbers, dates, strings)
- Preserve existing formatting when possible
- When appending rows, match the column structure of existing data

### Creating Spreadsheets
- Ask for a descriptive title
- Set up headers in the first row when creating structured data

### Formulas
- You can write formulas (e.g., "=SUM(A1:A10)") as cell values
- Explain what formulas do when the user asks about cell contents

### Error Handling
- If the user hasn't connected their Google account, suggest they visit the Providers page
- Handle "spreadsheet not found" and range errors gracefully
- Validate range notation before making API calls
