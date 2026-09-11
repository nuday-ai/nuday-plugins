---
name: create-docx
description: Generate Word documents with headings, tables, and rich formatting
metadata:
  source: nuday
  catalog: platform
  category: documentation
  priority: '20'
---

# Create DOCX

## Overview
Generate Microsoft Word (.docx) documents using the bundled `create_docx.py` helper script built on **python-docx**.

## Usage

Run the helper script:

```bash
python create_docx.py --output report.docx --title "My Report"
```

Or import the helper:

```python
from create_docx import DocxBuilder

doc = DocxBuilder("output.docx", title="Quarterly Report")
doc.add_heading("Section 1", level=1)
doc.add_paragraph("Body text goes here.")
doc.add_table([["Name", "Value"], ["Alpha", "100"], ["Beta", "200"]])
doc.add_bullet_list(["First item", "Second item", "Third item"])
doc.save()
```

## Capabilities
- **Headings** — levels 1-4 with Word's built-in heading styles
- **Paragraphs** — body text with optional bold/italic runs
- **Tables** — grid tables with header row styling
- **Bullet lists** — unordered lists using Word's List Bullet style
- **Numbered lists** — ordered lists using Word's List Number style
- **Page breaks** — explicit section separators

## Guidelines
1. Always specify an `--output` path.
2. Use heading levels consistently (h1 for sections, h2 for subsections).
3. If python-docx is not installed, install it: `pip install python-docx`.
4. For complex formatting, access the underlying `python-docx` Document via `doc.document`.
