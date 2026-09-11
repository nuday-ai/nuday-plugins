---
name: create-pdf
description: Generate professional PDF documents with headers, tables, and formatting
metadata:
  source: nuday
  catalog: platform
  category: documentation
  priority: '20'
---

# Create PDF

## Overview
Generate PDF documents programmatically using the bundled `create_pdf.py` helper script built on **ReportLab**.

## Usage

Run the helper script to produce a PDF:

```bash
python create_pdf.py --output report.pdf --title "My Report"
```

Or import the helper in your own code:

```python
from create_pdf import PDFBuilder

pdf = PDFBuilder("output.pdf", title="Quarterly Report")
pdf.add_heading("Section 1")
pdf.add_paragraph("Body text goes here.")
pdf.add_table([["Name", "Value"], ["Alpha", "100"], ["Beta", "200"]])
pdf.save()
```

## Capabilities
- **Headings** — multiple levels (h1-h3) with automatic styling
- **Paragraphs** — body text with word-wrap and configurable font/size
- **Tables** — grid tables with header row styling and alternating row colors
- **Page numbers** — automatic footer with page N of M
- **Margins & layout** — configurable page size (letter, A4) and margins

## Guidelines
1. Always specify an `--output` path so the caller knows where the file lands.
2. Keep table column counts consistent across all rows.
3. For long documents, call `pdf.add_page_break()` between major sections.
4. Prefer the helper script over raw ReportLab calls for consistency.
5. If ReportLab is not installed, install it: `pip install reportlab`.
