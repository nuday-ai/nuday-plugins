---
name: read-pdf
description: Extract text, tables, and metadata from PDF documents
metadata:
  source: nuday
  catalog: platform
  category: documentation
  priority: '20'
---

# Read and work with PDFs

NuDay PDF is the platform's native PDF engine. Its installed Python
distribution/import name is `nuday-pdf` / `nuday_pdf`; do not install or
substitute PyPDF, PyPDF2, or the unrelated public package at runtime.

Before using an optional operation, inspect
`nuday_pdf.build_capabilities()`. The Manager deploys the complete profile
with OCR, Office conversion, ML/table, compliance, redaction, rendering,
and trust services. Treat the Manager capability response as authoritative
because a deliberately reduced deployment may disable an optional family.

## Bounded page-by-page extraction

```python
import nuday_pdf

capabilities = nuday_pdf.build_capabilities()
assert capabilities["read"] and capabilities["adaptive_text_extraction"]

document = nuday_pdf.PdfDocument("document.pdf", streaming=True)
if document.is_encrypted:
    raise ValueError("Authenticate the document through an approved flow first")

try:
    metadata = document.document_metadata()
    for page_index in range(document.page_count):
        try:
            text = document.extract_text_adaptive(page_index)
            tables = document.extract_tables(page_index)
            print(text, tables)
        finally:
            document.release_page(page_index)
finally:
    del document
```

Use the platform document pipeline for ordinary user uploads because it
enforces page, decoded-content, extracted-text, and request-size limits.
Call the engine directly only inside a bounded platform tool or worker.

## Other available native surfaces

The engine also exposes metadata and outlines, forms/FDF/XFDF, annotations,
attachments, search, rendering, redaction/sanitization, PDF/A and PDF/UA
validation/conversion, AES-256 encryption, signature inspection and PAdES
signing, Office conversion, and PDF creation from text/Markdown/HTML/images.
Use the typed PDF tools instead of importing native methods in an
Assistant process: `inspect_pdf`, `inspect_pdf_signatures`,
`fill_pdf_form`, `flatten_pdf_form`, `export_pdf_form_data`,
`import_pdf_form_data`, `encrypt_pdf`, `decrypt_pdf`,
`validate_pdf_compliance`, `convert_pdf_a`, `sign_pdf`,
`plan_pdf_redaction`, `apply_pdf_redaction`, `sanitize_pdf`, `create_pdf`,
`convert_to_pdf`, `merge_pdfs`, `split_pdf`, `extract_pdf_pages`,
`render_pdf_pages`, and `ocr_pdf`. These preserve originals, enforce
workspace permissions and limits, create versioned artifacts, and record
safe audit events. Passwords are Personal Secrets references. The signing
tools select the tenancy's approved authority and timestamp provider;
NuDay's platform authority is the default. Never load a PDF certificate
private key into an Assistant process.

Ask for explicit confirmation before flattening, decryption, applying
redactions, sanitization, or another operation that can materially change
disclosure or legal meaning. A redaction must be planned and reviewed
before its exact plan hash is applied.

Scanned/image-only pages require an OCR-capable complete worker. Never
silently invent text when OCR is unavailable; return a typed unsupported
result or route to that worker.
